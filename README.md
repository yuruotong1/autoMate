<div align="center"><a name="readme-top"></a>

<img src="./resources/logo.png" width="120" height="120" alt="autoMate logo">
<h1>autoMate</h1>

一个 Agent 和 RPA 开发平台
[![][issues-helper-image]][issues-helper-url] [![Issues need help][help-wanted-image]][help-wanted-url]


📚[文档地址](https://s0soyusc93k.feishu.cn/wiki/JhhIwAUXJiBHG9kmt3YcXisWnec?from=from_copylink)|🎞️[介绍视频](https://www.bilibili.com/video/BV1LW421R7Ai/?share_source=copy_web&vd_source=c28e503b050f016c21660b69e391d391)

![](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

[issues-helper-image]: https://img.shields.io/badge/using-actions--cool-blue?style=flat-square
[issues-helper-url]: https://github.com/actions-cool
[help-wanted-image]: https://flat.badgen.net/github/label-issues/yuruotong1/autoMate/enhancement/open
[help-wanted-url]: https://github.com/yuruotong1/autoMate/labels/enhancement

</div>

[![](./resources/autoMate.png)](https://ant.design)


## ✨ 特性

- 🌈 聊聊天就能生成自动化代码。
- 🔍 快捷键呼出搜索框一键运行自动化代码。
- 📦 开箱即用的自动化工具套件。
- ⚙️ 自动化开发框架和工具配套。
- 🥳 兼容所有在线和本地大模型。


## 🔗 链接


- [基础功能](https://s0soyusc93k.feishu.cn/wiki/JhhIwAUXJiBHG9kmt3YcXisWnec#O9W8dEqfBo13oQxCslycFUWonFd)

## ⌨️ 本地开发

本项目分为前端和后端两个部分，前端项目在 app  目录下，后端项目在 server 目录下。这意味着，如果要运行 autoMate，你就得同时启动前端和后端。项目启动后会在～ 目录创建 sqlite 数据库 autoMate.db ，如果想查看数据库内容，建议使用开源数据库软件dbeaver。

### 启动前端

1. 安装 nodejs，使用最新版本即可；
2. 使用命令行进入到 app 目录；
3. 输入 npm install 安装依赖；
4. 输入 npm run dev 启动前端。

### 启动后端：

1. 安装python3，最好 3.9+版本。
2. 使用命令行进入 server 目录；
3. 创建并激活虚拟环境，输入 python -m venv .venv；
4. 输入 pip install -r requirements.txt 安装依赖；
5. 输入 flask --app main run 启动后端

### 打包

后端打包命令：

`pyinstaller main.spec`

前端打包命令：

`npm run build:win`

打包完成后，将main.exe放在前端根目录下。

## 🤝 参与共建


<a href="https://github.com/yuruotong1/autoMate/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=yuruotong1/autoMate" />
</a>