<div align="center"><a name="readme-top"></a>

<img src="./resources/logo.png" width="120" height="120" alt="autoMate logo">
<h1>autoMate</h1>
<p><b>🤖 AI-Powered Local Automation Tool | Let Your Computer Work for You</b></p>

[简体中文](./README_CN.md)

>"Automate the tedious, reclaim your time for life"


https://github.com/user-attachments/assets/35969270-873f-44d7-8b26-0944c76ba9f1




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

Unlike traditional RPA tools with complicated rule settings, autoMate leverages large language models to complete complex automation processes with just natural language task descriptions. Say goodbye to repetitive work and focus on what truly creates value!

## 🌟 Why autoMate Will Transform Your Work

> "Before using autoMate, I spent 3 hours daily processing reports; now I only need 10 minutes to set up tasks and can focus on what really matters." - Feedback from a finance manager.

When you first see autoMate automatically completing tasks that used to occupy hours of your time, you'll experience an indescribable sense of relief. This isn't just about efficiency - it's about liberating your creativity.

Imagine: waking up every morning to find that last night's data organization, report generation, and email responses have all been completed, leaving you only with work that truly requires your wisdom and creativity. This is the future autoMate brings to you.

## ✨ Features

- 🔮 No-Code Automation - Use natural language to describe tasks, no programming knowledge required
- 🖥️ Full Interface Control - Support operations on any visual interface, not limited to specific software
- 🚅 Simplified Installation - Streamlined installation process compared to official version, supports Chinese environment, one-click deployment
- 🔒 Local Operation - Protect data security, no privacy concerns
- 🌐 Multi-Model Support - Compatible with mainstream large language models
- 💎 Continuous Growth - Learns and adapts to your work habits and needs as you use it

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

For supported vendors and models, please refer to this [link](./SUPPORT_MODEL.md)

## 📝 FAQ

### 🔧 CUDA Version Mismatch
If you see the error: "GPU driver incompatible, please install appropriate torch version according to readme", it indicates a driver incompatibility. You can either:

1. Run pip list to check the torch version;
2. Check supported CUDA versions on the official website;
3. Copy the official torch installation command and reinstall torch for your CUDA version.

For example, if your CUDA version is 12.4, install torch using this command:

```bash
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

## 🤝 Contributing

Every excellent open-source project embodies collective wisdom. autoMate's growth depends on your participation and contribution. Whether fixing bugs, adding features, or improving documentation, your efforts will help thousands of people break free from repetitive work.

Join us in creating a more intelligent future.

> Strongly recommend reading ["How To Ask Questions The Smart Way"](https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way), ["How to Ask Questions to Open Source Community"](https://github.com/seajs/seajs/issues/545), ["How to Report Bugs Effectively"](http://www.chiark.greenend.org.uk/%7Esgtatham/bugs.html), and ["How to Submit Unanswerable Questions to Open Source Projects"](https://zhuanlan.zhihu.com/p/25795393) for better support.

<a href="https://github.com/yuruotong1/autoMate/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=yuruotong1/autoMate" />
</a>

---

<div align="center">
⭐ Every star is an encouragement to creators and an opportunity for more people to discover and benefit from autoMate ⭐
Your support today is our motivation for tomorrow
</div>
