# autoMate

[![MCP Toplist](https://mcptoplist.com/badge/glama%2Fyuruotong1%2FautoMate.svg)](https://mcptoplist.com/server/glama%2Fyuruotong1%2FautoMate)

> **A smart NAS for AI.** Notes · files · reminders · memory · 40+ tools.
> Plug it into OpenClaw / Claude Desktop / Cursor / Cline as a tool
> source, or use it standalone via its built-in web chat.

```
   ┌─ OpenClaw ─────┐                      ┌─ notes / memory ── survives every chat
   ├─ Claude Desktop├──── MCP ────┐        ├─ files ─────────── your file vault (NAS)
   ├─ Cursor / Cline├──── HTTP ───┤        ├─ reminders ─────── push to your phone
   ├─ Kimi / GPT    ├──── bridge ─┤        ├─ memory ────────── cross-session facts
   └─ your scripts  ┘             │        ├─ search.find ───── BM25 over notes+files
                                  ▼        │
                          ┌──────────────────┐    ┌─ shell · script · browser
                          │     autoMate     │ ── ┤  desktop · 31 SaaS APIs
                          │  (your machine)  │    └─ your real Chrome (extension)
                          └────────┬─────────┘
                                   ▼
                          ~/.automate/  · SQLite + Fernet
```

## What's the deal

Every AI vendor wants to be your chat tool. Most can call tools.
**None of them remember anything across vendors, store your files, or
ping your phone when something matters.**

autoMate is the layer behind the chat: a warehouse you own. Pick a
chat client you like (OpenClaw for IM, Claude Desktop for serious
work, Cursor for code), point it at autoMate via MCP, and **that
client** can write into your notes, drop files, schedule reminders,
search your library, and call your real-world tools — and tomorrow's
client can read all of it back the same way.

## Two ways to use it

| Mode | Who's the brain | When |
|---|---|---|
| **As a tool inside another AI client** | Your client (OpenClaw / Claude / Cursor / ...) | Most use cases — IM, coding, research |
| **Standalone via autoMate's web chat** | autoMate's own agent loop | Quick local queries, no other client |

Same backend. Same data. Pick the entry point.

## Connecting to OpenClaw / Claude Desktop / Cursor / Cline (v4.5.7)

After install, open **Settings → Connect to AI clients** and click
**"Copy install text"**. You get a single markdown blob with the
URL + token already filled in, and per-client sections for OpenClaw,
Claude Desktop, Cursor, Cline, generic MCP, and non-MCP gateways.

Three ways to use it:

- Read it and edit your client's config file by hand.
- **Paste it into another AI** — "Cursor, here's autoMate, set it up
  for me." The text is written so an AI reader can find the right
  section and edit the right config.
- For OpenClaw specifically, paste into your OpenClaw config under
  `bundle-mcp` — the section spells it out.

After the client picks up the new server, it gets all autoMate's
tools (`search.find`, `notes.read`, `files.list`, `audio.transcribe`,
...) plus a top-level `automate` tool that runs autoMate's own
agent loop on demand.

See [docs/channels.md](./docs/channels.md) for details.

## Install

| Path | Get | When |
|---|---|---|
| `pip install automate-hub` | Python package | Have Python, want it small |
| Standalone binary (Win / macOS / Linux) | [Releases](https://github.com/yuruotong1/autoMate/releases/latest) | No Python, double-click |
| Docker | `docker run -p 8765:8765 ghcr.io/yuruotong1/automate:latest` | Headless box / NAS |
| Browser extension | [`extension/`](./extension/) | Drive your real Chrome |
| Android APK | [Releases](https://github.com/yuruotong1/autoMate/releases/latest) | Optional viewer for the hub |

After install:

```bash
automate          # double-click on Windows/macOS does the same thing
```

Browser opens to `http://127.0.0.1:8765`. The wizard walks you through
picking a model, pasting a key, and (optionally) wiring up an AI client.

## What's in the box

**Personal data**
- `notes.*` — markdown documents with tags, search, pinning
- `files.*` — content-addressed blob vault, deduplication, **configurable storage path** (point it at an external SSD or NAS mount)
- `search.find` — Coze-style hybrid retrieval (SQLite FTS5 BM25) across notes + files in one call
- `reminders.*` — scheduler thread fires Web Push to your PWA
- `memory.*` — long-term key-value facts that any AI can read/write
- `audio.transcribe` — voice → text via Tencent ASR / OpenAI Whisper, with custom vocabulary mined from your notes (Pro tier)

**Local executors**
- `shell.*`, `script.*` (Python/Bash/Node), `desktop.*` (pyautogui)
- `browser.*` (Playwright, fresh Chromium tab)
- `bx.*` (your real browser via the [Chrome extension](./extension/README.md))

**SaaS integrations** — 31 platforms: GitHub · GitLab · Gitee · Notion ·
Slack · Linear · Jira · Confluence · Trello · Asana · Monday.com · HubSpot ·
Airtable · Stripe · Shopify · Telegram · Discord · MS Teams · Zoom ·
Twitter/X · SendGrid · Mailchimp · Twilio · Sentry · 飞书 · 钉钉 · 企业微信 ·
微信公众号 · 微博 · 语雀 · 高德地图.

**LLM providers** — 25 in the catalog: OpenAI · Anthropic · Gemini · xAI Grok ·
Mistral · Cohere · OpenRouter · Groq · Together · Fireworks · DeepInfra ·
DeepSeek · Moonshot Kimi · 通义 · 豆包 · GLM · 百川 · Yi · MiniMax · 阶跃 ·
混元 · 硅基流动 · Ollama · LM Studio · any OpenAI-compatible.

## IM channels (WeChat / Telegram / WhatsApp / ...)

We don't ship per-platform bots ourselves. Run [OpenClaw](https://github.com/openclaw/openclaw)
alongside autoMate — it has the official Tencent WeChat plugin for
*微信个人助手* (no account-takeover, no ban risk), plus Telegram /
WhatsApp / Slack / Discord / Signal / iMessage. autoMate plugs in as
its tool source via the MCP setup above. The user talks in their
chat platform → OpenClaw routes → OpenClaw's agent calls autoMate
when it needs your data.

The legacy bots in `automate/bots/` (telegram / wechat_oa / wecom)
are frozen but still ship for backward compatibility.

## Project layout

```
autoMate/
├─ automate/                 # the package
│  ├─ server/                # FastAPI app, REST + WS + MCP-over-HTTP
│  │  └─ mcp_bridge.py       # FastMCP exposure, mounted at /mcp/
│  ├─ agent/                 # NL → tool-call loop
│  ├─ providers/             # LLM provider catalog + clients
│  ├─ tools/                 # shell · script · browser · desktop · bx
│  │                         # plus notes · files · reminders · memory
│  │                         # · search · audio
│  ├─ integrations/          # 31 SaaS connectors
│  ├─ frontend/              # static SPA — PWA installable
│  │  └─ local-store.js      # IndexedDB store: notes / memory / files
│  ├─ channels.py            # external IM gateway bridge
│  ├─ audio.py               # transcription provider abstraction
│  ├─ auth.py                # autoMate Cloud session (Pro tier hook)
│  └─ {notes,files,reminders,memory,push}.py
├─ android/                  # native Android WebView app (APK)
├─ extension/                # Chrome MV3 extension
├─ docs/{channels,cloud,relay,mobile,sync}.md
├─ Dockerfile
└─ pyproject.toml
```

## Privacy & safety

- Server binds to `127.0.0.1`. Network access is opt-in (`--host 0.0.0.0`).
- API keys, OAuth tokens, push subscriptions: encrypted with Fernet,
  key at `~/.automate/secret.key` (chmod 600).
- LLM calls go directly from autoMate to the provider you chose. Nothing
  else sees them.
- The MCP endpoint at `/mcp/` requires a Bearer token. Treat it like a
  password — anyone with this token can call autoMate's tools, including
  `shell.exec`. Regenerate from Settings → Channels.
- autoMate Cloud (paid tier) is opt-in. Without `AUTOMATE_CLOUD_URL` set,
  no data leaves your machine. See [docs/cloud.md](./docs/cloud.md) for
  the open-client / closed-server boundary.

## Status

**v4.5.7** — autoMate is now an MCP-over-HTTP tool source for any
OpenClaw / Claude Desktop / Cursor / Cline / Cline / Kimi setup. Settings
gives you a one-click "Copy install text" for any AI client. Personal
infra is filled out: Coze-style retrieval, audio transcription,
configurable storage path, in-app auto-update, login hook for the
upcoming autoMate Cloud Pro tier.

中文版: [README_CN.md](./README_CN.md)

## License

MIT.
