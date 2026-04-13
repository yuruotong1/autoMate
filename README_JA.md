<div align="center"><a name="readme-top"></a>

<img src="./imgs/logo.png" width="120" height="120" alt="autoMate logo">
<h1>autoMate</h1>
<p><b>🤖 AI駆動のデスクトップ自動化ツール | コンピュータに仕事を任せる</b></p>

[English](./README.md) | [中文](./README_CN.md)

[![PyPI](https://img.shields.io/pypi/v/automate-mcp)](https://pypi.org/project/automate-mcp/)
[![License](https://img.shields.io/github/license/yuruotong1/autoMate)](LICENSE)

> "面倒な作業を自動化し、時間を生活に取り戻す"

https://github.com/user-attachments/assets/bf27f8bd-136b-402e-bc7d-994b99bcc368

</div>

> **声明：** autoMateは急速な開発段階にあります。深い設計思考・技術的議論・AI+RPA研究ノートは [知識プラネット「AI桐木とその仲間たち」](https://t.zsxq.com/x1cCW) で共有しています。

<div align="center">
<a href="https://t.zsxq.com/x1cCW" target="_blank" rel="noopener noreferrer">
  <img src="./imgs/knowledge.png" width="150" height="150" alt="知識プラネットQRコード">
</a>
</div>

---

## 💡 autoMateとは？

autoMateは**AI + RPAデスクトップ自動化ツール**です。自然言語でコンピュータを制御します。従来のRPAと違い、あなたのデモンストレーションから学習します — ボタンが見つからない場合は一度クリックするだけで、永遠に覚えます。

**2つの使い方：**

| モード | 適したシーン |
|--------|------------|
| 🔌 **MCPサーバー** | Claude Desktop、OpenClaw、Cursor、Windsurf — 設定してすぐ使える |
| 💻 **CLI** | スクリプト、ターミナル、パワーユーザー |

---

## ✨ 主な機能

- 🔮 **ノーコード自動化** — 自然言語でタスクを記述、AIがスクリプトを生成して実行
- 🧠 **人間参加型学習** — AIが要素を見つけられない場合、一度クリックすれば永遠に記憶
- 📝 **Markdownスクリプト** — 読みやすい`.md`ファイルとして保存、直接編集可能
- 🌐 **ユニバーサルLLMサポート** — OpenAI、Azure、OpenRouter、Groq、Ollama、DeepSeek等全対応
- 🔌 **MCPサーバー** — PyPIで公開済み、1行で接続
- 🖥️ **クロスプラットフォーム** — Windows、macOS、Linux

---

## 🔌 MCPサーバー セットアップ

> **前提：** `uv`を一度インストール — `pip install uv`

**ゼロ設定** — APIキー不要、環境変数不要。ホストLLM（Claude、GPTなど）が思考し、autoMateは手と目を提供します。

### Claude Desktop

Claude Desktop を開き、**Settings → Developer → Edit Config** から設定ファイルを直接開けます。

> デフォルトのパス（参考）：
> - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
> - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

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

再起動すれば完了！

### OpenClaw

`~/.openclaw/openclaw.json` を編集：

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

ゲートウェイを再起動：

```bash
openclaw gateway restart
```

### Cursor / Windsurf / Cline

設定 → MCPサーバー → 追加：

```json
{
  "automate": {
    "command": "uvx",
    "args": ["automate-mcp"]
  }
}
```

### MCPツール

| ツール | 説明 |
|--------|------|
| `screenshot` | 現在の画面をキャプチャしてbase64 PNGで返す |
| `click` | 画面座標をクリック（左/右/中） |
| `double_click` | 画面座標をダブルクリック |
| `type_text` | 現在のカーソル位置にテキストを入力 |
| `press_key` | キーまたはキーコンボ（例：`ctrl+c`、`enter`） |
| `scroll` | 上下スクロール |
| `mouse_move` | マウスカーソルを移動（クリックなし） |
| `drag` | ある位置から別の位置にドラッグ |
| `get_screen_size` | 画面解像度を取得 |
| `get_cursor_position` | 現在のカーソル位置を取得 |

---

## 🚀 CLI

```bash
git clone https://github.com/yuruotong1/autoMate.git
cd autoMate
conda create -n automate python=3.12 && conda activate automate
python install.py
```

```bash
export OPENAI_API_KEY=sk-...
export OPENAI_MODEL=gpt-4o

python cli.py run "メモ帳を開いてHello Worldと入力"
python cli.py list
python cli.py exec open_notepad
python cli.py show open_notepad
```

---

## 📝 Markdownスクリプト

```markdown
---
name: open_notepad
description: メモ帳を開いてメッセージを入力
---

## Steps

1. Windowsキーを押してスタートメニューを開く `[key:win]`
2. 検索ボックスに"notepad"と入力 `[type:notepad]`
3. メモ帳の結果をクリック `[click:Notepad]`
4. 挨拶文を入力 `[type:Hello, World!]`
5. Ctrl+Sで保存 `[key:ctrl+s]`
```

| ヒント | アクション |
|--------|----------|
| `[click:OK]` | OCRでラベルを検索してクリック |
| `[click:coord=320,240]` | 絶対座標でクリック |
| `[type:テキスト]` | テキストを入力 |
| `[key:ctrl+s]` | ショートカットキー |
| `[wait:2]` | 2秒待機 |

ヒントのないステップはAIビジョンモデルが自動解釈します。

---

## 🌐 対応LLMプロバイダー

| プロバイダー | Base URL | モデル例 |
|------------|----------|---------|
| [OpenAI](https://platform.openai.com) | `https://api.openai.com/v1` | gpt-4o, o3 |
| [OpenRouter](https://openrouter.ai) | `https://openrouter.ai/api/v1` | claude-3.7-sonnet |
| [DeepSeek](https://platform.deepseek.com) | `https://api.deepseek.com/v1` | deepseek-chat |
| [Groq](https://console.groq.com) | `https://api.groq.com/openai/v1` | llama-3.3-70b |
| [Ollama](https://ollama.com) | `http://localhost:11434/v1` | qwen2.5-vl |

---

## 🤝 コントリビュート

<a href="https://github.com/yuruotong1/autoMate/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=yuruotong1/autoMate" />
</a>

---

<div align="center">
⭐ スターは制作者への励ましであり、より多くの人々がautoMateを発見する機会です ⭐
</div>
