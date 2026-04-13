<div align="center"><a name="readme-top"></a>

<img src="./imgs/logo.png" width="120" height="120" alt="autoMate logo">
<h1>autoMate</h1>
<p><b>🤖 AI-Powered Local Automation Tool | Let Your Computer Work for You</b></p>

[中文](./README_CN.md) | [日本語](./README_JA.md)

>"Automate the tedious, give time back to life"

https://github.com/user-attachments/assets/bf27f8bd-136b-402e-bc7d-994b99bcc368


</div>

> **Special Note:** The autoMate project is still in its early stages of rapid iteration, and we continue to explore and integrate the latest technologies. During this process, **deeper design thinking, technical stack discussions, challenges and solutions encountered, as well as my ongoing research notes on AI+RPA, will be primarily shared and discussed in my [Knowledge Planet "AI Tongmu and His Noble Friends"](https://t.zsxq.com/x1cCW)**.
>
> If you're interested in the technical details behind autoMate, its development direction, or broader AI automation topics, feel free to scan the QR code to join and discuss with me and other friends, witnessing the growth of autoMate together!

<div align="center">
<figure>
    <a href="[Your Knowledge Planet Link]" target="_blank" rel="noopener noreferrer"><img src="./imgs/knowledge.png" width="150" height="150" alt="Knowledge Planet QR Code"></a>
</figure>
</div>


## 💫 Redefining Your Relationship with Computers

Unlike traditional RPA tools that are cumbersome to use, autoMate leverages the power of large language models to complete complex automation processes simply by describing tasks in natural language. Say goodbye to repetitive work and focus on what truly creates value!

**Let automation create more possibilities for your life.**

## 💡 Project Introduction
autoMate is a revolutionary AI+RPA automation tool built on OmniParser that can:

- 📊 Understand your requirements and automatically plan tasks
- 🔍 Intelligently comprehend screen content, simulating human vision and operations
- 🧠 Make autonomous decisions, judging and taking actions based on task requirements
- 💻 Support local deployment, protecting your data security and privacy

## ✨ Features

- 🔮 **No-Code Automation** — Describe tasks in natural language; AI writes and executes the script
- 🧠 **Human-in-the-Loop Learning** — When the AI can't find an element, it asks you to click it once and remembers forever
- 📝 **Markdown Scripts** — Scripts are stored as readable `.md` files you can edit directly; no rigid JSON schema
- 🖥️ **Full Interface Control** — Works on any visual interface, not limited to specific software
- 🌐 **Universal LLM Support** — OpenAI, Azure, OpenRouter, Groq, Ollama, DeepSeek, any OpenAI-compatible API
- 🔌 **MCP Server** — Deploy as an MCP tool for Claude Desktop, Cursor, Windsurf and more
- 💻 **CLI Mode** — Lightweight command-line interface; no browser required

## 🚀 Quick Start

### 📥 Download Binary
Download the pre-built executable from the [GitHub Releases](https://github.com/yuruotong1/autoMate/releases) page — no Python installation needed.

### 📦 Install from Source

```bash
# Clone the project
git clone https://github.com/yuruotong1/autoMate.git
cd autoMate
# Create python3.12 environment
conda create -n "automate" python==3.12
conda activate automate
# Install dependencies
python install.py
```

**Desktop UI (Gradio):**
```bash
python main.py
# Open http://localhost:7888/ in your browser
```

**CLI (lightweight, no browser needed):**
```bash
# Set your LLM credentials
export OPENAI_API_KEY=sk-...
export OPENAI_MODEL=gpt-4o

# Describe a task — AI generates a Markdown script and executes it
python cli.py run "open Notepad and type Hello World"

# List saved scripts
python cli.py list

# Re-run a saved script
python cli.py exec open_notepad

# Inspect a script
python cli.py show open_notepad
```

### 📝 How Markdown Scripts Work

autoMate stores automation scripts as human-readable `.md` files in `~/.automate/scripts/`.
Each step is a natural-language sentence with an optional inline action hint:

```markdown
---
name: open_notepad
description: Open Notepad and type a message
---

## Steps

1. Press the Windows key to open Start Menu `[key:win]`
2. Type "notepad" in the search box `[type:notepad]`
3. Click on the Notepad result `[click:Notepad]`
4. Type the greeting `[type:Hello, World!]`
5. Save with Ctrl+S `[key:ctrl+s]`

## Notes
Notepad usually opens within 1–2 seconds.
```

**Inline hint syntax:**

| Hint | Action |
|------|--------|
| `[click:OK]` | Click element whose label contains "OK" |
| `[click:coord=320,240]` | Click at absolute coordinates |
| `[type:hello world]` | Type text (focus element first if hinted) |
| `[key:ctrl+s]` | Press keyboard shortcut |
| `[wait:2]` | Wait 2 seconds |
| `[scroll_up]` / `[scroll_down]` | Scroll the page |

Steps without hints are interpreted by the AI vision model at runtime.
You can also embed Python code blocks for custom logic.

### 🔔 Note

autoMate supports **any OpenAI-compatible API**. Just set the Base URL, API Key, and Model in Settings:

| Provider | Base URL | Example Models |
| --- | --- | --- |
| [OpenAI](https://platform.openai.com) | `https://api.openai.com/v1` | gpt-4o, gpt-4.1, o3 |
| [Azure OpenAI](https://azure.microsoft.com/products/ai-services/openai-service) | your Azure endpoint | gpt-4o |
| [OpenRouter](https://openrouter.ai) | `https://openrouter.ai/api/v1` | claude-3.7-sonnet, gemini-2.5-pro, etc. |
| [DeepSeek](https://platform.deepseek.com) | `https://api.deepseek.com/v1` | deepseek-chat, deepseek-reasoner |
| [Groq](https://console.groq.com) | `https://api.groq.com/openai/v1` | llama-3.3-70b-versatile |
| [Ollama](https://ollama.com) (local) | `http://localhost:11434/v1` | qwen2.5-vl, gemma3-tools:27b |
| [yeka](https://2233.ai/api) (CN proxy) | `https://api.2233.ai/v1` | gpt-4o, o1 |

> **Recommended**: Use a multimodal model (vision support) for best results — e.g. `gpt-4o`, `claude-3.7-sonnet` via OpenRouter, or `qwen2.5-vl` locally via Ollama.

## 🔌 MCP Server — One-Command Install

autoMate is a **Model Context Protocol (MCP) server**. Any MCP-compatible client —
Claude Desktop, Cursor, Windsurf, Cline, etc. — can call it as a tool to control
your local desktop, with **no git clone or manual setup required**.

### Zero-install setup (recommended)

Just add the following to your MCP client config and restart — `uvx` handles
the download and execution automatically:

**Claude Desktop** → edit `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows** → `%APPDATA%\Claude\claude_desktop_config.json`  
**Cursor / Windsurf** → Settings → MCP Servers

```json
{
  "mcpServers": {
    "automate": {
      "command": "uvx",
      "args": [
        "--from", "git+https://github.com/yuruotong1/autoMate.git",
        "automate-mcp"
      ],
      "env": {
        "OPENAI_API_KEY": "sk-...",
        "OPENAI_BASE_URL": "https://api.openai.com/v1",
        "OPENAI_MODEL": "gpt-4o"
      }
    }
  }
}
```

> **`uvx` not installed?** Run `pip install uv` once, then the config above works.

### Alternative: pip install

```bash
pip install "git+https://github.com/yuruotong1/autoMate.git"
```

Then in your MCP config use `"command": "automate-mcp"` (no `args` needed).

### Use it

After restarting your client, just say:
> "Use automate to open Chrome and search for the latest AI news"

The AI will call `run_task` and autoMate controls the desktop for you.

### Available MCP Tools

| Tool | Description |
| --- | --- |
| `run_task` | Execute a desktop automation task in natural language |
| `screenshot` | Capture the screen (or a region) and return as base64 PNG |

### Environment variables

| Variable | Default | Description |
| --- | --- | --- |
| `OPENAI_API_KEY` | *(required)* | API key for your LLM provider |
| `OPENAI_BASE_URL` | `https://api.openai.com/v1` | Any OpenAI-compatible endpoint |
| `OPENAI_MODEL` | `gpt-4o` | Model name |

## 📝 FAQ
### What models are supported?
autoMate now supports **any OpenAI-compatible API**. The underlying architecture uses a 3-tier fallback (structured output → JSON mode → plain text extraction) to work across different providers.

Recommended: use a **multimodal model with vision capability** (the agent needs to see the screen). OpenAI `gpt-4o`, Claude via OpenRouter, and `qwen2.5-vl` via Ollama are all tested and working.

### Why is my execution speed slow?
If your computer doesn't have an NVIDIA dedicated graphics card, it will run slower because we frequently call OCR for visual annotation, which consumes a lot of GPU resources. We are actively optimizing and adapting. We recommend using an NVIDIA graphics card with at least 4GB of VRAM, and the version should match your torch version:

1. Run `pip list` to check torch version;
2. Check supported cuda version from [official website](https://pytorch.org/get-started/locally/);
3. Uninstall installed torch and torchvision;
4. Copy the official torch installation command and reinstall torch suitable for your cuda version.

For example, if your cuda version is 12.4, you need to install torch using the following command:

```bash
pip3 uninstall -y torch torchvision
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

## 🤝 Join Us

Every excellent open-source project embodies collective wisdom. The growth of autoMate is inseparable from your participation and contribution. Whether it's fixing bugs, adding features, or improving documentation, your every contribution will help thousands of people break free from repetitive work.

Join us in creating a more intelligent future.

<a href="https://github.com/yuruotong1/autoMate/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=yuruotong1/autoMate" />
</a>

---

<div align="center">
⭐ Every Star is an encouragement to the creators and an opportunity for more people to discover and benefit from autoMate ⭐
Your support today is our motivation for tomorrow's progress
</div>
