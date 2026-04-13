<div align="center"><a name="readme-top"></a>

<img src="./imgs/logo.png" width="120" height="120" alt="autoMate logo">
<h1>autoMate</h1>
<p><b>🤖 AI-Powered Desktop Automation | Let Your Computer Work for You</b></p>

[中文](./README_CN.md) | [日本語](./README_JA.md)

> "Automate the tedious, give time back to life"

https://github.com/user-attachments/assets/bf27f8bd-136b-402e-bc7d-994b99bcc368

</div>

> **Note:** autoMate is in active development. Deeper design thinking, technical discussions, and AI+RPA research notes are shared in [Knowledge Planet "AI Tongmu and His Noble Friends"](https://t.zsxq.com/x1cCW).

<div align="center">
<a href="https://t.zsxq.com/x1cCW" target="_blank" rel="noopener noreferrer">
  <img src="./imgs/knowledge.png" width="150" height="150" alt="Knowledge Planet QR Code">
</a>
</div>

---

## 💡 What is autoMate?

autoMate is an **AI + RPA automation tool** that controls your desktop through natural language. Unlike traditional RPA, it learns from your demonstrations — when it can't find a button, just click it once and it remembers forever.

**Two ways to use it:**

| Mode | Best for |
|------|----------|
| 🔌 **MCP Server** | Claude Desktop, OpenClaw, Cursor, Windsurf — plug in and go |
| 💻 **CLI** | Scripts, terminals, power users |

---

## ✨ Features

- 🔮 **No-Code Automation** — Describe tasks in natural language; AI writes and runs the script
- 🧠 **Human-in-the-Loop Learning** — AI can't find an element? Click it once, it remembers forever
- 📝 **Markdown Scripts** — Stored as readable `.md` files; edit them directly, no rigid JSON schema
- 🌐 **Universal LLM Support** — OpenAI, Azure, OpenRouter, Groq, Ollama, DeepSeek, any OpenAI-compatible API
- 🔌 **MCP Server** — Works with Claude Desktop, OpenClaw, Cursor, Windsurf, Cline and more
- 🖥️ **Cross-Platform** — Windows, macOS, Linux

---

## 🔌 MCP Server Setup

> **Prerequisite:** Install `uv` once — `pip install uv`

### Claude Desktop

Config file:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "automate": {
      "command": "uvx",
      "args": ["automate-mcp"],
      "env": {
        "OPENAI_API_KEY": "sk-...",
        "OPENAI_BASE_URL": "https://api.openai.com/v1",
        "OPENAI_MODEL": "gpt-4o"
      }
    }
  }
}
```

Restart Claude Desktop — you'll see `run_task` and `screenshot` in the tools list.

### OpenClaw

Edit `~/.openclaw/openclaw.json`:

```json
{
  "mcpServers": {
    "automate": {
      "command": "uvx",
      "args": ["automate-mcp"],
      "env": {
        "OPENAI_API_KEY": "sk-...",
        "OPENAI_BASE_URL": "https://api.openai.com/v1",
        "OPENAI_MODEL": "gpt-4o"
      }
    }
  }
}
```

Then restart the gateway:

```bash
openclaw gateway restart
```

### Cursor / Windsurf / Cline

Settings → MCP Servers → Add:

```json
{
  "automate": {
    "command": "uvx",
    "args": ["automate-mcp"],
    "env": {
      "OPENAI_API_KEY": "sk-...",
      "OPENAI_MODEL": "gpt-4o"
    }
  }
}
```

### After connecting

Say in any client:
> *"Use automate to open Chrome and search for the latest AI news"*

### MCP Tools

| Tool | Description |
|------|-------------|
| `run_task` | Execute a desktop automation task in natural language |
| `screenshot` | Capture the screen (or a region) and return as base64 PNG |

---

## 🚀 CLI

### Install

```bash
git clone https://github.com/yuruotong1/autoMate.git
cd autoMate
conda create -n automate python=3.12
conda activate automate
python install.py
```

### Usage

```bash
export OPENAI_API_KEY=sk-...
export OPENAI_MODEL=gpt-4o

# Describe a task — AI generates a Markdown script and executes it
python cli.py run "open Notepad and type Hello World"

# Re-run a saved script
python cli.py exec open_notepad

# List all saved scripts
python cli.py list

# Inspect a script
python cli.py show open_notepad
```

---

## 📝 Markdown Scripts

autoMate saves automation scripts as `.md` files in `~/.automate/scripts/`. Human-readable, version-controllable, and AI-interpretable at runtime.

```markdown
---
name: open_notepad
description: Open Notepad and type a message
---

## Steps

1. Press the Windows key to open Start Menu `[key:win]`
2. Type "notepad" in the search box `[type:notepad]`
3. Click the Notepad result `[click:Notepad]`
4. Type the greeting `[type:Hello, World!]`
5. Save with Ctrl+S `[key:ctrl+s]`

## Notes
Notepad usually opens within 1–2 seconds.

## Code
```python
# Optional: custom Python runs as a step
import time
time.sleep(1)
```
```

### Inline hint syntax

| Hint | Action |
|------|--------|
| `[click:OK]` | Click element whose label contains "OK" (OCR-based) |
| `[click:coord=320,240]` | Click at absolute screen coordinates |
| `[type:hello world]` | Type text |
| `[key:ctrl+s]` | Press keyboard shortcut |
| `[wait:2]` | Wait 2 seconds |
| `[scroll_up]` / `[scroll_down]` | Scroll the page |

Steps **without** hints are interpreted by the AI vision model at runtime.

### Human-in-the-loop learning

When the AI can't locate an element, it pauses and asks:

```
[autoMate] Step 3: 'Click the Submit button'
Please click the target element now…

[autoMate] Got click at (842, 631) — learning…
[autoMate] Learned hint: [click:Submit]  Resuming.
```

The learned hint is automatically written back into the Markdown file — next run needs no human help.

---

## 🌐 Supported LLM Providers

| Provider | Base URL | Example Models |
|----------|----------|----------------|
| [OpenAI](https://platform.openai.com) | `https://api.openai.com/v1` | gpt-4o, gpt-4.1, o3 |
| [Azure OpenAI](https://azure.microsoft.com/products/ai-services/openai-service) | your Azure endpoint | gpt-4o |
| [OpenRouter](https://openrouter.ai) | `https://openrouter.ai/api/v1` | claude-3.7-sonnet, gemini-2.5-pro |
| [DeepSeek](https://platform.deepseek.com) | `https://api.deepseek.com/v1` | deepseek-chat, deepseek-reasoner |
| [Groq](https://console.groq.com) | `https://api.groq.com/openai/v1` | llama-3.3-70b-versatile |
| [Ollama](https://ollama.com) (local) | `http://localhost:11434/v1` | qwen2.5-vl, gemma3-tools:27b |
| [yeka](https://2233.ai/api) (CN proxy) | `https://api.2233.ai/v1` | gpt-4o, o1 |

> **Recommended:** Use a multimodal model with vision — `gpt-4o`, `claude-3.7-sonnet` via OpenRouter, or `qwen2.5-vl` via Ollama.

```bash
export OPENAI_API_KEY=sk-...
export OPENAI_BASE_URL=https://openrouter.ai/api/v1
export OPENAI_MODEL=anthropic/claude-3.7-sonnet
```

---

## 📝 FAQ

**Q: Why is execution slow without a GPU?**  
OmniParser (YOLO-based UI detection) is GPU-intensive. With an NVIDIA GPU (4 GB+ VRAM):

```bash
pip3 uninstall -y torch torchvision
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu124
```

**Q: Can I edit the Markdown scripts manually?**  
Yes — they live in `~/.automate/scripts/*.md`. The AI reads natural-language descriptions at runtime; hints just make execution faster and more reliable.

**Q: Does it work on macOS / Linux?**  
Yes. MCP server and CLI work on all three platforms. The YOLO model requires Python 3.10–3.12.

---

## 🤝 Contributing

Every excellent open-source project embodies collective wisdom. Whether it's fixing bugs, adding features, or improving documentation — your contribution helps thousands of people escape repetitive work.

<a href="https://github.com/yuruotong1/autoMate/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=yuruotong1/autoMate" />
</a>

---

<div align="center">
⭐ Every star encourages the creators and helps more people discover autoMate ⭐
</div>
