"""Tool registry — the single source of truth for what autoMate can do.

A ``Tool`` is anything callable with a JSON-schema parameter spec. The same
registry feeds three surfaces:

1. The Agent loop (LLM picks tools by name)
2. The HTTP API (POST /api/execute/<tool>)
3. The MCP bridge (tools auto-exported to any MCP client)

Tools fall into three buckets, distinguished only by namespace prefix:
- ``shell.*`` / ``script.*`` / ``browser.*`` / ``desktop.*`` — local execution
- ``<integration>.*`` — third-party SaaS (github, notion, slack, ...)
"""
from __future__ import annotations

import inspect
from dataclasses import dataclass, field
from typing import Any, Callable

from ..tracing import trace_action


@dataclass
class Tool:
    name: str
    description: str
    parameters: dict[str, Any]
    handler: Callable[..., Any]
    category: str = "general"          # 'system' | 'browser' | 'desktop' | 'integration' | ...
    requires: list[str] = field(default_factory=list)  # connection ids needed
    danger: str = "low"                # 'low' | 'medium' | 'high' (UI hint)
    tier: str = "free"                 # 'free' | 'pro' — pro tools require a logged-in cloud session

    def call(self, args: dict[str, Any]) -> Any:
        with trace_action(self.name, self.category):
            sig = inspect.signature(self.handler)
            accepted = {k: v for k, v in args.items() if k in sig.parameters}
            return self.handler(**accepted)


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' already registered")
        self._tools[tool.name] = tool

    def add(self, *, name: str, description: str, parameters: dict | None = None,
            category: str = "general", requires: list[str] | None = None,
            danger: str = "low") -> Callable[[Callable], Callable]:
        """Decorator form. Use for ad-hoc registrations."""
        def deco(fn: Callable) -> Callable:
            self.register(Tool(
                name=name,
                description=description,
                parameters=parameters or {"type": "object", "properties": {}},
                handler=fn,
                category=category,
                requires=requires or [],
                danger=danger,
            ))
            return fn
        return deco

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def all(self) -> list[Tool]:
        return list(self._tools.values())

    def by_category(self) -> dict[str, list[Tool]]:
        out: dict[str, list[Tool]] = {}
        for t in self._tools.values():
            out.setdefault(t.category, []).append(t)
        return out


def build_default_registry() -> ToolRegistry:
    """Construct the registry with built-in executors and integration tools."""
    from . import shell as _shell
    from . import script as _script
    from . import browser as _browser
    from . import browser_ext as _bx
    from . import desktop as _desktop
    from . import notes as _notes
    from . import files as _files
    from . import reminders as _reminders
    from . import memory as _memory
    from . import search as _search
    from . import audio as _audio
    from . import integrations_adapter as _ia

    reg = ToolRegistry()
    # Personal-infra tools first — these are autoMate's identity.
    _search.register(reg)            # search.find — preferred entry for "find me X"
    _notes.register(reg)
    _files.register(reg)
    _reminders.register(reg)
    _memory.register(reg)
    _audio.register(reg)             # audio.transcribe — first Pro-tier tool
    # Then the local executors and integrations.
    _shell.register(reg)
    _script.register(reg)
    _browser.register(reg)
    _bx.register(reg)
    _desktop.register(reg)
    _ia.register(reg)
    return reg
