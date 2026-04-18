#!/usr/bin/env python3
"""
autoMate MCP Server — Desktop GUI Automation for Apps Without APIs

Zero-config setup:
{
  "mcpServers": {
    "automate": {
      "command": "uvx",
      "args": ["automate-mcp"]
    }
  }
}
"""

import base64
import json
import logging
import platform
import re
import sys
import time
from datetime import datetime
from io import BytesIO
from pathlib import Path

import pyautogui
import pyperclip
from mcp.server.fastmcp import FastMCP

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05

SCRIPTS_DIR = Path.home() / ".automate" / "scripts"
SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

LOGS_DIR = Path.home() / ".automate" / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("automate.mcp_server")

def _setup_logging():
    if logger.handlers:
        return
    log_file = LOGS_DIR / "mcp_server.log"
    handler = logging.FileHandler(log_file, encoding="utf-8")
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setFormatter(formatter)
    stderr_handler.setLevel(logging.INFO)
    logger.addHandler(stderr_handler)
    logger.info("=== MCP server logging initialized ===")
    logger.info("Log file: %s", log_file)

_setup_logging()

# ---------------------------------------------------------------------------
# Server identity — this is what Claude reads to decide when to use autoMate
# ---------------------------------------------------------------------------
mcp = FastMCP(
    "automate",
    instructions="""
autoMate controls desktop GUI applications that have NO API and NO dedicated MCP server.

WHEN TO USE autoMate:
- Automating desktop apps like 剪映, Photoshop, AutoCAD, WeChat, DingTalk, SAP, WPS, or any internal company tool
- Running saved automation scripts (macros) by name
- Recording a new reusable automation workflow
- Any task where the target is a desktop window with buttons, menus, or forms

WHEN NOT TO USE autoMate (use a dedicated MCP instead):
- File/folder operations → use filesystem MCP
- Windows system settings → use Windows MCP
- Web browsing / web scraping → use browser MCP
- Git operations → use git MCP

TYPICAL WORKFLOW:
1. Call `screenshot` to see the current screen
2. Call `run_script` if a saved script exists for this task
3. Otherwise use `click`, `type_text`, `press_key`, `scroll` to interact step by step
4. Call `save_script` to save the workflow for future reuse

CLOUD VISION WORKFLOW (optional — requires env vars):
1. Call `warm_endpoints` to wake up scaled-to-zero HF endpoints
2. Call `parse_screen` to detect all UI elements (icons, text, buttons) via OmniParser
3. Call `reason_action` to let a vision-language model decide the next action
4. Or call `smart_act` for the full autonomous loop: parse → reason → execute

autoMate is the ONLY tool that can automate desktop GUI apps with no API.
""",
)


# ---------------------------------------------------------------------------
# Script helpers
# ---------------------------------------------------------------------------

def _script_path(name: str) -> Path:
    safe = re.sub(r"[^\w\-]", "_", name.strip())
    return SCRIPTS_DIR / f"{safe}.md"


def _load_script(name: str) -> str | None:
    p = _script_path(name)
    return p.read_text(encoding="utf-8") if p.exists() else None


# ---------------------------------------------------------------------------
# Screen tools
# ---------------------------------------------------------------------------

@mcp.tool()
def screenshot(region: list[int] | None = None) -> str:
    """
    Capture the current screen and return a base64-encoded PNG.

    Use this FIRST before any interaction to understand what is on screen.

    Args:
        region: Optional [x, y, width, height] to capture a specific area.

    Returns:
        Data-URI string: "data:image/png;base64,..."
    """
    if region and len(region) == 4:
        img = pyautogui.screenshot(region=tuple(region))
    else:
        img = pyautogui.screenshot()
    buf = BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"data:image/png;base64,{b64}"


# ---------------------------------------------------------------------------
# Mouse tools
# ---------------------------------------------------------------------------

@mcp.tool()
def click(x: int, y: int, button: str = "left") -> str:
    """
    Click at screen coordinates.

    Args:
        x: X coordinate.
        y: Y coordinate.
        button: "left" (default), "right", or "middle".
    """
    pyautogui.click(x, y, button=button)
    return f"Clicked ({x}, {y}) [{button}]"


@mcp.tool()
def double_click(x: int, y: int) -> str:
    """Double-click at screen coordinates."""
    pyautogui.doubleClick(x, y)
    return f"Double-clicked ({x}, {y})"


@mcp.tool()
def mouse_move(x: int, y: int) -> str:
    """Move the mouse cursor without clicking."""
    pyautogui.moveTo(x, y)
    return f"Cursor moved to ({x}, {y})"


@mcp.tool()
def drag(start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 0.5) -> str:
    """Drag from one screen position to another."""
    pyautogui.moveTo(start_x, start_y)
    pyautogui.drag(end_x - start_x, end_y - start_y, duration=duration)
    return f"Dragged ({start_x},{start_y}) → ({end_x},{end_y})"


@mcp.tool()
def scroll(direction: str = "down", amount: int = 3) -> str:
    """
    Scroll the screen.

    Args:
        direction: "up" or "down".
        amount: Scroll clicks (default 3).
    """
    pyautogui.scroll(amount if direction == "up" else -amount)
    return f"Scrolled {direction} ×{amount}"


# ---------------------------------------------------------------------------
# Keyboard tools
# ---------------------------------------------------------------------------

@mcp.tool()
def type_text(text: str) -> str:
    """
    Type text at the current cursor position.

    Uses clipboard paste for speed and full Unicode/CJK support.

    Args:
        text: The text to type.
    """
    old = pyperclip.paste()
    pyperclip.copy(text)
    pyautogui.hotkey("command" if platform.system() == "Darwin" else "ctrl", "v")
    time.sleep(0.05)
    pyperclip.copy(old)
    return f"Typed {len(text)} characters"


@mcp.tool()
def press_key(keys: str) -> str:
    """
    Press a key or key combination.

    Args:
        keys: Single key or combo joined by "+".
              Examples: "enter", "ctrl+c", "ctrl+shift+s", "alt+tab", "win"
    """
    parts = [k.strip() for k in keys.split("+")]
    if len(parts) == 1:
        pyautogui.press(parts[0])
    else:
        pyautogui.hotkey(*parts)
    return f"Pressed [{keys}]"


# ---------------------------------------------------------------------------
# Screen info tools
# ---------------------------------------------------------------------------

@mcp.tool()
def get_screen_size() -> str:
    """Return the screen resolution."""
    w, h = pyautogui.size()
    return f"{w}x{h}"


@mcp.tool()
def get_cursor_position() -> str:
    """Return the current cursor coordinates."""
    x, y = pyautogui.position()
    return f"({x}, {y})"


# ---------------------------------------------------------------------------
# Script / action library tools
# ---------------------------------------------------------------------------

@mcp.tool()
def list_scripts() -> str:
    """
    List all saved automation scripts.

    Returns a summary of available scripts that can be run with run_script.
    """
    files = sorted(SCRIPTS_DIR.glob("*.md"))
    if not files:
        return "No saved scripts yet. Use save_script to create one."

    lines = [f"Found {len(files)} script(s) in {SCRIPTS_DIR}:\n"]
    for f in files:
        content = f.read_text(encoding="utf-8")
        # Extract description from frontmatter
        desc = ""
        m = re.search(r"^description:\s*(.+)$", content, re.MULTILINE)
        if m:
            desc = m.group(1).strip()
        lines.append(f"  • {f.stem}" + (f" — {desc}" if desc else ""))
    return "\n".join(lines)


@mcp.tool()
def run_script(name: str) -> str:
    """
    Run a saved automation script by name.

    This is the primary way to execute reusable automation workflows.
    Use list_scripts first to see what's available.

    Args:
        name: Script name (without .md extension).
    """
    content = _load_script(name)
    if content is None:
        available = [f.stem for f in SCRIPTS_DIR.glob("*.md")]
        hint = f" Available: {', '.join(available)}" if available else " No scripts saved yet."
        return f"Script '{name}' not found.{hint}"

    # Parse and execute steps from ## Steps section
    steps_match = re.search(r"##\s+Steps\s*\n(.*?)(?=\n##|\Z)", content, re.DOTALL)
    if not steps_match:
        return f"Script '{name}' has no ## Steps section."

    steps_text = steps_match.group(1).strip()
    results = []

    for line in steps_text.splitlines():
        line = line.strip()
        if not line or not re.match(r"^\d+\.", line):
            continue

        # Extract hints from the step line
        hints = re.findall(r"\[([a-z_]+):([^\]]*)\]", line, re.IGNORECASE)

        if not hints:
            results.append(f"⚠ Step needs manual execution: {line}")
            continue

        for action, value in hints:
            action = action.lower()
            try:
                if action == "click":
                    if value.startswith("coord="):
                        xy = value[6:].split(",")
                        pyautogui.click(int(xy[0]), int(xy[1]))
                        results.append(f"✓ click coord ({xy[0]},{xy[1]})")
                    else:
                        results.append(f"⚠ OCR click '{value}' — needs vision model")
                elif action == "type":
                    old = pyperclip.paste()
                    pyperclip.copy(value)
                    pyautogui.hotkey("command" if platform.system() == "Darwin" else "ctrl", "v")
                    time.sleep(0.05)
                    pyperclip.copy(old)
                    results.append(f"✓ type '{value[:20]}{'...' if len(value) > 20 else ''}'")
                elif action == "key":
                    parts = [k.strip() for k in value.split("+")]
                    if len(parts) == 1:
                        pyautogui.press(parts[0])
                    else:
                        pyautogui.hotkey(*parts)
                    results.append(f"✓ key [{value}]")
                elif action == "wait":
                    time.sleep(float(value or "1"))
                    results.append(f"✓ wait {value}s")
                elif action in ("scroll_up", "scroll_down"):
                    pyautogui.scroll(3 if action == "scroll_up" else -3)
                    results.append(f"✓ {action}")
            except Exception as e:
                results.append(f"✗ {action} failed: {e}")

    return f"Script '{name}' executed:\n" + "\n".join(results)


@mcp.tool()
def save_script(name: str, description: str, steps: str) -> str:
    """
    Save an automation workflow as a reusable script.

    Call this after successfully completing a task to save it for future reuse.
    Saved scripts can be shared with others and run with run_script.

    Args:
        name: Short identifier, e.g. "export_jianying_douyin"
        description: One-line description of what the script does.
        steps: The steps in Markdown format. Each step on a new line starting
               with a number. Add hints like [click:coord=x,y], [type:text],
               [key:ctrl+s], [wait:2] to make steps executable.
               Example:
                 1. Open export dialog [key:ctrl+e]
                 2. Set resolution to 1080p [click:coord=320,480]
                 3. Click export button [click:coord=800,600]
    """
    content = f"""---
name: {name}
description: {description}
created: {datetime.now().strftime("%Y-%m-%d")}
---

## Steps

{steps.strip()}
"""
    path = _script_path(name)
    path.write_text(content, encoding="utf-8")
    return f"Saved script '{name}' → {path}"


@mcp.tool()
def show_script(name: str) -> str:
    """
    Show the contents of a saved script.

    Args:
        name: Script name (without .md extension).
    """
    content = _load_script(name)
    if content is None:
        return f"Script '{name}' not found."
    return content


@mcp.tool()
def delete_script(name: str) -> str:
    """
    Delete a saved script.

    Args:
        name: Script name (without .md extension).
    """
    path = _script_path(name)
    if not path.exists():
        return f"Script '{name}' not found."
    path.unlink()
    return f"Deleted script '{name}'"


@mcp.tool()
def install_script(url: str) -> str:
    """
    Install a script from a URL (GitHub raw link or automate-actions library).

    Args:
        url: Direct URL to a .md script file.
             Community library: https://github.com/yuruotong1/automate-actions
    """
    import urllib.request
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            content = resp.read().decode("utf-8")
    except Exception as e:
        return f"Failed to fetch script: {e}"

    # Extract name from frontmatter
    m = re.search(r"^name:\s*(.+)$", content, re.MULTILINE)
    if not m:
        return "Invalid script: missing 'name' in frontmatter."

    name = re.sub(r"[^\w\-]", "_", m.group(1).strip())
    path = _script_path(name)
    path.write_text(content, encoding="utf-8")
    return f"Installed script '{name}' → {path}"


# ---------------------------------------------------------------------------
# Cloud vision tools (optional — requires AUTOMATE_* env vars)
# ---------------------------------------------------------------------------

def _cloud_vision_available() -> bool:
    try:
        import cloud_vision
        return cloud_vision.is_configured()
    except ImportError:
        return False


@mcp.tool()
def cloud_vision_config() -> str:
    """
    Show current cloud vision configuration.

    Cloud vision enables screen parsing (OmniParser) and action reasoning
    (UI-TARS / Qwen-VL) via HuggingFace Inference Endpoints — zero local GPU.

    Returns configuration status and env var hints if not configured.
    """
    logger.info("MCP tool called: cloud_vision_config")
    try:
        import cloud_vision
    except ImportError:
        logger.error("cloud_vision_config: cloud_vision module not available")
        return (
            "cloud_vision module not available. "
            "Ensure cloud_vision.py is in the same directory as mcp_server.py."
        )

    if not cloud_vision.is_configured():
        logger.warning("cloud_vision_config: not configured")
        return (
            "Cloud vision not configured. Set these env vars:\n"
            "  AUTOMATE_HF_TOKEN              — HuggingFace API token\n"
            "  AUTOMATE_SCREEN_PARSER_URL      — OmniParser endpoint URL\n"
            "  AUTOMATE_ACTION_MODEL_URL       — Vision-language model endpoint URL\n"
            "  AUTOMATE_ACTION_MODEL_NAME      — Model name (e.g. repo id)\n"
            "  AUTOMATE_HF_NAMESPACE           — HF namespace for endpoint management\n"
            "  AUTOMATE_SCREEN_PARSER_ENDPOINT — Endpoint name for warmup\n"
            "  AUTOMATE_ACTION_MODEL_ENDPOINT  — Endpoint name for warmup\n"
            "\nSee .env.example for details."
        )

    summary = cloud_vision.get_config_summary()
    logger.info("cloud_vision_config: configured, summary=%s", json.dumps(summary))
    return json.dumps(summary, indent=2)


@mcp.tool()
def warm_endpoints(timeout_seconds: int = 600) -> str:
    """
    Wake up scaled-to-zero HuggingFace Inference Endpoints and wait until ready.

    Call this BEFORE using parse_screen or reason_action if endpoints may
    have scaled to zero (default: 15 min idle). Warmup takes 1-5 minutes.

    Requires AUTOMATE_HF_NAMESPACE and endpoint name env vars.

    Args:
        timeout_seconds: Max seconds to wait for endpoints (default 600).
    """
    logger.info("MCP tool called: warm_endpoints (timeout=%s)", timeout_seconds)
    try:
        import cloud_vision
    except ImportError:
        logger.error("warm_endpoints: cloud_vision module not available")
        return "cloud_vision module not available."

    result = cloud_vision.warm_endpoints(timeout_seconds=timeout_seconds)
    logger.info("warm_endpoints: result=%s", json.dumps(result))
    return json.dumps(result, indent=2)


@mcp.tool()
def parse_screen(
    region: list[int] | None = None,
    bbox_threshold: float = 0.05,
    iou_threshold: float = 0.7,
) -> str:
    """
    Detect all UI elements on screen using a cloud screen parser (OmniParser-compatible).

    Captures a screenshot and sends it to the configured endpoint for
    YOLO icon detection, Florence-2 captioning, and EasyOCR text extraction.
    Returns bounding boxes with pixel coordinates, element types, and labels.

    Requires AUTOMATE_SCREEN_PARSER_URL to be set.

    Args:
        region: Optional [x, y, width, height] to capture a sub-region.
        bbox_threshold: Confidence threshold for detection (default 0.05).
        iou_threshold: IoU threshold for NMS (default 0.7).
    """
    logger.info("MCP tool called: parse_screen region=%s bbox_threshold=%s iou_threshold=%s", region, bbox_threshold, iou_threshold)
    try:
        import cloud_vision
    except ImportError:
        logger.error("parse_screen: cloud_vision module not available")
        return "cloud_vision module not available."

    try:
        result = cloud_vision.parse_screen(
            region=region,
            bbox_threshold=bbox_threshold,
            iou_threshold=iou_threshold,
        )
        elements = result["elements"]
        logger.info("parse_screen: SUCCESS, %d elements found", len(elements))
        lines = [f"Found {len(elements)} UI elements (screen {result['screen_size']['w']}x{result['screen_size']['h']}):\n"]
        for el in elements:
            inter = " [interactive]" if el.get("interactivity") else ""
            lines.append(
                f"  [{el['id']:3d}] {el['type']:4s} | center ({el['center'][0]:4d}, {el['center'][1]:4d}) "
                f"| bbox {el['bbox_px']}{inter} | \"{el.get('content', '')}\""
            )
        return "\n".join(lines)
    except Exception as e:
        logger.error("parse_screen: FAILED with error: %s", e)
        return f"parse_screen error: {e}"


@mcp.tool()
def reason_action(
    task: str,
    use_parser: bool = True,
    region: list[int] | None = None,
    max_tokens: int = 512,
) -> str:
    """
    Ask a cloud vision-language model what GUI action to take next.

    Sends a screenshot (and optionally parsed UI elements) to the action model
    endpoint for reasoning about what to click, type, or press.

    Requires AUTOMATE_ACTION_MODEL_URL to be set.

    Args:
        task: Natural language description of what to accomplish.
        use_parser: If True (default), first parse_screen to provide element context.
        region: Optional [x, y, width, height] to capture a sub-region.
        max_tokens: Maximum tokens for the model response (default 512).
    """
    logger.info("MCP tool called: reason_action task='%s' use_parser=%s region=%s max_tokens=%d", task[:50], use_parser, region, max_tokens)
    try:
        import cloud_vision
    except ImportError:
        logger.error("reason_action: cloud_vision module not available")
        return "cloud_vision module not available."

    try:
        elements = None
        if use_parser and cloud_vision._get_screen_parser_url():
            try:
                logger.debug("reason_action: parsing screen first...")
                parsed = cloud_vision.parse_screen(region=region)
                elements = parsed["elements"]
                logger.debug("reason_action: parsed %d elements", len(elements))
            except Exception as e:
                logger.warning("reason_action: parse_screen failed, continuing without elements: %s", e)
                elements = None

        result = cloud_vision.reason_action(
            task=task, elements=elements, region=region, max_tokens=max_tokens,
        )
        logger.info("reason_action: SUCCESS, model=%s reasoning_len=%d", result['model'], len(result['reasoning']))
        return f"Model: {result['model']}\n\n{result['reasoning']}"
    except Exception as e:
        logger.error("reason_action: FAILED with error: %s", e)
        return f"reason_action error: {e}"


@mcp.tool()
def smart_act(
    task: str,
    max_steps: int = 10,
    step_delay: float = 1.0,
) -> str:
    """
    Full autonomous loop: parse screen → reason action → execute → repeat.

    Combines cloud screen parsing, vision-language model reasoning, and
    local action execution. Repeats until the model says done() or max_steps.

    Requires both AUTOMATE_SCREEN_PARSER_URL and AUTOMATE_ACTION_MODEL_URL.

    Args:
        task: What to accomplish (natural language).
        max_steps: Safety limit on iterations (default 10).
        step_delay: Seconds between steps for UI to settle (default 1.0).
    """
    logger.info("MCP tool called: smart_act task='%s' max_steps=%d step_delay=%.1f", task[:50], max_steps, step_delay)
    try:
        import cloud_vision
    except ImportError:
        logger.error("smart_act: cloud_vision module not available")
        return "cloud_vision module not available."

    try:
        steps = cloud_vision.smart_act(
            task=task, max_steps=max_steps, step_delay=step_delay,
        )
        logger.info("smart_act: SUCCESS, %d steps completed", len(steps))
        lines = [f"Completed {len(steps)} step(s):\n"]
        for s in steps:
            lines.append(
                f"  Step {s['step']}: {s['action_taken']} "
                f"({s['elements_found']} elements detected)"
            )
        return "\n".join(lines)
    except Exception as e:
        logger.error("smart_act: FAILED with error: %s", e)
        return f"smart_act error: {e}"


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    mcp.run()


if __name__ == "__main__":
    main()
