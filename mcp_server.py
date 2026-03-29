#!/usr/bin/env python3
"""
autoMate MCP Server

Exposes autoMate's desktop automation capabilities as MCP tools so any
MCP-compatible client — Claude Desktop, Cursor, Windsurf, Cline, etc. —
can control the local desktop through natural language.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Quick setup (Claude Desktop example)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Add the following to ~/Library/Application Support/Claude/claude_desktop_config.json
(macOS) or %APPDATA%\\Claude\\claude_desktop_config.json (Windows):

{
  "mcpServers": {
    "automate": {
      "command": "python",
      "args": ["/absolute/path/to/autoMate/mcp_server.py"],
      "env": {
        "OPENAI_API_KEY": "sk-...",
        "OPENAI_BASE_URL": "https://api.openai.com/v1",
        "OPENAI_MODEL": "gpt-4o"
      }
    }
  }
}

Replace OPENAI_BASE_URL / OPENAI_MODEL to use any OpenAI-compatible provider
(OpenRouter, Groq, Ollama, DeepSeek, Azure OpenAI, etc.).
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Exposed tools
  • run_task   – execute a desktop automation task in natural language
  • screenshot – capture the screen (or a region) and return it as base64 PNG
"""

import base64
import os
from io import BytesIO

from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Server instance
# ---------------------------------------------------------------------------
mcp = FastMCP(
    "automate",
    instructions=(
        "Desktop automation tool powered by autoMate.\n"
        "• Use `run_task` to describe what you want done on the desktop "
        "and autoMate will control the mouse/keyboard autonomously.\n"
        "• Use `screenshot` to see the current state of the screen.\n"
        "Always call `screenshot` first to understand the current screen state "
        "before planning tasks."
    ),
)

# Lazy-loaded vision agent (YOLO model loading is expensive)
_vision_agent = None


def _get_vision_agent():
    global _vision_agent
    if _vision_agent is None:
        from auto_control.agent.vision_agent import VisionAgent
        from util.download_weights import OMNI_PARSER_DIR

        _vision_agent = VisionAgent(
            yolo_model_path=os.path.join(OMNI_PARSER_DIR, "icon_detect", "model.pt")
        )
    return _vision_agent


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@mcp.tool()
def screenshot(screen_region: list[int] | None = None) -> str:
    """
    Capture the current screen and return a base64-encoded PNG image.

    Args:
        screen_region: Optional [x, y, width, height] to capture only a
                       specific region of the screen.

    Returns:
        A data-URI string: "data:image/png;base64,<base64data>"
    """
    from auto_control.tools.screen_capture import get_screenshot

    region = tuple(screen_region) if screen_region else None
    img, _ = get_screenshot(region)

    buf = BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"data:image/png;base64,{b64}"


@mcp.tool()
def run_task(task: str, screen_region: list[int] | None = None) -> str:
    """
    Execute a desktop automation task using natural language.

    autoMate will:
      1. Analyse the current screen with OmniParser (YOLO-based UI detection)
      2. Plan the required steps with an LLM
      3. Execute each step by controlling the mouse and keyboard

    Args:
        task: Natural language description of the task, e.g.
              "Open Chrome and search for the latest AI news"
              "Fill in the form on the screen and click Submit"
        screen_region: Optional [x, y, width, height] to restrict the
                       automation to a specific screen region.

    Returns:
        A status message indicating the task outcome.
    """
    from auto_control.llm_client import configure
    from auto_control.loop import sampling_loop_sync

    # Apply runtime LLM config from environment variables
    configure(
        base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        api_key=os.environ.get("OPENAI_API_KEY", ""),
        model=os.environ.get("OPENAI_MODEL", "gpt-4o"),
    )

    region = tuple(screen_region) if screen_region else None
    vision_agent = _get_vision_agent()
    messages = [{"role": "user", "content": task}]

    for _ in sampling_loop_sync(
        model=os.environ.get("OPENAI_MODEL", "gpt-4o"),
        messages=messages,
        vision_agent=vision_agent,
        screen_region=region,
    ):
        pass  # each yield is one step; the loop ends when next_action == "None"

    return f"✅ Task completed: {task}"


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()
