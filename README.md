<div align="center"><a name="readme-top"></a>

<img src="./imgs/logo.png" width="120" height="120" alt="autoMate logo">
<h1>autoMate</h1>
<p><b>🤖 Desktop Automation for Apps Without APIs</b></p>

[中文](./README_CN.md) | [日本語](./README_JA.md)

[![PyPI](https://img.shields.io/pypi/v/automate-mcp)](https://pypi.org/project/automate-mcp/)
[![License](https://img.shields.io/github/license/yuruotong1/autoMate)](LICENSE)

> Give Claude hands and eyes — automate any desktop app, even if it has no API

https://github.com/user-attachments/assets/bf27f8bd-136b-402e-bc7d-994b99bcc368

</div>

---

## 💡 What is autoMate?

autoMate is an MCP server that gives AI assistants (Claude, GPT, etc.) the ability to **control any desktop application** — even apps with no API, no plugin system, and no automation support.

Think of it as the cross-platform, AI-native alternative to [Quicker](https://www.getquicker.net) — but instead of building workflows by dragging blocks, you just describe what you want.

**What makes it different from filesystem / browser / Windows MCP:**

| MCP Server | What it automates |
|------------|------------------|
| filesystem MCP | Files and folders |
| browser MCP | Web pages |
| Windows MCP | OS settings and system calls |
| **autoMate** | **Any desktop GUI app with no API** — 剪映, Photoshop, AutoCAD, WeChat, SAP, internal tools… |

---

## ✨ Features

- 🖥️ **Automates apps with no API** — if it has a GUI, autoMate can drive it
- 📚 **Reusable script library** — save workflows once, run forever; install community scripts in one command
- 🧠 **Claude knows when to use it** — clear identity prevents autoMate from being bypassed by other MCPs
- 🤖 **Zero config** — no API keys, no env vars; the host LLM does the thinking
- 🌍 **Cross-platform** — Windows, macOS, Linux (Quicker is Windows-only)

---

## 🔌 Setup

> **Prerequisite:** `pip install uv`

### Claude Desktop

Open **Settings → Developer → Edit Config**, then add:

```json
{
  "mcpServers": {
    "automate": {
      "command": "uvx",
      "args": ["automate-mcp@latest"]
    }
  }
}
```

Restart Claude Desktop — done. autoMate auto-updates every restart.

### OpenClaw

Edit `~/.openclaw/openclaw.json`:

```json
{
  "mcpServers": {
    "automate": {
      "command": "uvx",
      "args": ["automate-mcp@latest"]
    }
  }
}
```

```bash
openclaw gateway restart
```

### Cursor / Windsurf / Cline

Settings → MCP Servers → Add:

```json
{
  "automate": {
    "command": "uvx",
    "args": ["automate-mcp@latest"]
  }
}
```

---

## 🛠️ MCP Tools

**Script library** — the core value: save a workflow once, run it forever.

| Tool | Description |
|------|-------------|
| `list_scripts` | Show all saved automation scripts |
| `run_script` | Run a saved script by name |
| `save_script` | Save the current workflow as a reusable script |
| `show_script` | View a script's contents |
| `delete_script` | Delete a script |
| `install_script` | Install a script from a URL or the community library |

**Low-level desktop control** — used by Claude when building or executing scripts.

| Tool | Description |
|------|-------------|
| `screenshot` | Capture the screen and return as base64 PNG |
| `click` | Click at screen coordinates |
| `double_click` | Double-click at screen coordinates |
| `type_text` | Type text (full Unicode / CJK support) |
| `press_key` | Press a key or combo (e.g. `ctrl+c`, `win`) |
| `scroll` | Scroll up or down |
| `mouse_move` | Move cursor without clicking |
| `drag` | Drag from one position to another |

---

## 📚 Script Library

Scripts are saved as `.md` files in `~/.automate/scripts/` — human-readable, git-friendly, shareable.

**Example script:**

```markdown
---
name: jianying_export_douyin
description: Export the current 剪映 project as a 9:16 Douyin video
created: 2025-01-01
---

## Steps

1. Open export dialog [key:ctrl+e]
2. Select resolution 1080×1920 [click:coord=320,480]
3. Set format to MP4 [click:coord=320,560]
4. Click export [click:coord=800,650]
5. Wait for export to finish [wait:5]
```

**Inline hint syntax:**

| Hint | Action |
|------|--------|
| `[click:coord=320,240]` | Click at absolute screen coordinates |
| `[type:hello]` | Type text |
| `[key:ctrl+s]` | Press keyboard shortcut |
| `[wait:2]` | Wait 2 seconds |
| `[scroll_up]` / `[scroll_down]` | Scroll the page |

Steps without hints are interpreted by the AI vision model at runtime.

**Install a community script:**

```
Tell Claude: "install the automate script from <url>"
```

or Claude calls `install_script` directly with a raw GitHub URL.

---

## 📝 FAQ

**Q: How is this different from just using Claude's computer-use capability?**  
autoMate provides persistent, reusable scripts. Once you automate a task, it's saved and runs instantly next time — no re-reasoning required.

**Q: Why does Claude sometimes use Windows MCP / filesystem MCP instead of autoMate?**  
Update to v0.4.0+ — the server description now explicitly tells Claude when to use autoMate vs other MCPs.

**Q: Does it work with apps that change their UI frequently?**  
Coordinate-based hints (`[click:coord=x,y]`) are fragile to UI changes. For resilient scripts, describe the step in natural language and let Claude re-locate the element each run.

**Q: Does it work on macOS / Linux?**  
Yes — all three platforms. This is the main advantage over Quicker (Windows-only).

---

## 🤝 Contributing

<a href="https://github.com/yuruotong1/autoMate/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=yuruotong1/autoMate" />
</a>

---

<div align="center">
⭐ Every star encourages the creators and helps more people discover autoMate ⭐
</div>
