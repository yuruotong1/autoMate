<div align="center"><a name="readme-top"></a>

<img src="./resources/logo.png" width="120" height="120" alt="autoMate logo">
<h1>autoMate</h1>
<p><b>🤖 AI驱动的本地自动化工具 | 让电脑自己会干活</b></p>

>"让繁琐自动化，把时间还给生活"

https://github.com/user-attachments/assets/bf27f8bd-136b-402e-bc7d-994b99bcc368


</div>

> 特别声明：autoMate 项目还处于非常早期阶段，目前的能力还不足以解决任何问题，当前仅限于学习和交流。不过我会不断的寻求突破点，不停地融入最新的技术！如果你有任何疑问，也可以加vx好友，入群交流。

<div align="center">
<img src="./resources/wxchat.png" width="120" height="120" alt="autoMate logo">
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
- 🚅 简化安装 - 比官方版本更简洁的安装流程，支持中文环境，一键部署



## 🚀 快速开始

### 📦 安装
Clone项目，然后安装环境：

```bash
git clone https://github.com/yuruotong1/autoMate.git
cd autoMate
conda create -n "automate" python==3.12
conda activate automate
pip install -r requirements.txt
```
### 🎮 启动应用

```bash
python main.py
```
然后在浏览器中打开`http://localhost:7888/`，配置您的API密钥和基本设置。


目前支持的模型如下:


| Vendor| Model |
| --- | --- |
| [openainext](https://api.openai-next.com) | gpt-4o,gpt-4o-2024-08-06,gpt-4o-2024-11-20 |
|[yeka](https://2233.ai/api)|gpt-4o,o1|
|openai|gpt-4o,gpt-4o-2024-08-06,gpt-4o-2024-11-20,o1,4.gpt-4.5-preview-2025-02-27,|




## 📝常见问题

### 🔧CUDA版本不匹配问题
建议使用不少于 4G 显存的英伟达显卡运行，当然也可以用CPU运行，只是会非常慢：

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
