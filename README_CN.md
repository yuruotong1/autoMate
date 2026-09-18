# autoMate

> **AI 的智能 NAS。** 笔记 · 文件 · 提醒 · 记忆 · 40+ 工具。
> 接进 OpenClaw / Claude Desktop / Cursor / Cline 当工具源,
> 或者用它自带的 web 聊天独立跑。

```
   ┌─ OpenClaw ─────┐                      ┌─ notes/memory ──── 跨会话生存
   ├─ Claude Desktop├──── MCP ────┐        ├─ files ─────────── 文件库 (NAS)
   ├─ Cursor / Cline├──── HTTP ───┤        ├─ reminders ─────── 推到手机
   ├─ Kimi / GPT    ├──── bridge ─┤        ├─ memory ────────── 长期记忆
   └─ 你的脚本      ┘             │        ├─ search.find ───── 笔记+文件 BM25 检索
                                  ▼        │
                          ┌──────────────────┐    ┌─ shell · script · browser
                          │     autoMate     │ ── ┤  desktop · 31 家 SaaS API
                          │   (你的机器)     │    └─ 你正在用的 Chrome (扩展)
                          └────────┬─────────┘
                                   ▼
                          ~/.automate/  · SQLite + Fernet 加密
```

## 这是什么

每家 AI 厂商都在抢"聊天入口"。大多数也能调工具。**但没有任何一家能把你
所有用过的 AI 串起来 — 跨厂商记忆、本地存大文件、时间到了主动推手机。**

autoMate 是聊天背后的那一层:**你自己拥有的仓库**。挑一个你喜欢的 AI 客户端
(OpenClaw 接 IM,Claude Desktop 干正事,Cursor 写代码),用 MCP 把它指向
autoMate — 从此**那个客户端**能往你笔记里写、把文件丢进来、设置提醒、检索
你的资料库、调用真实工具。明天换一家,数据照样能读出来。

## 两种用法

| 模式 | 谁是脑子 | 适合 |
|---|---|---|
| **当别的 AI 客户端的工具** | 你的客户端(OpenClaw / Claude / Cursor / ...) | 大部分场景:IM、写代码、做研究 |
| **走 autoMate 自带的 web 聊天** | autoMate 自己的 agent | 本地快查,不想用别的客户端 |

后端是同一个,数据一份,看你想从哪儿进。

## 接 OpenClaw / Claude Desktop / Cursor / Cline (v4.5.7)

装完之后,打开 **Settings → Connect to AI clients**,点
**"Copy install text"**。一段 markdown 进剪贴板,URL + token 已经填好,
分节涵盖 OpenClaw / Claude Desktop / Cursor / Cline / 通用 MCP / 非 MCP 网关。

三种用法:

- 自己读着照配置文件改
- **粘贴给另一个 AI**:"Cursor,这是 autoMate,帮我配上"。文本是设计成
  AI 也能读的 — 它会自己找到对应那节,改对应配置文件
- OpenClaw 用户:粘到 OpenClaw 的 `bundle-mcp` 配置里就行,文中给了具体格式

客户端接受新 server 后,所有 autoMate 工具都能用(`search.find`、
`notes.read`、`files.list`、`audio.transcribe` ...),还有一个顶层
`automate` 工具能整轮调 autoMate 自己的 agent。

详见 [docs/channels.md](./docs/channels.md)。

## 安装

| 路径 | 拿什么 | 适合 |
|---|---|---|
| `pip install automate-hub` | Python 包 | 有 Python 想轻量 |
| 独立二进制(Win/Mac/Linux) | [Releases](https://github.com/yuruotong1/autoMate/releases/latest) | 没 Python,双击就跑 |
| Docker | `docker run -p 8765:8765 ghcr.io/yuruotong1/automate:latest` | NAS / 服务器 |
| 浏览器扩展 | [`extension/`](./extension/) | 接管你正在用的 Chrome |
| 手机 (PWA) | 浏览器打开 hub 地址 → 加入主屏幕 | iOS / Android 都行,免上架 |

装完跑 `automate`,浏览器自动开。配模型 + 粘 key + (可选) 接 AI 客户端,
两三分钟搞定。

## 仓库里有什么

**个人数据**
- `notes.*` — Markdown 文档,标签、搜索、置顶
- `files.*` — 内容寻址文件库,SHA-256 去重,**存储路径可配**(指外置 SSD / NAS 都行)
- `search.find` — Coze 风格混合检索(SQLite FTS5 BM25),笔记 + 文件一锅出
- `reminders.*` — 后台 scheduler + Web Push 推手机
- `memory.*` — 长期 K/V 事实,任何 AI 都能读写
- `audio.transcribe` — 语音转文字,腾讯 ASR / OpenAI Whisper,自动用你笔记里挖出来的专有名词当 hot-words(Pro tier)

**本地执行器**
- `shell.*`、`script.*`(Python/Bash/Node)、`desktop.*`(pyautogui)
- `browser.*`(Playwright,起干净 Chromium)
- `bx.*`(通过 [Chrome 扩展](./extension/README.md) 接管你正在用的浏览器)

**SaaS 集成 — 31 家**:GitHub · GitLab · Gitee · Notion · Slack · Linear ·
Jira · Confluence · Trello · Asana · Monday · HubSpot · Airtable · Stripe ·
Shopify · Telegram · Discord · MS Teams · Zoom · Twitter/X · SendGrid ·
Mailchimp · Twilio · Sentry · 飞书 · 钉钉 · 企业微信 · 微信公众号 · 微博 ·
语雀 · 高德地图。

**LLM 供应商 — 25 家**:OpenAI · Anthropic · Gemini · xAI Grok · Mistral ·
Cohere · OpenRouter · Groq · Together · Fireworks · DeepInfra · DeepSeek ·
Kimi · 通义 · 豆包 · 智谱 GLM · 百川 · Yi · MiniMax · 阶跃 · 混元 · 硅基流动 ·
Ollama · LM Studio · 任意 OpenAI 兼容端点。

## 微信 / Telegram / WhatsApp 等 IM 怎么接

我们**不自己写每一家 IM 的 bot**。在 autoMate 旁边跑
[OpenClaw](https://github.com/openclaw/openclaw) — 它有腾讯官方写的
**微信个人助手**插件(走的是微信官方渠道,**不是个人微信号自动化,
没有封号风险**),同时支持 Telegram / WhatsApp / Slack / Discord /
Signal / iMessage。autoMate 通过上面那段 MCP 配置接进去当工具源。

用户在自己的 IM 里说话 → OpenClaw 收 → OpenClaw 的 agent 需要查你
个人数据时调 autoMate 工具 → 回话。

老的 `automate/bots/`(telegram / wechat_oa / wecom)冻结但保留,新部署
应该走 OpenClaw + 上面的 MCP 桥。

## 隐私

- 服务器默认绑 `127.0.0.1`,需要联网访问要 `--host 0.0.0.0`。
- 凭据全部 Fernet 加密,密钥在 `~/.automate/secret.key`(0600)。
- LLM 调用直接从 autoMate 走到你选的厂商,中间没人偷看。
- `/mcp/` 端点要 Bearer token 鉴权 — 当密码看待,任何拿到 token 的人都能调
  autoMate 工具(包括 `shell.exec`)。Settings → Channels 可以重新生成。
- autoMate Cloud(付费层)是**可选的**。不设 `AUTOMATE_CLOUD_URL`,数据
  完全不出本机。详见 [docs/cloud.md](./docs/cloud.md)。

## 状态

**v4.5.7** — autoMate 现在是 MCP-over-HTTP 工具源,任何 OpenClaw /
Claude Desktop / Cursor / Cline / Kimi 客户端都能用。Settings 里一键复制
适配所有客户端的安装文本(也能粘给另一个 AI 让它帮你配)。个人基础设施
全到位:Coze 风格检索、语音转写、自定义存储路径、APP 内自动更新、autoMate
Cloud 付费层登录入口已就位。

English: [README.md](./README.md)

## License

MIT。
## 执行步骤追踪

使用 `automate serve --trace`、`automate mcp --trace`，或设置环境变量
`AUTOMATE_DEVTOOLS=true`，可在本地记录工具执行步骤、耗时和异常类型。
默认关闭，不记录参数和返回内容。事件格式及调试工具接入方式见
[追踪文档](docs/tracing.md)。
