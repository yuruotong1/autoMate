<div align="center"><a name="readme-top"></a>

<img src="./imgs/logo.png" width="120" height="120" alt="autoMate logo">
<h1>autoMate</h1>
<p><b>🤖 AI駆動のローカル自動化ツール | コンピュータに仕事を任せる</b></p>

[English](./README.md) | [中文](./README_CN.md)

>"面倒な作業を自動化し、時間を生活に取り戻す"

https://github.com/user-attachments/assets/bf27f8bd-136b-402e-bc7d-994b99bcc368


</div>

> **特別声明：** autoMateプロジェクトは現在も急速な開発段階にあり、最新の技術を継続的に探索・統合しています。この過程で、**より深い設計思考、技術スタックの議論、直面する課題と解決策、およびAI+RPA分野に関する継続的な研究ノートは、主に[知識プラネット「AI桐木とその仲間たち」](https://t.zsxq.com/x1cCW)**で共有・議論されています。
>
> autoMateの技術的な詳細、開発方向性、またはより広範なAI自動化トピックに興味がある方は、QRコードをスキャンして参加し、私や他の仲間たちと一緒にautoMateの成長を目撃しましょう！

<div align="center">
<figure>
    <a href="[あなたの知識プラネットリンク]" target="_blank" rel="noopener noreferrer"><img src="./imgs/knowledge.png" width="150" height="150" alt="知識プラネットQRコード"></a>
</figure>
</div>


## 💫 コンピュータとの関係を再定義

従来のRPAツールとは異なり、autoMateは大規模言語モデルの力を活用し、自然言語でタスクを説明するだけで複雑な自動化プロセスを完了します。繰り返し作業にさようならし、本当に価値を生み出すことに集中しましょう！

**自動化で生活により多くの可能性を。**

## 💡 プロジェクト概要
autoMateは、OmniParserをベースにした革新的なAI+RPA自動化ツールで、以下のことができます：

- 📊 要件を理解し、自動的にタスクを計画
- 🔍 画面の内容をインテリジェントに理解し、人間の視覚と操作をシミュレート
- 🧠 自律的な判断を行い、タスク要件に基づいて判断と行動を実行
- 💻 ローカルデプロイメントをサポートし、データセキュリティとプライバシーを保護

## ✨ 主な機能

- 🔮 ノーコード自動化 - 自然言語でタスクを記述、プログラミング知識不要
- 🖥️ 全インターフェース制御 - 特定のソフトウェアに限定されない、あらゆる視覚的インターフェースの操作をサポート
- 🌐 マルチプラットフォームLLMサポート - OpenAI、Azure、OpenRouter、Groq、Ollama、DeepSeekなどOpenAI互換API全対応
- 🔌 MCPサーバー - MCPツールとして展開し、Claude Desktop・Cursor・Windsurf等のAIクライアントから呼び出し可能
- 🚅 簡単なインストール - ワンクリックデプロイ

## 🚀 クイックスタート

### 📥 直接使用
GitHubリリースから実行ファイルを直接ダウンロードできます。

### 📦 インストール
まずminiCondaのインストールを強く推奨します。minicondaで依存関係をインストールしてください。オンラインに多くのチュートリアルがありますが、わからない場合はAIに質問することもできます。その後、以下のコマンドで環境をセットアップします：

```bash
# プロジェクトをクローン
git clone https://github.com/yuruotong1/autoMate.git
cd autoMate
# Python 3.12環境を作成
conda create -n "automate" python==3.12
# 環境をアクティベート
conda activate automate
# 依存関係をインストール
python install.py
```

インストール後、コマンドラインでアプリケーションを起動できます：

```bash
python main.py
```

その後、ブラウザで`http://localhost:7888/`を開き、APIキーと基本設定を構成してください。

### 🔔 注意

autoMateは**任意のOpenAI互換API**をサポートしています。設定画面でBase URL・API Key・Modelを入力するだけで切り替えられます：

| プロバイダー | Base URL | モデル例 |
| --- | --- | --- |
| [OpenAI](https://platform.openai.com) | `https://api.openai.com/v1` | gpt-4o, o3 |
| [OpenRouter](https://openrouter.ai) | `https://openrouter.ai/api/v1` | claude-3.7-sonnet, gemini-2.5-pro |
| [DeepSeek](https://platform.deepseek.com) | `https://api.deepseek.com/v1` | deepseek-chat |
| [Groq](https://console.groq.com) | `https://api.groq.com/openai/v1` | llama-3.3-70b-versatile |
| [Ollama](https://ollama.com)（ローカル） | `http://localhost:11434/v1` | qwen2.5-vl, gemma3-tools:27b |
| [yeka](https://2233.ai/api)（中国プロキシ） | `https://api.2233.ai/v1` | gpt-4o, o1 |

> **推奨**：視覚対応のマルチモーダルモデルを使用すると最良の結果が得られます（`gpt-4o`、OpenRouter経由の`claude-3.7-sonnet`、またはOllama経由の`qwen2.5-vl`など）。

## 🔌 MCPサーバー

autoMateを**MCPサーバー**として展開することで、Claude Desktop・Cursor・Windsurf等のAIクライアントがツールとしてローカルデスクトップを制御できます。

### 設定方法

**1. 依存関係のインストール**
```bash
pip install -r requirements.txt
```

**2. MCPクライアント設定に追加**

Claude Desktopの場合、設定ファイルを編集します：
- macOS：`~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows：`%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "automate": {
      "command": "python",
      "args": ["/絶対パス/autoMate/mcp_server.py"],
      "env": {
        "OPENAI_API_KEY": "sk-...",
        "OPENAI_BASE_URL": "https://api.openai.com/v1",
        "OPENAI_MODEL": "gpt-4o"
      }
    }
  }
}
```

Claude Desktopを再起動すると **`run_task`** と **`screenshot`** の2つの新しいツールが追加されます。

### 利用可能なMCPツール

| ツール | 説明 |
| --- | --- |
| `run_task` | 自然言語でタスクを記述し、autoMateがデスクトップを自動操作 |
| `screenshot` | 現在の画面（または特定領域）をキャプチャしてbase64 PNGで返す |

## 📝 よくある質問
### どのモデルがサポートされていますか？
**任意のOpenAI互換API**をサポートしています。3段階フォールバック機能（構造化出力 → JSONモード → プレーンテキスト抽出）により、さまざまなプロバイダーで動作します。

**ビジョン対応のマルチモーダルモデル**の使用を推奨します（エージェントが画面を見る必要があるため）。`gpt-4o`、OpenRouter経由のClaude/Gemini、またはOllama経由の`qwen2.5-vl`が動作確認済みです。

### 実行速度が遅いのはなぜですか？
NVIDIAの専用グラフィックスカードがない場合、実行速度が遅くなります。これは、視覚的な注釈のためにOCRを頻繁に呼び出し、大量のGPUリソースを消費するためです。私たちは積極的に最適化と適応を行っています。少なくとも4GBのVRAMを持つNVIDIAグラフィックスカードの使用を推奨し、バージョンはtorchバージョンと一致している必要があります：

1. `pip list`を実行してtorchバージョンを確認
2. [公式サイト](https://pytorch.org/get-started/locally/)でサポートされているcudaバージョンを確認
3. インストールされているtorchとtorchvisionをアンインストール
4. 公式のtorchインストールコマンドをコピーし、お使いのcudaバージョンに適したtorchを再インストール

例えば、cudaバージョンが12.4の場合、以下のコマンドでtorchをインストールする必要があります：

```bash
pip3 uninstall -y torch torchvision
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

## 🤝 参加する

優れたオープンソースプロジェクトは、集団の知恵の結晶です。autoMateの成長は、あなたの参加と貢献なしには成り立ちません。バグ修正、機能追加、ドキュメント改善など、あなたの貢献は何千人もの人々が繰り返し作業から解放されるのを助けます。

よりインテリジェントな未来の創造に参加しましょう。

<a href="https://github.com/yuruotong1/autoMate/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=yuruotong1/autoMate" />
</a>

---

<div align="center">
⭐ スターは制作者への励ましであり、より多くの人々がautoMateを発見し恩恵を受ける機会です ⭐
今日のあなたのサポートが、明日の私たちの進歩の原動力です
</div>
