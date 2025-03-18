<div align="center"><a name="readme-top"></a>

<img src="./resources/logo.png" width="120" height="120" alt="autoMate logo">
<h1>autoMate</h1>
<p><b>🤖 AI搭載ローカル自動化ツール | パソコンに仕事を任せよう</b></p>

[English](./README.md) | [简体中文](./README_CN.md)

>"面倒な作業を自動化し、人生の時間を取り戻そう"


https://github.com/user-attachments/assets/bf27f8bd-136b-402e-bc7d-994b99bcc368

</div>

> 特記事項：autoMateプロジェクトは現在、非常に初期段階にあります。現時点での機能は限定的で、主に学習とコミュニケーションを目的としています。しかし、私たちは継続的にブレークスルーを追求し、最新技術を統合しています！ご質問がありましたら、WeChatでお気軽にお問い合わせください。

<div align="center">
<img src="./resources/wxchat.png" width="120" height="120" alt="autoMate logo">
</div>

## 💫 パソコンとの関係を再定義

反復的な作業で夜遅くまで働くことに疲れていませんか？単調な作業があなたの創造性と貴重な時間を奪っていませんか？

autoMateは単なるツールではありません - AGI時代のインテリジェントなデジタル同僚として、仕事と生活のバランスを取り戻すためにたゆまぬ努力を続けています。

**自動化であなたの人生にもっと可能性を。**

## 💡 プロジェクト概要
autoMateは、OmniParserを基盤とした革新的なAI+RPA自動化ツールで、AIをあなたの「デジタル従業員」に変えます：

- 📊 パソコンインターフェースを自動操作し、複雑なワークフローを完了
- 🔍 画面の内容を知的に理解し、人間の視覚と操作をシミュレート
- 🧠 タスク要件に基づいて自律的に判断し行動
- 💻 ローカルデプロイメントでデータセキュリティとプライバシーを保護

## ✨ 特徴

- 🔮 ノーコード自動化 - 自然言語でタスクを記述、プログラミング知識不要
- 🖥️ 完全なインターフェース制御 - 特定のソフトウェアに限定されない、あらゆる視覚的インターフェースでの操作をサポート
- 🚅 簡単インストール - 公式版と比べてインストール手順を簡素化、日本語環境対応、ワンクリックデプロイメント
- 🔒 ローカル実行 - データセキュリティを保護、プライバシーの心配なし

## 🚀 クイックスタート

### 📦 インストール
プロジェクトをクローンし、環境をセットアップ：

```bash
git clone https://github.com/yuruotong1/autoMate.git
cd autoMate
conda create -n "automate" python==3.12
conda activate automate
pip install -r requirements.txt
```

### 🎮 アプリケーションの起動

```bash
python main.py
```
ブラウザで`http://localhost:7888/`を開き、APIキーと基本設定を構成してください。

## 📝 よくある質問

### 🔧 CUDAバージョンの不一致
4GB以上のVRAMを搭載したNVIDIAグラフィックスカードの使用を推奨しますが、CPU上での実行も可能です（ただし非常に遅くなります）：

1. `pip list`を実行してtorchバージョンを確認；
2. [公式サイト](https://pytorch.org/get-started/locally/)で対応するCUDAバージョンを確認；
3. 現在インストールされているtorchとtorchvisionをアンインストール；
4. 公式のtorchインストールコマンドをコピーし、お使いのCUDAバージョン用のtorchを再インストール。

例えば、CUDAバージョンが12.4の場合、以下のコマンドでtorchをインストール：

```bash
pip3 uninstall -y torch torchvision
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

現在サポートされているモデルは以下の通りです:


| Vendor| Model |
| --- | --- |
| [openainext](https://api.openai-next.com) | gpt-4o,gpt-4o-2024-08-06,gpt-4o-2024-11-20 |
|[yeka](https://2233.ai/api)|gpt-4o,o1|
|openai|gpt-4o,gpt-4o-2024-08-06,gpt-4o-2024-11-20,o1,4.gpt-4.5-preview-2025-02-27,|


## 🤝 コントリビューション

優れたオープンソースプロジェクトは集合知の結晶です。autoMateの成長はあなたの参加と貢献に依存しています。バグ修正、機能追加、ドキュメント改善など、あなたの努力は何千人もの人々を反復作業から解放することにつながります。

より知的な未来を一緒に創造しましょう。

<a href="https://github.com/yuruotong1/autoMate/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=yuruotong1/autoMate" />
</a>

---

<div align="center">
⭐ 一つ一つのスターは開発者への励みであり、より多くの人々がautoMateを発見し恩恵を受ける機会となります ⭐
今日のあなたのサポートが、私たちの明日への原動力です
</div>
