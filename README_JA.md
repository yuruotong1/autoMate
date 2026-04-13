<div align="center"><a name="readme-top"></a>

<img src="./imgs/logo.png" width="120" height="120" alt="autoMate logo">
<h1>autoMate</h1>
<p><b>🤖 APIのないデスクトップアプリを自動化するMCPサーバー</b></p>

[English](./README.md) | [中文](./README_CN.md)

[![PyPI](https://img.shields.io/pypi/v/automate-mcp)](https://pypi.org/project/automate-mcp/)
[![License](https://img.shields.io/github/license/yuruotong1/autoMate)](LICENSE)

> Claudeに手と目を — APIがなくても、どんなデスクトップアプリも自動化できる

https://github.com/user-attachments/assets/bf27f8bd-136b-402e-bc7d-994b99bcc368

</div>

---

## 💡 autoMateとは？

autoMateはMCPサーバーです。AIアシスタント（Claude、GPTなど）が**APIのないデスクトップアプリを直接操作**できるようになります。

クロスプラットフォームでAIネイティブな[Quicker](https://www.getquicker.net)の代替として考えてください。ブロックをドラッグしてワークフローを組む必要はなく、Claudeに話しかけるだけです。

**他のMCPとの違い：**

| MCPサーバー | 自動化対象 |
|------------|----------|
| filesystem MCP | ファイルとフォルダ |
| browser MCP | Webページ |
| Windows MCP | OS設定・システムコール |
| **autoMate** | **APIのないデスクトップGUIアプリ** — Photoshop、AutoCAD、SAP、社内ツール… |

---

## ✨ 主な機能

- 🖥️ **APIなしアプリを自動化** — GUIがあれば動かせる
- 📚 **再利用可能なスクリプトライブラリ** — ワークフローを一度保存して永久に再利用
- 🧠 **Claudeが使いどころを理解** — 他のMCPに上書きされない明確なアイデンティティ
- 🤖 **ゼロ設定** — APIキー不要、環境変数不要
- 🌍 **クロスプラットフォーム** — Windows、macOS、Linux（QuickerはWindowsのみ）

---

## 🔌 セットアップ

> **前提：** `pip install uv`

### Claude Desktop

**Settings → Developer → Edit Config** を開いて追加：

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

Claude Desktopを再起動すれば完了。`@latest`により毎回起動時に自動更新されます。

### OpenClaw

`~/.openclaw/openclaw.json` を編集：

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

設定 → MCPサーバー → 追加：

```json
{
  "automate": {
    "command": "uvx",
    "args": ["automate-mcp@latest"]
  }
}
```

---

## 🛠️ MCPツール

**スクリプトライブラリ** — 一度保存すれば永久に再利用。

| ツール | 説明 |
|--------|------|
| `list_scripts` | 保存済みスクリプト一覧 |
| `run_script` | 名前でスクリプトを実行 |
| `save_script` | ワークフローをスクリプトとして保存 |
| `show_script` | スクリプトの内容を表示 |
| `delete_script` | スクリプトを削除 |
| `install_script` | URLまたはコミュニティライブラリからインストール |

**低レベルデスクトップ制御** — スクリプト構築・実行時にClaudeが使用。

| ツール | 説明 |
|--------|------|
| `screenshot` | 画面をキャプチャしてbase64 PNGで返す |
| `click` | 座標をクリック |
| `double_click` | 座標をダブルクリック |
| `type_text` | テキストを入力（CJK対応） |
| `press_key` | キーまたはキーコンボを押す |
| `scroll` | 上下スクロール |
| `mouse_move` | カーソルを移動（クリックなし） |
| `drag` | ある位置から別の位置にドラッグ |

---

## 📚 スクリプトライブラリ

スクリプトは `~/.automate/scripts/` に `.md` ファイルとして保存されます。

```markdown
---
name: export_premiere_youtube
description: PremiereのプロジェクトをYouTube用にエクスポート
created: 2025-01-01
---

## Steps

1. エクスポートダイアログを開く [key:ctrl+m]
2. YouTubeプリセットを選択 [click:coord=320,480]
3. エクスポートをクリック [click:coord=800,650]
4. 完了まで待機 [wait:10]
```

| ヒント | アクション |
|--------|----------|
| `[click:coord=320,240]` | 絶対座標をクリック |
| `[type:テキスト]` | テキストを入力 |
| `[key:ctrl+s]` | ショートカットキー |
| `[wait:2]` | 2秒待機 |

---

## 📝 よくある質問

**Q: Claudeがautomateの代わりにWindows MCPやfilesystem MCPを使ってしまう**  
v0.4.0以降にアップデートしてください。サーバーの説明文が更新され、Claudeが適切なMCPを選択できるようになりました。

**Q: macOS / Linuxで動作しますか？**  
はい。Quicker（Windowsのみ）と違い、3プラットフォーム全てで動作します。

---

## 🤝 コントリビュート

<a href="https://github.com/yuruotong1/autoMate/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=yuruotong1/autoMate" />
</a>

---

<div align="center">
⭐ スターは制作者への励ましであり、より多くの人々がautoMateを発見する機会です ⭐
</div>
