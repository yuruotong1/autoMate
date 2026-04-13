"""
Script execution engine.

For each step in a Markdown script the engine:
  1. Checks for inline hints ([click:OK], [type:hello], etc.)
     → executes directly if a hint is found.
  2. Falls back to AI vision-based interpretation for natural-language steps
     that have no hints.
  3. When the target element cannot be located the engine delegates to the
     human-in-the-loop learning callback (on_teach).
"""

from __future__ import annotations

import logging
import time
import traceback
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Callable, Optional

import pyautogui

from .locators import resolve_ocr, resolve_image, resolve_coord
from .script import MarkdownStep, Script

log = logging.getLogger(__name__)

pyautogui.FAILSAFE = True
pyautogui.PAUSE    = 0.05


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------

class StepStatus(Enum):
    OK       = auto()
    SKIPPED  = auto()
    TEACH_ME = auto()   # location not found → need human demo
    ERROR    = auto()


@dataclass
class StepResult:
    index:   int
    status:  StepStatus
    message: str = ""


@dataclass
class RunResult:
    script_name:  str
    success:      bool
    step_results: list[StepResult] = field(default_factory=list)
    error:        Optional[str] = None


# ---------------------------------------------------------------------------
# Callback types
# ---------------------------------------------------------------------------

# Called when a step cannot be located.
# Signature: (step: MarkdownStep) -> Optional[tuple[int, int]]
TeachCallback = Callable[[MarkdownStep], Optional[tuple[int, int]]]

# Called after each step.
# Signature: (step: MarkdownStep, result: StepResult) -> None
ProgressCallback = Callable[[MarkdownStep, StepResult], None]


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------

class Engine:
    def __init__(
        self,
        on_teach:    Optional[TeachCallback]    = None,
        on_progress: Optional[ProgressCallback] = None,
        use_ai_fallback: bool = True,
    ):
        self.on_teach        = on_teach
        self.on_progress     = on_progress
        self.use_ai_fallback = use_ai_fallback

    # ── public entry point ──────────────────────────────────────────────

    def run(self, script: Script) -> RunResult:
        steps  = script.steps()
        result = RunResult(script_name=script.name, success=False)
        script.total_runs += 1

        for step in steps:
            sr = self._run_step(step, script)
            result.step_results.append(sr)

            if self.on_progress:
                self.on_progress(step, sr)

            if sr.status in (StepStatus.ERROR, StepStatus.TEACH_ME):
                result.error = sr.message
                return result

        result.success   = True
        script.success_runs += 1
        return result

    # ── step dispatch ────────────────────────────────────────────────────

    def _run_step(self, step: MarkdownStep, script: Script) -> StepResult:
        log.info("Step %d: %s", step.index, step.text)

        # Code block → exec directly
        if step.is_code:
            return self._exec_code(step)

        action = step.action

        # No hint → AI interpretation
        if not action:
            if self.use_ai_fallback:
                return self._ai_interpret(step, script)
            return StepResult(step.index, StepStatus.SKIPPED,
                              "No action hint and AI fallback disabled")

        # Hinted actions
        try:
            return self._exec_hinted(step)
        except Exception as exc:
            log.exception("Step %d error", step.index)
            return StepResult(step.index, StepStatus.ERROR, str(exc))

    # ── direct hint execution ────────────────────────────────────────────

    def _exec_hinted(self, step: MarkdownStep) -> StepResult:
        action = step.action
        value  = step.value
        hints  = step.hints

        if action == "wait":
            secs = float(value or "1")
            time.sleep(secs)
            return StepResult(step.index, StepStatus.OK, f"waited {secs}s")

        if action == "key":
            key = value or ""
            if "+" in key:
                pyautogui.hotkey(*key.split("+"))
            else:
                pyautogui.press(key)
            return StepResult(step.index, StepStatus.OK, f"key {key!r}")

        if action == "type":
            xy = self._resolve_location(step)
            if xy:
                pyautogui.click(*xy)
                time.sleep(0.1)
            if value:
                pyautogui.typewrite(value, interval=0.04)
            return StepResult(step.index, StepStatus.OK, f"typed {value!r}")

        if action in ("click", "double_click", "right_click"):
            # coord= wins over ocr text
            coord = hints.get("coord")
            if coord:
                xy = (coord[0], coord[1])
            else:
                xy = self._resolve_location(step)

            if xy is None:
                return self._teach(step)

            if action == "double_click":
                pyautogui.doubleClick(*xy)
            elif action == "right_click":
                pyautogui.rightClick(*xy)
            else:
                pyautogui.click(*xy)
            return StepResult(step.index, StepStatus.OK, f"{action} @ {xy}")

        if action in ("scroll_up", "scroll_down"):
            direction = 3 if action == "scroll_up" else -3
            pyautogui.scroll(direction)
            return StepResult(step.index, StepStatus.OK, action)

        return StepResult(step.index, StepStatus.SKIPPED, f"unknown action '{action}'")

    def _resolve_location(self, step: MarkdownStep) -> Optional[tuple[int, int]]:
        """Try OCR text or coord hints to find (x, y)."""
        hints = step.hints
        coord = hints.get("coord")
        if coord:
            return (coord[0], coord[1])

        value = step.value
        if value:
            # Try OCR match
            xy = resolve_ocr(value, confidence=0.65)
            if xy:
                return xy

        return None

    def _teach(self, step: MarkdownStep) -> StepResult:
        """Delegate to human-in-the-loop teach callback."""
        if self.on_teach:
            xy = self.on_teach(step)
            if xy:
                pyautogui.click(*xy)
                return StepResult(step.index, StepStatus.OK,
                                  f"user demonstrated click @ {xy}")
        return StepResult(step.index, StepStatus.TEACH_ME,
                          f"Could not locate '{step.text}'; needs demonstration")

    # ── AI vision fallback ───────────────────────────────────────────────

    def _ai_interpret(self, step: MarkdownStep, script: Script) -> StepResult:
        """
        Ask the LLM what to do for a natural-language step.

        The LLM sees: script body (context) + current step description
        + a screenshot, and returns a structured action hint.
        """
        try:
            import json
            import base64
            import io
            import pyautogui
            from pydantic import BaseModel
            from auto_control.llm_client import run as llm_run

            class AIAction(BaseModel):
                action: str          # click / type / key / wait / scroll_up / scroll_down / skip
                value: Optional[str] = None    # text to type, key name, wait seconds, or OCR text for click
                coord: Optional[list[int]] = None  # [x, y] absolute coordinates if needed

            # Take screenshot
            screenshot = pyautogui.screenshot()
            buf = io.BytesIO()
            screenshot.save(buf, format="PNG")
            b64 = base64.b64encode(buf.getvalue()).decode()

            system_prompt = (
                "You are an RPA execution assistant.\n"
                "You will be given:\n"
                "  1. The full script body (context for what this automation does)\n"
                "  2. The current step description\n"
                "  3. A screenshot of the current screen\n\n"
                "Return a JSON action with:\n"
                "  action: one of click / double_click / right_click / type / key / wait / scroll_up / scroll_down / skip\n"
                "  value:  text to type, key to press (e.g. 'ctrl+s'), seconds to wait, "
                "or visible UI text of element to click\n"
                "  coord:  [x, y] absolute screen coordinates (only if OCR text won't work)\n\n"
                "If the step is purely informational with no UI action, use action='skip'."
            )

            user_content = (
                f"## Script context\n{script.body}\n\n"
                f"## Current step\n{step.text}\n\n"
                "## Screenshot\n"
                f"![screen](data:image/png;base64,{b64})"
            )

            messages: list = [{"role": "user", "content": user_content}]
            raw = llm_run(messages, system_prompt, AIAction)
            data = json.loads(raw)

            ai_action = data.get("action", "skip")
            ai_value  = data.get("value")
            ai_coord  = data.get("coord")

            if ai_action == "skip":
                return StepResult(step.index, StepStatus.SKIPPED, "AI: no action needed")

            # Synthesise a temporary hinted step and re-run through _exec_hinted
            temp_hints = {"action": ai_action, "value": ai_value}
            if ai_coord:
                temp_hints["coord"] = ai_coord

            import copy
            temp_step         = copy.copy(step)
            temp_step.hints   = temp_hints

            # Patch value/action accessors used by _exec_hinted
            temp_step._hints  = temp_hints

            return self._exec_hinted(temp_step)

        except Exception as exc:
            log.debug("AI fallback error: %s\n%s", exc, traceback.format_exc())
            return StepResult(step.index, StepStatus.ERROR,
                              f"AI interpretation failed: {exc}")

    # ── code execution ───────────────────────────────────────────────────

    def _exec_code(self, step: MarkdownStep) -> StepResult:
        try:
            exec(step.code, {"__name__": "__automate__"})  # noqa: S102
            return StepResult(step.index, StepStatus.OK, "code block executed")
        except Exception as exc:
            return StepResult(step.index, StepStatus.ERROR,
                              f"code block error: {exc}")
