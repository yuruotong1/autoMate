"""Opt-in, local tool traces and vendor-neutral devtools event hooks.

Payloads are intentionally excluded: arguments, results and exception messages
can contain credentials or personal data. Hooks receive metadata only.
"""
from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from datetime import datetime, timezone
import json
import logging
import os
from threading import RLock
from time import perf_counter
from typing import Callable
from uuid import uuid4

from .settings import PATHS

_log = logging.getLogger(__name__)
_lock = RLock()
_hooks: list[Callable[[dict], None]] = []
_parent: ContextVar[str | None] = ContextVar("automate_trace_parent", default=None)


def enabled() -> bool:
    return os.environ.get("AUTOMATE_DEVTOOLS", "").strip().lower() in {
        "1", "true", "yes", "on",
    }


def add_trace_hook(hook: Callable[[dict], None]) -> Callable[[], None]:
    """Subscribe to enabled traces; return an idempotent unsubscribe function.

    Hooks run synchronously and should enqueue slow work. Hook failures never
    change tool results. Register hooks before executing tools.
    """
    with _lock:
        _hooks.append(hook)

    def unsubscribe() -> None:
        with _lock:
            if hook in _hooks:
                _hooks.remove(hook)

    return unsubscribe


def _emit(event: dict) -> None:
    event = {"schema_version": 1, "timestamp": datetime.now(timezone.utc).isoformat(),
             "pid": os.getpid(), **event}
    try:
        with _lock:
            PATHS.logs.mkdir(parents=True, exist_ok=True)
            # One file per process avoids interleaved records across workers.
            path = PATHS.logs / f"trace-{os.getpid()}.jsonl"
            with path.open("a", encoding="utf-8") as stream:
                stream.write(json.dumps(event, ensure_ascii=False) + "\n")
    except Exception:
        _log.warning("Could not write autoMate trace event")
    with _lock:
        hooks = tuple(_hooks)
    for hook in hooks:
        try:
            hook(dict(event))
        except Exception:
            _log.warning("autoMate trace hook failed")


@contextmanager
def trace_action(name: str, category: str):
    """Emit paired start/end (or error) events without changing execution."""
    if not enabled():
        yield
        return
    action_id = uuid4().hex
    metadata = {"action_id": action_id, "parent_id": _parent.get(),
                "tool": name, "category": category}
    token = _parent.set(action_id)
    start = perf_counter()
    try:
        _emit({**metadata, "event": "action.start"})
        try:
            yield
        except BaseException as exc:
            _emit({**metadata, "event": "action.error",
                   "duration_ms": (perf_counter() - start) * 1000,
                   "error_type": type(exc).__name__})
            raise
        else:
            _emit({**metadata, "event": "action.end",
                   "duration_ms": (perf_counter() - start) * 1000})
    finally:
        _parent.reset(token)
