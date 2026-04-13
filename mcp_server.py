#!/usr/bin/env python3
"""
autoMate MCP Server — Zero-Config Desktop Automation Tools

Exposes low-level desktop control tools (screenshot, click, type, key, scroll)
so that the HOST LLM (Claude, GPT, etc.) handles all reasoning.

No API keys, no environment variables — just plug in and go:

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
import platform
import time
from io import BytesIO

import pyautogui
import pyperclip
from mcp.server.fastmcp import FastMCP

# Safety: move mouse to corner to abort; small pause between actions
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05

# ---------------------------------------------------------------------------
# Server instance
# ---------------------------------------------------------------------------
mcp = FastMCP(
    "automate",
    instructions=(
        "Desktop automation toolkit powered by autoMate.\n"
        "You have direct control over the mouse and keyboard.\n\n"
        "Workflow:\n"
        "1. Call `screenshot` to see the current screen.\n"
        "2. Decide what to do based on what you see.\n"
        "3. Use `click`, `type_text`, `press_key`, `scroll`, or `double_click` to act.\n"
        "4. Call `screenshot` again to verify the result.\n\n"
        "Always screenshot first before acting."
    ),
)


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@mcp.tool()
def screenshot(region: list[int] | None = None) -> str:
    """
    Capture the current screen and return a base64-encoded PNG image.

    Args:
        region: Optional [x, y, width, height] to capture a specific area.

    Returns:
        A data-URI string: "data:image/png;base64,..."
    """
    if region and len(region) == 4:
        img = pyautogui.screenshot(region=tuple(region))
    else:
        img = pyautogui.screenshot()

    buf = BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"data:image/png;base64,{b64}"


@mcp.tool()
def click(x: int, y: int, button: str = "left") -> str:
    """
    Click at screen coordinates.

    Args:
        x: X coordinate.
        y: Y coordinate.
        button: "left", "right", or "middle". Default "left".
    """
    pyautogui.click(x, y, button=button)
    return f"Clicked ({x}, {y}) with {button} button."


@mcp.tool()
def double_click(x: int, y: int) -> str:
    """
    Double-click at screen coordinates.

    Args:
        x: X coordinate.
        y: Y coordinate.
    """
    pyautogui.doubleClick(x, y)
    return f"Double-clicked ({x}, {y})."


@mcp.tool()
def type_text(text: str) -> str:
    """
    Type text at the current cursor position.

    Uses clipboard paste for speed and full Unicode support.

    Args:
        text: The text to type.
    """
    old = pyperclip.paste()
    pyperclip.copy(text)
    if platform.system() == "Darwin":
        pyautogui.hotkey("command", "v")
    else:
        pyautogui.hotkey("ctrl", "v")
    time.sleep(0.05)
    pyperclip.copy(old)
    return f"Typed {len(text)} characters."


@mcp.tool()
def press_key(keys: str) -> str:
    """
    Press a key or key combination.

    Args:
        keys: Key name or combo separated by "+".
              Examples: "enter", "ctrl+c", "ctrl+shift+s", "alt+tab", "win"
    """
    parts = [k.strip() for k in keys.split("+")]
    if len(parts) == 1:
        pyautogui.press(parts[0])
    else:
        pyautogui.hotkey(*parts)
    return f"Pressed {keys}."


@mcp.tool()
def scroll(direction: str = "down", amount: int = 3) -> str:
    """
    Scroll the screen.

    Args:
        direction: "up" or "down". Default "down".
        amount: Number of scroll clicks. Default 3.
    """
    clicks = amount if direction == "up" else -amount
    pyautogui.scroll(clicks)
    return f"Scrolled {direction} by {amount}."


@mcp.tool()
def mouse_move(x: int, y: int) -> str:
    """
    Move the mouse cursor without clicking.

    Args:
        x: X coordinate.
        y: Y coordinate.
    """
    pyautogui.moveTo(x, y)
    return f"Moved cursor to ({x}, {y})."


@mcp.tool()
def drag(start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 0.5) -> str:
    """
    Drag from one position to another.

    Args:
        start_x: Starting X coordinate.
        start_y: Starting Y coordinate.
        end_x: Ending X coordinate.
        end_y: Ending Y coordinate.
        duration: Drag duration in seconds. Default 0.5.
    """
    pyautogui.moveTo(start_x, start_y)
    pyautogui.drag(end_x - start_x, end_y - start_y, duration=duration)
    return f"Dragged from ({start_x}, {start_y}) to ({end_x}, {end_y})."


@mcp.tool()
def get_screen_size() -> str:
    """
    Get the screen resolution.

    Returns:
        Screen width and height.
    """
    w, h = pyautogui.size()
    return f"Screen size: {w} x {h}"


@mcp.tool()
def get_cursor_position() -> str:
    """
    Get the current cursor position.

    Returns:
        Current X and Y coordinates.
    """
    x, y = pyautogui.position()
    return f"Cursor at ({x}, {y})"


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    """
    Console-script entry point.

    Registered as ``automate-mcp`` in pyproject.toml:
      - pip install automate-mcp  -> `automate-mcp` command
      - uvx automate-mcp          -> run without install
    """
    mcp.run()


if __name__ == "__main__":
    main()
