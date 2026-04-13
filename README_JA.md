<div align="center"><a name="readme-top"></a>

<img src="./imgs/logo.png" width="120" height="120" alt="autoMate logo">
<h1>autoMate</h1>
<p><b>🤖 AI駆動のデスクトップ自動化ツール | コンピュータに仕事を任せる</b></p>

[English](./README.md) | [中文](./README_CN.md)

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

**3つの使い方：**

| モード | 適したシーン |
|--------|------------|
| 🔌 **MCPサーバー** | Claude Desktop、Cursor、Windsurf — UIなし |
| 💻 **CLI** | スクリプト、ターミナル、パワーユーザー |
| 🖥️ **デスクトップUI** | ブラウザ経由のビジュアルインターフェース |

---

## ✨ 主な機能

- 🔮 **ノーコード自動化** — 自然言語でタスクを記述、AIがスクリプトを生成して実行
- 🧠 **人間参加型学習** — AIが要素を見つけられない場合、一度クリックすれば永遠に記憶
- 📝 **Markdownスクリプト** — 読みやすい`.md`ファイルとして保存、直接編集可能、JSON不要
- 🌐 **ユニバーサルLLMサポート** — OpenAI、Azure、OpenRouter、Groq、Ollama、DeepSeek等全対応
- 🔌 **MCPサーバー** — Claude Desktop、Cursor、Windsurf、Clineに1行で接続
- 🖥️ **クロスプラットフォーム** — Windows、macOS、Linux

---

## 🔌 MCPサーバー — ワンコマンドセットアップ

最も素早い接続方法。gitクローンもpipインストールも不要 — 貼り付けて再起動するだけです。

**Claude Desktop (macOS)** → `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows** → `%APPDATA%\Claude\claude_desktop_config.json`  
**Cursor / Windsurf** → 設定 → MCPサーバー

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

> `uvx`がない場合は `pip install uv` を一度実行してください。

クライアントを再起動後、こう言うだけ：
> *"automateを使ってChromeを開き、最新のAIニュースを検索して"*

### MCPツール

| ツール | 説明 |
|--------|------|
| `run_task` | 自然言語でタスクを記述し、autoMateがデスクトップを自動操作 |
| `screenshot` | 現在の画面（または特定領域）をキャプチャしてbase64 PNGで返す |

---

## 🚀 CLIとデスクトップUI

### インストール

```bash
git clone https://github.com/yuruotong1/autoMate.git
cd autoMate
conda create -n automate python=3.12
conda activate automate
python install.py
```

### CLI（ブラウザ不要）

```bash
export OPENAI_API_KEY=sk-...
export OPENAI_MODEL=gpt-4o

# タスクを記述 — AIがMarkdownスクリプトを生成して実行
python cli.py run "メモ帳を開いてHello Worldと入力"

# 保存済みスクリプトを再実行
python cli.py exec open_notepad

# 保存済みスクリプト一覧
python cli.py list

# スクリプトの内容を確認
python cli.py show open_notepad
```

### デスクトップUI（Gradio）

```bash
python main.py
# ブラウザで http://localhost:7888/ を開く
```

### バイナリダウンロード

Python不要。[Releases](https://github.com/yuruotong1/autoMate/releases)ページから各プラットフォーム向けパッケージをダウンロードできます。

---

## 📝 Markdownスクリプト

autoMateは`~/.automate/scripts/`に`.md`ファイルとしてスクリプトを保存します。人間が読め、Gitで管理でき、実行時にAIが直接解釈します。

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

## Notes
メモ帳は通常1〜2秒で開きます。

## Code
```python
# オプション：カスタムPythonをステップとして実行
import time
time.sleep(1)
```
```

### インラインヒント構文

| ヒント | アクション |
|--------|----------|
| `[click:OK]` | "OK"を含むラベルの要素をクリック（OCRベース） |
| `[click:coord=320,240]` | 絶対座標でクリック |
| `[type:テキスト]` | テキストを入力 |
| `[key:ctrl+s]` | キーボードショートカットを押す |
| `[wait:2]` | 2秒待機 |
| `[scroll_up]` / `[scroll_down]` | ページをスクロール |

ヒントの**ないステップ**は、実行時にAIビジョンモデルが自動解釈します。

### 人間参加型学習

AIが要素を見つけられない場合、一時停止して尋ねます：

```
[autoMate] Step 3: '送信ボタンをクリック'
対象要素を今すぐクリックしてください…

[autoMate] クリック座標 (842, 631) を検出 — 学習中…
[autoMate] ヒントを学習: [click:送信]  実行を再開します。
```

学習したヒントは自動的にMarkdownファイルに書き戻されます — 次回の実行では確認なしに動作します。

---

## 🌐 対応LLMプロバイダー

autoMateは**任意のOpenAI互換API**で動作します：

| プロバイダー | Base URL | モデル例 |
|------------|----------|---------|
| [OpenAI](https://platform.openai.com) | `https://api.openai.com/v1` | gpt-4o, gpt-4.1, o3 |
| [Azure OpenAI](https://azure.microsoft.com/products/ai-services/openai-service) | Azureエンドポイント | gpt-4o |
| [OpenRouter](https://openrouter.ai) | `https://openrouter.ai/api/v1` | claude-3.7-sonnet, gemini-2.5-pro |
| [DeepSeek](https://platform.deepseek.com) | `https://api.deepseek.com/v1` | deepseek-chat |
| [Groq](https://console.groq.com) | `https://api.groq.com/openai/v1` | llama-3.3-70b-versatile |
| [Ollama](https://ollama.com)（ローカル） | `http://localhost:11434/v1` | qwen2.5-vl, gemma3-tools:27b |

> **推奨：** ビジョン対応マルチモーダルモデルを使用すると最良の結果が得られます（`gpt-4o`、OpenRouter経由の`claude-3.7-sonnet`、またはOllama経由の`qwen2.5-vl`）。

```bash
export OPENAI_API_KEY=sk-...
export OPENAI_BASE_URL=https://openrouter.ai/api/v1
export OPENAI_MODEL=anthropic/claude-3.7-sonnet
```

---

## 📝 よくある質問

**Q：GPUなしで動作が遅いのはなぜ？**  
OmniParser（YOLOベースのUI検出）はGPU集約型です。NVIDIA GPU（4GB+ VRAM）がある場合：

```bash
pip3 uninstall -y torch torchvision
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu124
```

**Q：Markdownスクリプトを手動で編集できますか？**  
はい！スクリプトは`~/.automate/scripts/*.md`にあります。AIは実行時に自然言語の説明を直接読み取るため、英語（または日本語）で書くだけで十分です。

**Q：macOS / Linuxで動作しますか？**  
はい。MCPサーバーとCLIは3つのプラットフォームすべてで動作します。YOLOモデルにはPython 3.10〜3.12が必要です。

---

## 🤝 コントリビュート

優れたオープンソースプロジェクトは、集団の知恵の結晶です。バグ修正、機能追加、ドキュメント改善など、あなたの貢献が何千人もの人々を繰り返し作業から解放します。

<a href="https://github.com/yuruotong1/autoMate/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=yuruotong1/autoMate" />
</a>

---

<div align="center">
⭐ スターは制作者への励ましであり、より多くの人々がautoMateを発見する機会です ⭐
</div>
