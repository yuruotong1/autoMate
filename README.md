<div align="center"><a name="readme-top"></a>

<img src="./resources/logo.png" width="120" height="120" alt="autoMate logo">
<h1>autoMate</h1>
<p><b>🤖 AI-Powered Local Automation Tool | Let Your Computer Work for You</b></p>

[简体中文](./README_CN.md) | [日本語](./README_JA.md)

>"Automate the tedious, reclaim your time for life"


https://github.com/user-attachments/assets/bf27f8bd-136b-402e-bc7d-994b99bcc368


</div>

> Special Note: The autoMate project is still in a very early stage. Its current capabilities are limited and it's primarily for learning and communication purposes. However, we are continuously seeking breakthroughs and integrating the latest technologies!If you have any question, add my wechat.

<div align="center">
<img src="./resources/wxchat.png" width="120" height="120" alt="autoMate logo">
</div>

## 💫 Redefining Your Relationship with Computers

Tired of working late nights on repetitive tasks? Frustrated by mundane activities consuming your creativity and precious time?

autoMate is not just another tool - it's your intelligent digital colleague for the AGI era, working tirelessly to help you restore balance between work and life.

**Let automation create more possibilities for your life.**

## 💡 Project Overview
autoMate is a revolutionary AI+RPA automation tool built on OmniParser, turning AI into your "digital employee" that can:

- 📊 Automatically operate your computer interface and complete complex workflows
- 🔍 Intelligently understand screen content, simulating human vision and operations
- 🧠 Make autonomous decisions and take actions based on task requirements
- 💻 Support local deployment to protect your data security and privacy


## ✨ Features

- 🔮 No-Code Automation - Use natural language to describe tasks, no programming knowledge required
- 🖥️ Full Interface Control - Support operations on any visual interface, not limited to specific software
- 🚅 Simplified Installation - Streamlined installation process compared to official version, supports Chinese environment, one-click deployment
- 🔒 Local Operation - Protect data security, no privacy concerns


## 🚀 Quick Start

### 📦 Installation
Clone the project and set up the environment:

```bash
git clone https://github.com/yuruotong1/autoMate.git
cd autoMate
conda create -n "automate" python==3.12
conda activate automate
pip install -r requirements.txt
```
### 🎮 Launch Application

```bash
python main.py
```
Then open `http://localhost:7888/` in your browser to configure your API key and basic settings.


Support model:


| Vendor| Model |
| --- | --- |
|[yeka](https://2233.ai/api)|gpt-4o,o1|
|openai|gpt-4o,gpt-4o-2024-08-06,gpt-4o-2024-11-20,o1,4.gpt-4.5-preview-2025-02-27,|


## 📝 FAQ

### 🔧 CUDA Version Mismatch
We recommend using an NVIDIA graphics card with at least 4GB of VRAM, although you can also run it on CPU (which will be very slow):

1. Run `pip list` to check the torch version;
2. Check supported CUDA versions on the [official website](https://pytorch.org/get-started/locally/);
3. Uninstall the currently installed torch and torchvision;
4. Copy the official torch installation command and reinstall torch for your CUDA version.

For example, if your CUDA version is 12.4, install torch using this command:

```bash
pip3 uninstall -y torch torchvision
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```


## 🤝 Contributing

Every excellent open-source project embodies collective wisdom. autoMate's growth depends on your participation and contribution. Whether fixing bugs, adding features, or improving documentation, your efforts will help thousands of people break free from repetitive work.

Join us in creating a more intelligent future.

<a href="https://github.com/yuruotong1/autoMate/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=yuruotong1/autoMate" />
</a>

---

<div align="center">
⭐ Every star is an encouragement to creators and an opportunity for more people to discover and benefit from autoMate ⭐
Your support today is our motivation for tomorrow
</div>
