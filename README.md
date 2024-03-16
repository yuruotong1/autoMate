# autoMate
<div align="center">

<a ><img src="./source/github/logo.svg" width="120" height="120" alt="autoMate logo"></a>

# autoMate

autoMate是一个基于 LLM 大语言模型的自动化工作系统，提供开箱即用的鼠标控制、键盘控制、浏览器器控制、数据处理、模型编排、模型调用等能力。同时可以通过可视化进行工作流编排，从而实现复杂的自动化功能！
</div>

![](source/github/main.gif)

如果你对 autoMate
感兴趣，欢迎加好友一起讨论，我拉你进群。如果您有疑问，欢迎点击[链接](https://www.wolai.com/f/wVW256zr4sRbxFP2bY7FUr)给出宝贵建议：

![](source/github/wx_code.png)



相比coze、fastgpt、dify等比较成熟的LLM应用开发平台，autoMate有什么不同？

autoMate 采用了传统的C/S架构，有两种好处：
1. 这意味着它比B/S架构更接近操作系统，与操作系统距离的缩短意味着我们的Tools拥有更高的操作权限，可以实现与桌面端的程序进行无缝交互；
2. 这意味着它摆脱了浏览器限制，让应用与LLM完全融合一体，就。


它支持人工编排，对多种工具进行组合使用，完成但不限于以下工作：

1. 能够根据你输入的任务，在网上找资料并参考优秀案例来执行任务，并最终给出一个结果。你只需要像一个老板一样反馈结果好还是坏，autoMate会自动优化方案。



# 工具列表
autoMate 已经集成以下工具，工具列表会不断更新： 

1. 百度搜索引擎：使用selenium工具操作浏览器进行百度搜索，获取列表：
2. 大模型工具：利用ChatGPT进行问答；
3. 应用工具：打开指定应用；
4. 浏览器工具：利用selenium打开指定网页。

# QuickStart

## 修改 config
运行前需要配置一下config.yaml文件，将目录中的config.yaml.tmp更名为config.yaml，以下是最简配置：
```yaml
browser:
  browser_type: edge

openai:
  api_key: "key"
  api_url: "xxxx/v1/"

data_position: local
```

- browser.browser_type: 浏览器名称，支持edge、chrome；
- openai.api_key：openai 的 key；
- openai.api_url：openai 的 base url；
- data_position: 数据存储位置，如果local表示在本地存储。

## 安装依赖
1. 安装python的3.9+版本。
2. 安装包依赖管理工具 poetry，打开 PowerShell 或命令提示符，使用以下命令下载并安装 Poetry：
```cmd
curl -sSL https://install.python-poetry.org/ | python
```
配置 poetry，将虚拟环境配置到当前项目目录：
```commandline
poetry config virtualenvs.in-project true
```
创建虚拟环境并安装依赖：
```commandline
poetry env use python
poetry install
```

## 运行

运行：
```commandline
poetry run python main.py
```

# 开发进度

| 功能                      | 日期    | 进度  |
|-------------------------|-------|-----|
| 支持for循环、if分支            | 3月24日 | 开发中 |
| 支持鼠标操作、键盘的基本操作          | 3月24日 | 待完成 |
| 支持Selenium操作web浏览器的全套操作 | 3月30日 | 待完成 |
| 支持登陆场景下的所有操作            | 4月15日 | 待完成 |
| 支持基于opencv的找图定位         | 4月15日 | 待完成 |


