<div align="center"><a name="readme-top"></a>

<img src="./imgs/logo.png" width="120" height="120" alt="autoMate logo">
<h1>autoMate</h1>
<p><b>🤖 AI驱动的本地自动化工具 | 让电脑自己会干活</b></p>

[English](./README.md) | [日本語](./README_JA.md)

>"让繁琐自动化，把时间还给生活"

https://github.com/user-attachments/assets/bf27f8bd-136b-402e-bc7d-994b99bcc368


</div>

> **特别声明：** autoMate 项目仍处于快速迭代的早期阶段，我们会不断探索和融入最新技术。在这个过程中，**更深入的设计思考、技术选型讨论、遇到的挑战与解决方案，以及我对 AI+RPA 领域的持续研究笔记，会主要在我的 [知识星球「AI桐木和他的贵人们」](https://t.zsxq.com/x1cCW)** 中分享和探讨。
>
> 如果你对 autoMate 背后的技术细节、发展方向或更广泛的 AI 自动化话题感兴趣，欢迎扫码加入，与我和其他朋友一起交流，共同见证 autoMate 的成长！

<div align="center">
<figure>
    <a href="[你的知识星球链接]" target="_blank" rel="noopener noreferrer"><img src="./imgs/knowledge.png" width="150" height="150" alt="知识星球二维码"></a>
</figure>
</div>


## 💫 重新定义你与电脑的关系

不同于传统RPA工具的繁琐，autoMate借助大模型的能力，只需用自然语言描述任务，AI就能完成复杂的自动化流程。从此告别重复性工作，专注于真正创造价值的事情！

**让自动化为你的生活创造更多可能。**

## 💡 项目简介
autoMate 是一款革命性的AI+RPA自动化工具，基于OmniParser构建，它能够

- 📊 理解您的需求，自动进行任务规划
- 🔍 智能理解屏幕内容，模拟人类视觉和操作
- 🧠 自主决策，根据任务需求进行判断并采取行动
- 💻 支持本地化部署，保护您的数据安全和隐私

## ✨ 功能特点

- 🔮 无代码自动化 - 使用自然语言描述任务，无需编程知识
- 🖥️ 全界面操控 - 支持任何可视化界面的操作，不限于特定软件
- 🚅 简化安装 - 支持中文环境，一键部署


## 🚀 快速开始

### 📥 直接使用
可以直接从 github release 下载可执行文件使用。

### 📦 安装
强烈建议先安装miniConda，用miniconda安装依赖，网上有很多教程，实在不懂可以问AI。然后按照下面命令安装环境：

```bash
# 把项目拉下来
git clone https://github.com/yuruotong1/autoMate.git
cd autoMate
# 创建 python3.12 环境
conda create -n "automate" python==3.12
# 激活环境
conda activate automate
# 安装相关依赖
python install.py
```
安装完成后可以使用命令行启动应用：

```bash
python main.py
```
然后在浏览器中打开`http://localhost:7888/`，配置您的API密钥和基本设置。

### 🔔 注意

目前已经测试并且支持的模型如下：

> PS：以下是经过测试可以跑的大模型厂商，这些厂商与我们没有任何利益关系，因此我们也不承诺售后、功能保障、稳定性维护等工作，涉及付费情况请行考虑。


| Vendor| Model |
| --- | --- |
|[yeka](https://2233.ai/api)|gpt-4o,o1|
|openai|gpt-4o,gpt-4o-2024-08-06,gpt-4o-2024-11-20,o1,4.gpt-4.5-preview-2025-02-27|


## 📝常见问题
### 支持什么模型？
目前仅支持 OpenAI 系列模型，如果国内不能访问 OpenAI，建议使用[yeka](https://2233.ai/api)进行中转。

为什么目前不支持其他模型？我们用到了多模态+结构化输出能力，其他模型厂商很少能够同时支持这两个能力，如果适配其他模型的话，我们要对底层进行较大修改，效果也不能得到保证。但是我们正在积极寻找解决方案，一有更新会立即同步出来。


### 为什么我的执行速度很慢?
如果你的电脑没有NVIDIA独显的话，运行的会比较慢，因为我们会高频次调用OCR对视觉进行标注，这会消耗大量的GPU资源，我们也在积极进行优化和适配。建议使用不少于 4G 显存的英伟达显卡运行，并且版本和torch版本一致：

1. 运行`pip list`查看torch版本；
2. 从[官网](https://pytorch.org/get-started/locally/)查看支持的cuda版本；
3. 卸载已安装的 torch 和 torchvision；
3. 复制官方的 torch 安装命令，重新安装适合自己 cuda 版本的 torch。

比如我的 cuda 版本为 12.4，需要按照如下命令来安装 torch；

```bash
pip3 uninstall -y torch torchvision
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```


## 🤝 参与共建

每一个优秀的开源项目都凝聚着集体的智慧。autoMate的成长离不开你的参与和贡献。无论是修复bug、添加功能，还是改进文档，你的每一份付出都将帮助成千上万的人摆脱重复性工作的束缚。

加入我们，一起创造更加智能的未来。

<a href="https://github.com/yuruotong1/autoMate/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=yuruotong1/autoMate" />
</a>

---

<div align="center">
⭐ 每一个Star都是对创作者的鼓励，也是让更多人发现并受益于autoMate的机会 ⭐
今天你的支持，就是我们明天前进的动力
</div>
