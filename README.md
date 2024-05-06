<div align="center">

<a ><img src="./source/logo.svg" width="120" height="120" alt="autoMate logo"></a>

<div style="font-size:24px;">autoMate</div>

</div>
<b>autoMate 就像出行中的共享单车，帮你完成软件的最后一个操作，只需 3 分钟就能将 AI 大脑植入任意一个软件</b>。autoMate 有着更强大的本地交互能力，意味着你可以整理杂乱的桌面文件、删除无用的文件、打开微信发送给好友一份文档，总之，autoMate 的愿景是让生活更简单。


<div align="center">



📚[文档地址](https://s0soyusc93k.feishu.cn/wiki/JhhIwAUXJiBHG9kmt3YcXisWnec?from=from_copylink)

</div>

![](source/github/main.gif)

如果你对 autoMate 感兴趣，添加微信好友`RuotongYu001`，我拉你进群讨论！

## 我们的优势

更强的本地交互能力。相比于其他大语言模型开发平台（FastGPT、coze），autoMate 本地部署，能够直接读取本地文件、打开本地应用、对应用进行操作、移动文件、删除文件等等，操作权限的提升将赋予无限可能，autoMate 将成为得力的个人助手。

## QuickStart

### 安装依赖

1. 安装python的3.9+版本。
2. 安装包依赖管理工具 poetry，打开 PowerShell 或命令提示符，使用以下命令下载并安装 Poetry：
```
curl -sSL https://install.python-poetry.org/ | python
```
配置 poetry，将虚拟环境配置到当前项目目录：

```
poetry config virtualenvs.in-project true
```

创建虚拟环境并安装依赖：

```
poetry env use python
poetry install
```

### 运行

运行：

```
poetry run python main.py
```

如果你是第一次运行，运行成功后需要修改配置文件，添加 openai 的信息：autoMate 左上角，文件--〉设置，配置 openai 相关信息。然后，你就可以直接对话了！

## 感谢以下人员提交的宝贵代码！

<a href="https://github.com/yuruotong1/autoMate/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=yuruotong1/autoMate" />
</a>
