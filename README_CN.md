<div align="center"><a name="readme-top"></a>

<img src="./imgs/logo.png" width="120" height="120" alt="autoMate logo">
<h1>autoMate</h1>
<p><b>🤖 AI 驱动的桌面自动化工具 | 让电脑自己会干活</b></p>

[English](./README.md) | [日本語](./README_JA.md)

[![PyPI](https://img.shields.io/pypi/v/automate-mcp)](https://pypi.org/project/automate-mcp/)
[![License](https://img.shields.io/github/license/yuruotong1/autoMate)](LICENSE)

> "让繁琐自动化，把时间还给生活"

https://github.com/user-attachments/assets/bf27f8bd-136b-402e-bc7d-994b99bcc368

</div>

> **特别声明：** autoMate 项目仍处于快速迭代阶段。更深入的设计思考、技术选型讨论、挑战与解决方案，以及 AI+RPA 领域的研究笔记，会主要在 [知识星球「AI桐木和他的贵人们」](https://t.zsxq.com/x1cCW) 中分享。

<div align="center">
<a href="https://t.zsxq.com/x1cCW" target="_blank" rel="noopener noreferrer">
  <img src="./imgs/knowledge.png" width="150" height="150" alt="知识星球二维码">
</a>
</div>

---

## 💡 autoMate 是什么？

autoMate 是一款 **AI + RPA 桌面自动化工具**，通过自然语言控制你的电脑。和传统 RPA 不同，它支持从你的示范中学习——当它找不到某个按钮时，你只需点击一次，它就会永远记住。

**两种使用方式：**

| 模式 | 适合场景 |
|------|---------|
| 🔌 **MCP Server** | Claude Desktop、OpenClaw、Cursor、Windsurf，接入即用 |
| 💻 **CLI 命令行** | 脚本、终端、进阶用户 |

---

## ✨ 功能特点

- 🖥️ **专为无 API 的桌面软件而生** — 剪映、Photoshop、AutoCAD、微信、SAP、公司内部系统，有界面就能自动化
- 📚 **可复用脚本库** — 工作流保存为 Markdown 脚本，一行命令安装社区脚本，分享给所有人用
- 🔌 **MCP Server，有明确的使用边界** — Claude 知道什么时候该用 autoMate，不会被 filesystem/Windows MCP 替代
- 🤖 **零配置** — 不需要 API Key，不需要环境变量，宿主大模型负责思考
- 🖱️ **完整桌面控制** — 截图、点击、输入、按键、滚动、拖拽
- 🌍 **跨平台** — Windows、macOS、Linux（Quicker 只支持 Windows）

---

## 🔌 MCP Server 接入

> **前提：** 安装一次 `uv` — `pip install uv`

**零配置** — 不需要 API Key，不需要环境变量。宿主大模型（Claude、GPT 等）负责思考，autoMate 只提供手和眼睛。

### Claude Desktop

打开 Claude Desktop → **Settings → Developer → Edit Config** 即可直接定位并编辑配置文件。

> 默认路径参考：
> - macOS：`~/Library/Application Support/Claude/claude_desktop_config.json`
> - Windows：`%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "automate": {
      "command": "uvx",
      "args": ["automate-mcp"]
    }
  }
}
```

重启 Claude Desktop，搞定！

### OpenClaw（小龙虾）

编辑 `~/.openclaw/openclaw.json`：

```json
{
  "mcpServers": {
    "automate": {
      "command": "uvx",
      "args": ["automate-mcp"]
    }
  }
}
```

然后重启网关：

```bash
openclaw gateway restart
```

### Cursor / Windsurf / Cline

设置 → MCP Servers → 添加：

```json
{
  "automate": {
    "command": "uvx",
    "args": ["automate-mcp"]
  }
}
```

### 接入后使用

在任意客户端直接说：
> *"用 automate 打开 Chrome，搜索最新的 AI 新闻"*

### MCP 工具列表

**脚本库**（核心功能——保存一次，永久复用）：

| 工具 | 说明 |
|------|------|
| `list_scripts` | 查看所有已保存的自动化脚本 |
| `run_script` | 按名称执行已保存的脚本 |
| `save_script` | 将当前工作流保存为可复用脚本 |
| `show_script` | 查看脚本内容 |
| `delete_script` | 删除脚本 |
| `install_script` | 从 URL 或社区动作库安装脚本 |

**底层桌面控制**（构建新脚本时使用）：

| 工具 | 说明 |
|------|------|
| `screenshot` | 截取屏幕，返回 base64 PNG |
| `click` | 点击屏幕坐标 |
| `double_click` | 双击屏幕坐标 |
| `type_text` | 输入文字（支持中文及全 Unicode） |
| `press_key` | 按键或组合键（如 `ctrl+c`、`win`） |
| `scroll` | 上下滚动 |
| `mouse_move` | 移动鼠标（不点击） |
| `drag` | 从一个位置拖拽到另一个位置 |

---

## 🚀 CLI 命令行

### 安装

```bash
git clone https://github.com/yuruotong1/autoMate.git
cd autoMate
conda create -n automate python=3.12
conda activate automate
python install.py
```

### 使用

```bash
export OPENAI_API_KEY=sk-...
export OPENAI_MODEL=gpt-4o

# 描述任务 — AI 生成 Markdown 脚本并执行
python cli.py run "打开记事本，输入 Hello World"

# 重新执行已保存的脚本
python cli.py exec open_notepad

# 查看所有已保存的脚本
python cli.py list

# 查看脚本内容
python cli.py show open_notepad
```

---

## 📝 Markdown 脚本格式

autoMate 将脚本保存为 `~/.automate/scripts/` 目录下的 `.md` 文件，人类可读、可用 Git 管理，运行时 AI 可直接解读。

```markdown
---
name: open_notepad
description: 打开记事本并输入消息
---

## Steps

1. 按 Windows 键打开开始菜单 `[key:win]`
2. 在搜索框中输入 notepad `[type:notepad]`
3. 点击记事本应用 `[click:Notepad]`
4. 输入问候语 `[type:Hello, World!]`
5. 用 Ctrl+S 保存 `[key:ctrl+s]`

## Notes
记事本通常 1–2 秒内打开。

## Code
```python
# 可选：自定义 Python 代码作为步骤执行
import time
time.sleep(1)
```
```

### 内联提示语法

| 提示 | 操作 |
|------|------|
| `[click:确认]` | 点击标签含"确认"的元素（基于 OCR） |
| `[click:coord=320,240]` | 点击绝对屏幕坐标 |
| `[type:文本内容]` | 输入文字 |
| `[key:ctrl+s]` | 按快捷键 |
| `[wait:2]` | 等待 2 秒 |
| `[scroll_up]` / `[scroll_down]` | 滚动页面 |

**没有提示**的步骤，由 AI 视觉模型在运行时自动解读。

### 人机协同学习

当 AI 找不到某个元素时，它会暂停并提示：

```
[autoMate] Step 3: '点击提交按钮'
请点击目标元素…

[autoMate] 检测到点击坐标 (842, 631) — 正在学习…
[autoMate] 已学习提示: [click:提交]  继续执行。
```

学到的提示会自动写回 Markdown 文件——下次运行无需再次询问。

---

## 🌐 支持的 LLM 提供商

| 平台 | Base URL | 示例模型 |
|------|----------|---------|
| [OpenAI](https://platform.openai.com) | `https://api.openai.com/v1` | gpt-4o, gpt-4.1, o3 |
| [Azure OpenAI](https://azure.microsoft.com/products/ai-services/openai-service) | 你的 Azure 端点 | gpt-4o |
| [OpenRouter](https://openrouter.ai) | `https://openrouter.ai/api/v1` | claude-3.7-sonnet, gemini-2.5-pro |
| [DeepSeek](https://platform.deepseek.com) | `https://api.deepseek.com/v1` | deepseek-chat, deepseek-reasoner |
| [Groq](https://console.groq.com) | `https://api.groq.com/openai/v1` | llama-3.3-70b-versatile |
| [Ollama](https://ollama.com)（本地） | `http://localhost:11434/v1` | qwen2.5-vl, gemma3-tools:27b |
| [yeka](https://2233.ai/api)（国内代理） | `https://api.2233.ai/v1` | gpt-4o, o1 |

> **推荐**：使用支持视觉的多模态模型，如 `gpt-4o`、通过 OpenRouter 的 `claude-3.7-sonnet`，或 Ollama 本地运行的 `qwen2.5-vl`。

```bash
export OPENAI_API_KEY=sk-...
export OPENAI_BASE_URL=https://openrouter.ai/api/v1
export OPENAI_MODEL=anthropic/claude-3.7-sonnet
```

---

## 📝 常见问题

**Q：没有 GPU 运行为什么很慢？**  
OmniParser（基于 YOLO 的 UI 检测）需要 GPU。有 NVIDIA 显卡（4GB+ 显存）时：

```bash
pip3 uninstall -y torch torchvision
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu124
```

**Q：能手动编辑 Markdown 脚本吗？**  
可以！脚本在 `~/.automate/scripts/*.md`，用任何文本编辑器都能改。AI 运行时会直接读取自然语言描述，内联提示只是让执行更快更可靠。

**Q：支持 macOS / Linux 吗？**  
支持。MCP Server 和 CLI 在三个平台都可以运行。YOLO 模型需要 Python 3.10–3.12。

---

## 🤝 参与共建

每一个优秀的开源项目都凝聚着集体的智慧。无论是修复 bug、添加功能，还是改进文档，你的每一份贡献都将帮助更多人摆脱重复性工作。

<a href="https://github.com/yuruotong1/autoMate/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=yuruotong1/autoMate" />
</a>

---

<div align="center">
⭐ 每一个 Star 都是对创作者的鼓励，也是让更多人发现并受益于 autoMate 的机会 ⭐
</div>
