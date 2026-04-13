<div align="center"><a name="readme-top"></a>

<img src="./imgs/logo.png" width="120" height="120" alt="autoMate logo">
<h1>autoMate</h1>
<p><b>🤖 AI驱动的本地自动化工具 | 让电脑自己会干活</b></p>

[English](./README.md) | [日本語](./README_JA.md)

>"让繁琐自动化，把时间还给生活"

https://github.com/user-attachments/assets/bf27f8bd-136b-402e-bc7d-994b99bcc368


</div>

> **特别声明：** autoMate 项目仍处于快速迭代的早期阶段，我们会不断探索和融入最新技术。在这个过程中，**更深入的设计思考、技术选型讨论、遇到的挑战与解决方案，以及我对 AI+RPA 领域的持续研究笔记，会主要在我的 [知识星球「AI桐木和他的贵人们」](https://t.zsxq.com/x1cCW)** 中分享和探讨。
>
> 如果你对 autoMate 背后的技术细节、发展方向或更广泛的 AI 自动化话题感兴趣，欢迎扫码加入，与我和其他朋友一起交流，共同见证 autoMate 的成长！

<div align="center">
<figure>
    <a href="[你的知识星球链接]" target="_blank" rel="noopener noreferrer"><img src="./imgs/knowledge.png" width="150" height="150" alt="知识星球二维码"></a>
</figure>
</div>


## 💫 重新定义你与电脑的关系

不同于传统RPA工具的繁琐，autoMate借助大模型的能力，只需用自然语言描述任务，AI就能完成复杂的自动化流程。从此告别重复性工作，专注于真正创造价值的事情！

**让自动化为你的生活创造更多可能。**

## 💡 项目简介
autoMate 是一款革命性的AI+RPA自动化工具，基于OmniParser构建，它能够

- 📊 理解您的需求，自动进行任务规划
- 🔍 智能理解屏幕内容，模拟人类视觉和操作
- 🧠 自主决策，根据任务需求进行判断并采取行动
- 💻 支持本地化部署，保护您的数据安全和隐私

## ✨ 功能特点

- 🔮 **无代码自动化** — 用自然语言描述任务，AI 自动生成脚本并执行
- 🧠 **人机协同学习** — 当 AI 找不到元素时，只需点击一次，下次自动记住
- 📝 **Markdown 脚本** — 脚本以可读的 `.md` 文件保存，可直接编辑，无需僵化 JSON 格式
- 🖥️ **全界面操控** — 支持任何可视化界面，不限于特定软件
- 🌐 **多平台 LLM 支持** — 兼容 OpenAI、Azure、OpenRouter、Groq、Ollama、DeepSeek 等任意 OpenAI-compatible 接口
- 🔌 **MCP Server** — 可作为 MCP 工具供 Claude Desktop、Cursor、Windsurf 等直接调用
- 💻 **CLI 模式** — 轻量命令行界面，无需浏览器


## 🚀 快速开始

### 📥 直接使用
可以直接从 [GitHub Releases](https://github.com/yuruotong1/autoMate/releases) 下载可执行文件使用，无需 Python 环境。

### 📦 从源码安装
强烈建议先安装 miniConda，网上有很多教程，实在不懂可以问 AI。然后按照下面命令安装环境：

```bash
git clone https://github.com/yuruotong1/autoMate.git
cd autoMate
conda create -n "automate" python==3.12
conda activate automate
python install.py
```

**桌面 UI（Gradio）：**
```bash
python main.py
# 浏览器打开 http://localhost:7888/
```

**CLI（轻量，无需浏览器）：**
```bash
export OPENAI_API_KEY=sk-...
export OPENAI_MODEL=gpt-4o

# 描述任务 — AI 生成 Markdown 脚本并执行
python cli.py run "打开记事本，输入 Hello World"

# 查看已保存的脚本
python cli.py list

# 重新执行已保存的脚本
python cli.py exec open_notepad

# 查看脚本内容
python cli.py show open_notepad
```

### 📝 Markdown 脚本格式

autoMate 将脚本保存为 `~/.automate/scripts/` 目录下的 `.md` 文件，人类可读，可直接编辑。
每个步骤是一句自然语言，后面可跟内联操作提示：

```markdown
---
name: open_notepad
description: 打开记事本并输入消息
---

## Steps

1. 按 Windows 键打开开始菜单 `[key:win]`
2. 在搜索框中输入 "notepad" `[type:notepad]`
3. 点击记事本应用 `[click:Notepad]`
4. 输入问候语 `[type:Hello, World!]`
5. 用 Ctrl+S 保存 `[key:ctrl+s]`

## Notes
记事本通常 1–2 秒内打开。
```

**内联提示语法：**

| 提示 | 操作 |
|------|------|
| `[click:确认]` | 点击标签含"确认"的元素 |
| `[click:coord=320,240]` | 点击绝对坐标 |
| `[type:文本内容]` | 输入文字 |
| `[key:ctrl+s]` | 按快捷键 |
| `[wait:2]` | 等待 2 秒 |
| `[scroll_up]` / `[scroll_down]` | 滚动页面 |

没有提示的步骤在运行时由 AI 视觉模型自动解读。也可以嵌入 Python 代码块实现自定义逻辑。

### 🔔 注意

autoMate 现在支持**任意 OpenAI-compatible 接口**，在设置界面填写 Base URL、API Key 和 Model 即可切换：

| 平台 | Base URL | 示例模型 |
| --- | --- | --- |
| [OpenAI](https://platform.openai.com) | `https://api.openai.com/v1` | gpt-4o, gpt-4.1, o3 |
| [Azure OpenAI](https://azure.microsoft.com/products/ai-services/openai-service) | 你的 Azure 端点 | gpt-4o |
| [OpenRouter](https://openrouter.ai) | `https://openrouter.ai/api/v1` | claude-3.7-sonnet, gemini-2.5-pro 等 |
| [DeepSeek](https://platform.deepseek.com) | `https://api.deepseek.com/v1` | deepseek-chat, deepseek-reasoner |
| [Groq](https://console.groq.com) | `https://api.groq.com/openai/v1` | llama-3.3-70b-versatile |
| [Ollama](https://ollama.com)（本地） | `http://localhost:11434/v1` | qwen2.5-vl, gemma3-tools:27b |
| [yeka](https://2233.ai/api)（国内代理） | `https://api.2233.ai/v1` | gpt-4o, o1 |

> **推荐**：使用支持视觉的多模态模型效果最佳，如 `gpt-4o`、通过 OpenRouter 使用 `claude-3.7-sonnet`，或通过 Ollama 本地运行 `qwen2.5-vl`。


## 🔌 MCP Server

autoMate 可以部署为 **MCP（Model Context Protocol）服务器**，让 Claude Desktop、Cursor、Windsurf 等 AI 客户端直接调用它来控制你的本地桌面。

### 配置方法

**1. 安装依赖**
```bash
pip install -r requirements.txt
```

**2. 添加到 MCP 客户端配置**

以 Claude Desktop 为例，编辑配置文件：
- macOS：`~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows：`%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "automate": {
      "command": "python",
      "args": ["/绝对路径/autoMate/mcp_server.py"],
      "env": {
        "OPENAI_API_KEY": "sk-...",
        "OPENAI_BASE_URL": "https://api.openai.com/v1",
        "OPENAI_MODEL": "gpt-4o"
      }
    }
  }
}
```

重启 Claude Desktop 后，会出现两个新工具：**`run_task`** 和 **`screenshot`**。

**3. 开始使用**

在 Claude Desktop 中直接说：
> "用 automate 打开 Chrome，搜索最新的 AI 新闻"

Claude 会调用 `run_task`，autoMate 自动控制桌面完成操作。

### 可用 MCP 工具

| 工具 | 描述 |
| --- | --- |
| `run_task` | 用自然语言描述任务，autoMate 自动执行桌面操作 |
| `screenshot` | 截取当前屏幕（或指定区域），返回 base64 PNG |

## 📝常见问题
### 支持什么模型？
现在支持**任意 OpenAI-compatible 接口**。底层使用三级 fallback 机制（结构化输出 → JSON 模式 → 纯文本提取），跨平台兼容性大幅提升。

推荐使用**支持视觉的多模态模型**（agent 需要看屏幕内容）。`gpt-4o`、通过 OpenRouter 使用 Claude/Gemini、或 Ollama 本地运行 `qwen2.5-vl` 均已测试可用。


### 为什么我的执行速度很慢?
如果你的电脑没有NVIDIA独显的话，运行的会比较慢，因为我们会高频次调用OCR对视觉进行标注，这会消耗大量的GPU资源，我们也在积极进行优化和适配。建议使用不少于 4G 显存的英伟达显卡运行，并且版本和torch版本一致：

1. 运行`pip list`查看torch版本；
2. 从[官网](https://pytorch.org/get-started/locally/)查看支持的cuda版本；
3. 卸载已安装的 torch 和 torchvision；
3. 复制官方的 torch 安装命令，重新安装适合自己 cuda 版本的 torch。

比如我的 cuda 版本为 12.4，需要按照如下命令来安装 torch；

```bash
pip3 uninstall -y torch torchvision
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```


## 🤝 参与共建

每一个优秀的开源项目都凝聚着集体的智慧。autoMate的成长离不开你的参与和贡献。无论是修复bug、添加功能，还是改进文档，你的每一份付出都将帮助成千上万的人摆脱重复性工作的束缚。

加入我们，一起创造更加智能的未来。

<a href="https://github.com/yuruotong1/autoMate/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=yuruotong1/autoMate" />
</a>

---

<div align="center">
⭐ 每一个Star都是对创作者的鼓励，也是让更多人发现并受益于autoMate的机会 ⭐
今天你的支持，就是我们明天前进的动力
</div>
