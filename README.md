# autoMate

autoMate是一款基于 langchain，让大模型为你打工的工具。

![](./source/main.gif)

它支持人工编排，对多种工具进行组合使用，完成但不限于以下工作

1. 能够根据你输入的任务，在网上找资料并参考优秀案例来执行任务，并最终给出一个结果。你只需要像一个老板一样反馈结果好还是坏，autoMate会自动优化方案。

如果你对 autoMate 感兴趣，欢迎加群一起讨论：

![](./source/group_code.jpg)

# 工具列表
autoMate 已经集成以下工具，工具列表会不断更新： 

1. 百度搜索引擎：使用selenium工具操作浏览器进行百度搜索，获取列表：
2. 大模型工具：利用ChatGPT进行问答；
3. 应用工具：打开指定应用；
4. 浏览器工具：打开指定网页。

# 安装和运行

## 修改 config
运行前需要配置一下config.yaml文件，将目录中的config.yaml.tmp更名为config.yaml，以下是最简配置：
```yaml
browser:
  browser_type: edge

openai:
  api_key: "key"
  api_url: "xxxx/v1/"
```

- browser.browser_type：浏览器名称，支持edge、chrome
- openai.api_key：openai 的 key
- openai.api_url：openai 的 base url

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