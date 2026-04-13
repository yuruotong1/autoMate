<div align="center"><a name="readme-top"></a>

<img src="./imgs/logo.png" width="120" height="120" alt="autoMate logo">
<h1>autoMate</h1>
<p><b>🤖 专为没有 API 的桌面软件而生的自动化工具</b></p>

[English](./README.md) | [日本語](./README_JA.md)

[![PyPI](https://img.shields.io/pypi/v/automate-mcp)](https://pypi.org/project/automate-mcp/)
[![License](https://img.shields.io/github/license/yuruotong1/autoMate)](LICENSE)

> 给 Claude 一双手和眼睛——自动化任何桌面软件，哪怕它没有 API

https://github.com/user-attachments/assets/bf27f8bd-136b-402e-bc7d-994b99bcc368

</div>

> **特别声明：** autoMate 项目仍处于快速迭代阶段。更深入的设计思考与 AI+RPA 研究笔记，会在 [知识星球「AI桐木和他的贵人们」](https://t.zsxq.com/x1cCW) 中分享。

<div align="center">
<a href="https://t.zsxq.com/x1cCW" target="_blank" rel="noopener noreferrer">
  <img src="./imgs/knowledge.png" width="150" height="150" alt="知识星球二维码">
</a>
</div>

---

## 💡 autoMate 是什么？

autoMate 是一个 MCP Server，让 AI 助手（Claude、GPT 等）能够**直接操控任何桌面软件**——即使那个软件没有 API、没有插件系统、没有任何自动化接口。

可以把它理解为跨平台的 AI 原生版 [Quicker](https://www.getquicker.net)——不需要拖拽积木搭工作流，对 Claude 说一句话就搞定。

**和其他 MCP 的区别：**

| MCP Server | 负责什么 |
|------------|---------|
| filesystem MCP | 文件和文件夹 |
| browser MCP | 网页 |
| Windows MCP | 系统设置和系统调用 |
| **autoMate** | **没有 API 的桌面 GUI 软件** — 剪映、Photoshop、AutoCAD、微信、SAP、公司内部系统… |

---

## ✨ 功能特点

- 🖥️ **专为无 API 的桌面软件而生** — 有界面就能自动化
- 📚 **可复用脚本库** — 工作流保存一次，永久复用；一行命令安装社区脚本
- 🧠 **Claude 知道什么时候该用它** — 明确的使用边界，不会被其他 MCP 替代
- 🤖 **零配置** — 不需要 API Key，不需要环境变量，宿主大模型负责思考
- 🌍 **跨平台** — Windows、macOS、Linux（Quicker 只支持 Windows）

---

## 🔌 接入方式

> **前提：** `pip install uv`

### Claude Desktop

打开 **Settings → Developer → Edit Config**，添加：

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

重启 Claude Desktop 即可，`@latest` 会在每次重启时自动拉取最新版本。

### OpenClaw（小龙虾）

编辑 `~/.openclaw/openclaw.json`：

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

设置 → MCP Servers → 添加：

```json
{
  "automate": {
    "command": "uvx",
    "args": ["automate-mcp@latest"]
  }
}
```

---

## 🛠️ MCP 工具列表

**脚本库** — 核心功能：保存一次工作流，永久复用。

| 工具 | 说明 |
|------|------|
| `list_scripts` | 查看所有已保存的自动化脚本 |
| `run_script` | 按名称执行已保存的脚本 |
| `save_script` | 将当前工作流保存为可复用脚本 |
| `show_script` | 查看脚本内容 |
| `delete_script` | 删除脚本 |
| `install_script` | 从 URL 或社区动作库安装脚本 |

**底层桌面控制** — Claude 在构建或执行脚本时调用。

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

## 📚 脚本库

脚本以 `.md` 文件保存在 `~/.automate/scripts/`，人类可读、Git 可管理、可分享。

**示例脚本：**

```markdown
---
name: jianying_export_douyin
description: 将当前剪映项目导出为抖音 9:16 竖版视频
created: 2025-01-01
---

## Steps

1. 打开导出对话框 [key:ctrl+e]
2. 选择分辨率 1080×1920 [click:coord=320,480]
3. 设置格式为 MP4 [click:coord=320,560]
4. 点击导出按钮 [click:coord=800,650]
5. 等待导出完成 [wait:5]
```

**内联提示语法：**

| 提示 | 操作 |
|------|------|
| `[click:coord=320,240]` | 点击绝对屏幕坐标 |
| `[type:文字内容]` | 输入文字 |
| `[key:ctrl+s]` | 按快捷键 |
| `[wait:2]` | 等待 2 秒 |
| `[scroll_up]` / `[scroll_down]` | 滚动页面 |

没有提示的步骤，由 AI 视觉模型在运行时自动识别执行。

**安装社区脚本：**

```
对 Claude 说："从 <url> 安装这个 automate 脚本"
```

---

## 📝 常见问题

**Q：跟直接用 Claude 的 computer-use 有什么区别？**  
autoMate 提供持久化、可复用的脚本。一个任务自动化一次之后就保存下来，下次直接 `run_script` 秒执行——不需要 AI 重新推理一遍。

**Q：Claude 有时候还是会用 Windows MCP 或 filesystem MCP 替代我的操作怎么办？**  
升级到 v0.4.0+，新版 server description 已明确告知 Claude 各个 MCP 的使用边界。

**Q：支持 macOS / Linux 吗？**  
支持，三个平台均可运行。这也是相比 Quicker（仅 Windows）的核心优势。

---

## 🤝 参与共建

每一个优秀的开源项目都凝聚着集体的智慧。无论是修复 bug、贡献脚本，还是改进文档，欢迎参与。

<a href="https://github.com/yuruotong1/autoMate/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=yuruotong1/autoMate" />
</a>

---

<div align="center">
⭐ 每一个 Star 都是对创作者的鼓励，也是让更多人发现并受益于 autoMate 的机会 ⭐
</div>
