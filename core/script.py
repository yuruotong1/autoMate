"""
Script data model — Markdown + YAML-frontmatter format.

A Script is stored as a human-readable `.md` file:

    ---
    name: open_notepad
    description: Open Notepad and type a message
    created_at: 2024-01-01T10:00:00
    stability: draft
    total_runs: 0
    success_runs: 0
    ---

    # open_notepad

    Open Notepad on Windows and type a greeting.

    ## Steps

    1. Open Start Menu by pressing the Windows key `[key:win]`
    2. Type "notepad" in the search box `[type:notepad]`
    3. Click on the Notepad application result `[click:Notepad]`
    4. Type the greeting message `[type:Hello, World!]`
    5. Save the file `[key:ctrl+s]`

    ## Notes
    The Notepad window usually opens within 1–2 seconds.

    ## Code
    ```python
    # Optional: custom Python executed as a step
    import time
    time.sleep(1)
    ```

Inline hint syntax (case-insensitive):
  [click:<ocr-text>]       — click element whose visible text matches
  [click:coord=X,Y]        — click at absolute coordinates
  [type:<text>]            — type text (clicks location first if given)
  [key:<keys>]             — press key(s), e.g. ctrl+s, win, enter
  [wait:<seconds>]         — sleep N seconds
  [scroll_up] / [scroll_down]

The AI reads the full body at execution time, so natural-language steps
without hints are also understood — the execution engine falls back to
AI vision-based interpretation.
"""

from __future__ import annotations

import re
import textwrap
from datetime import datetime
from pathlib import Path
from typing import Optional

import yaml


# ---------------------------------------------------------------------------
# Script class
# ---------------------------------------------------------------------------

class Script:
    """
    An autoMate automation script backed by a Markdown file.

    Attributes
    ----------
    name        : machine-friendly identifier (snake_case)
    description : one-sentence summary
    body        : full Markdown text after the frontmatter
    created_at  : ISO timestamp string
    stability   : "draft" | "learning" | "stable"
    total_runs  : total execution attempts
    success_runs: completed runs without errors
    """

    def __init__(
        self,
        name: str,
        body: str = "",
        description: str = "",
        created_at: Optional[str] = None,
        stability: str = "draft",
        total_runs: int = 0,
        success_runs: int = 0,
    ):
        self.name         = name
        self.body         = body
        self.description  = description
        self.created_at   = created_at or datetime.now().isoformat(timespec="seconds")
        self.stability    = stability
        self.total_runs   = total_runs
        self.success_runs = success_runs

    # ── serialisation ────────────────────────────────────────────────────

    def to_markdown(self) -> str:
        """Render the script as a Markdown string with YAML frontmatter."""
        frontmatter = yaml.dump(
            {
                "name":         self.name,
                "description":  self.description,
                "created_at":   self.created_at,
                "stability":    self.stability,
                "total_runs":   self.total_runs,
                "success_runs": self.success_runs,
            },
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
        ).rstrip()
        return f"---\n{frontmatter}\n---\n\n{self.body.strip()}\n"

    def save(self, path: Path | str) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.to_markdown(), encoding="utf-8")

    @classmethod
    def from_markdown(cls, text: str) -> "Script":
        """Parse a Markdown string with optional YAML frontmatter."""
        meta: dict = {}
        body = text

        # Extract --- frontmatter ---
        fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
        if fm_match:
            meta = yaml.safe_load(fm_match.group(1)) or {}
            body = text[fm_match.end():]

        return cls(
            name         = str(meta.get("name", "unnamed")),
            description  = str(meta.get("description", "")),
            body         = body,
            created_at   = str(meta.get("created_at", "")),
            stability    = str(meta.get("stability", "draft")),
            total_runs   = int(meta.get("total_runs", 0)),
            success_runs = int(meta.get("success_runs", 0)),
        )

    @classmethod
    def from_file(cls, path: Path | str) -> "Script":
        return cls.from_markdown(Path(path).read_text(encoding="utf-8"))

    # ── step parsing ─────────────────────────────────────────────────────

    def steps(self) -> list["MarkdownStep"]:
        """
        Extract steps from the ``## Steps`` section of the body.

        Returns a list of MarkdownStep objects.  Each step carries:
          - text : full natural-language description (the list item text)
          - hints: parsed inline action hints, e.g. {"action": "click", "value": "OK"}
          - code : Python source string if the step is a code block
        """
        return _parse_steps(self.body)

    def __repr__(self) -> str:
        return f"Script(name={self.name!r}, steps={len(self.steps())})"


# ---------------------------------------------------------------------------
# MarkdownStep
# ---------------------------------------------------------------------------

class MarkdownStep:
    """A single step extracted from the Markdown body."""

    def __init__(
        self,
        index: int,
        text: str,
        hints: Optional[dict] = None,
        code: Optional[str] = None,
    ):
        self.index = index          # 1-based position
        self.text  = text           # full natural-language line
        self.hints = hints or {}    # {"action": ..., "value": ..., "coord": ...}
        self.code  = code           # Python source (if this is a code block)

    @property
    def is_code(self) -> bool:
        return self.code is not None

    @property
    def action(self) -> Optional[str]:
        return self.hints.get("action")

    @property
    def value(self) -> Optional[str]:
        return self.hints.get("value")

    def __repr__(self) -> str:
        if self.is_code:
            return f"MarkdownStep({self.index}, code)"
        return f"MarkdownStep({self.index}, {self.hints or self.text[:40]!r})"


# ---------------------------------------------------------------------------
# Inline hint parser
# ---------------------------------------------------------------------------

# Matches [action:value], [action:key=val,...], [scroll_up], [scroll_down]
_HINT_RE = re.compile(r"\[([a-z_]+)(?::([^\]]*))?\]", re.IGNORECASE)


def _parse_hint(tag: str, arg: Optional[str]) -> dict:
    """
    Convert a raw ``[tag:arg]`` match into a structured hints dict.

    Examples
    --------
    [click:OK]            -> {action: click, value: OK}
    [click:coord=320,240] -> {action: click, coord: [320, 240]}
    [type:Hello World]    -> {action: type,  value: Hello World}
    [key:ctrl+s]          -> {action: key,   value: ctrl+s}
    [wait:2]              -> {action: wait,  value: 2}
    [scroll_up]           -> {action: scroll_up}
    [scroll_down]         -> {action: scroll_down}
    """
    tag_lower = tag.lower()
    hints: dict = {"action": tag_lower}

    if not arg:
        return hints

    arg = arg.strip()

    # coord=X,Y special case
    coord_m = re.match(r"coord=(\d+)[,\s]+(\d+)", arg, re.IGNORECASE)
    if coord_m:
        hints["coord"] = [int(coord_m.group(1)), int(coord_m.group(2))]
        return hints

    hints["value"] = arg
    return hints


def _parse_steps(body: str) -> list[MarkdownStep]:
    """
    Parse steps from the ## Steps section, plus any ## Code blocks.
    """
    steps: list[MarkdownStep] = []

    # ── 1. Extract the ## Steps section ──────────────────────────────────
    steps_section = ""
    m = re.search(r"^##\s+Steps\s*\n(.*?)(?=\n##\s|\Z)", body, re.IGNORECASE | re.DOTALL | re.MULTILINE)
    if m:
        steps_section = m.group(1)

    step_idx = 1
    for line in steps_section.splitlines():
        line = line.strip()
        # Match numbered list items: "1. text" or "- text"
        item_m = re.match(r"^(?:\d+\.|[-*])\s+(.+)", line)
        if not item_m:
            continue

        text = item_m.group(1).strip()
        hints: dict = {}

        # Extract the LAST inline hint in the line
        for hint_m in _HINT_RE.finditer(text):
            h = _parse_hint(hint_m.group(1), hint_m.group(2))
            if h.get("action"):
                hints = h

        # Remove hint markup from display text
        clean_text = _HINT_RE.sub("", text).strip()

        steps.append(MarkdownStep(index=step_idx, text=clean_text, hints=hints))
        step_idx += 1

    # ── 2. Extract ## Code section(s) ────────────────────────────────────
    for code_m in re.finditer(
        r"^##\s+Code.*?\n```python\s*\n(.*?)```",
        body,
        re.IGNORECASE | re.DOTALL | re.MULTILINE,
    ):
        code = textwrap.dedent(code_m.group(1))
        steps.append(MarkdownStep(index=step_idx, text="[code block]", code=code))
        step_idx += 1

    return steps
