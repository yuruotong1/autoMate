"""
Human-in-the-loop learner.

When the engine cannot locate an element it calls Learner.teach(step).
The learner:
  1. Prompts the user to click the target element.
  2. Captures the click coordinates via pynput.
  3. Takes a screenshot crop → saves template PNG.
  4. Reads nearby OCR text to build a refined hint.
  5. Patches the script's Markdown body to add the learned hint inline
     so future runs use it without asking again.
  6. Returns (x, y) so the engine can immediately proceed.
"""

from __future__ import annotations

import logging
import re
import threading
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from .locators import nearby_ocr_text
from .script import MarkdownStep, Script

log = logging.getLogger(__name__)

_SNAPSHOTS_DIR = Path.home() / ".automate" / "snapshots"
_TEMPLATE_MARGIN = 40   # pixels


# ---------------------------------------------------------------------------
# Mouse click capture
# ---------------------------------------------------------------------------

def _capture_click(timeout: float = 30.0) -> Optional[tuple[int, int]]:
    result: list[Optional[tuple[int, int]]] = [None]
    done   = threading.Event()

    try:
        from pynput import mouse

        def on_click(x, y, button, pressed):
            if pressed:
                result[0] = (int(x), int(y))
                done.set()
                return False

        listener = mouse.Listener(on_click=on_click)
        listener.start()
        done.wait(timeout=timeout)
        listener.stop()
    except Exception as exc:
        log.debug("pynput error: %s", exc)

    return result[0]


# ---------------------------------------------------------------------------
# Template snapshot
# ---------------------------------------------------------------------------

def _save_template(x: int, y: int) -> Optional[str]:
    try:
        import cv2
        import numpy as np
        import pyautogui

        _SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)

        screenshot = pyautogui.screenshot()
        img_bgr    = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        h, w       = img_bgr.shape[:2]

        x1, y1 = max(0, x - _TEMPLATE_MARGIN), max(0, y - _TEMPLATE_MARGIN)
        x2, y2 = min(w, x + _TEMPLATE_MARGIN), min(h, y + _TEMPLATE_MARGIN)

        filename = f"tmpl_{uuid.uuid4().hex[:8]}.png"
        cv2.imwrite(str(_SNAPSHOTS_DIR / filename), img_bgr[y1:y2, x1:x2])
        log.debug("Saved template: %s", filename)
        return filename
    except Exception as exc:
        log.debug("Template save error: %s", exc)
        return None


# ---------------------------------------------------------------------------
# Learner
# ---------------------------------------------------------------------------

class Learner:
    def __init__(self, print_fn=print):
        self._print = print_fn

    def teach(
        self,
        step: MarkdownStep,
        script: Optional[Script] = None,
        timeout: float = 30.0,
    ) -> Optional[tuple[int, int]]:
        """
        Prompt the user to click the target element.

        If *script* is provided the Markdown body is updated in-place to
        embed the learned hint so future runs succeed without asking.

        Returns (x, y) or None if the user did not click in time.
        """
        self._print(
            f"\n[autoMate] Step {step.index}: '{step.text}'\n"
            "Please click the target element now…"
        )

        xy = _capture_click(timeout=timeout)
        if xy is None:
            self._print("[autoMate] No click detected — aborting step.")
            return None

        x, y = xy
        self._print(f"[autoMate] Got click at ({x}, {y}) — learning…")

        # Best hint: prefer nearby OCR text, fall back to coord
        ocr_text = nearby_ocr_text(x, y)
        if ocr_text and len(ocr_text.strip()) >= 2:
            learned_hint = f"[click:{ocr_text.strip()}]"
        else:
            learned_hint = f"[click:coord={x},{y}]"

        # Save template snapshot (best-effort)
        _save_template(x, y)

        # Patch the Markdown body so the hint is remembered
        if script is not None:
            script.body = _inject_hint(script.body, step.index, learned_hint)
            log.debug("Patched step %d with hint: %s", step.index, learned_hint)

        self._print(f"[autoMate] Learned hint: {learned_hint}  Resuming.\n")
        return (x, y)


# ---------------------------------------------------------------------------
# Markdown body patching
# ---------------------------------------------------------------------------

def _inject_hint(body: str, step_index: int, hint: str) -> str:
    """
    Add *hint* at the end of the numbered list item that corresponds to
    *step_index* (1-based) inside the ## Steps section of *body*.
    If the step already contains a [click:…] or [coord:…] hint it is
    replaced; otherwise *hint* is appended.
    """
    lines  = body.splitlines(keepends=True)
    result = []
    in_steps = False
    item_count = 0

    for line in lines:
        stripped = line.rstrip("\n")

        # Toggle steps section
        if re.match(r"^##\s+Steps", stripped, re.IGNORECASE):
            in_steps = True
            result.append(line)
            continue
        if re.match(r"^##\s+", stripped) and in_steps:
            in_steps = False

        if in_steps and re.match(r"^(?:\d+\.|[-*])\s+", stripped):
            item_count += 1
            if item_count == step_index:
                # Replace existing click/coord hint or append
                new_line = re.sub(r"\[(?:click|coord):[^\]]*\]", "", stripped).rstrip()
                new_line = f"{new_line} {hint}\n"
                result.append(new_line)
                continue

        result.append(line)

    return "".join(result)
