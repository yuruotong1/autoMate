<div align="center"><a name="readme-top"></a>

<img src="./imgs/logo.png" width="120" height="120" alt="autoMate logo">
<h1>autoMate</h1>
<p><b>🤖 AI-Powered Local Automation Tool | Let Your Computer Work for You</b></p>

[中文](./README_CN.md) | [日本語](./README_JA.md)

>"Automate the tedious, give time back to life"

https://github.com/user-attachments/assets/bf27f8bd-136b-402e-bc7d-994b99bcc368


</div>

> **Special Note:** The autoMate project is still in its early stages of rapid iteration, and we continue to explore and integrate the latest technologies. During this process, **deeper design thinking, technical stack discussions, challenges and solutions encountered, as well as my ongoing research notes on AI+RPA, will be primarily shared and discussed in my [Knowledge Planet "AI Tongmu and His Noble Friends"](https://t.zsxq.com/x1cCW)**.
>
> If you're interested in the technical details behind autoMate, its development direction, or broader AI automation topics, feel free to scan the QR code to join and discuss with me and other friends, witnessing the growth of autoMate together!

<div align="center">
<figure>
    <a href="[Your Knowledge Planet Link]" target="_blank" rel="noopener noreferrer"><img src="./imgs/knowledge.png" width="150" height="150" alt="Knowledge Planet QR Code"></a>
</figure>
</div>


## 💫 Redefining Your Relationship with Computers

Unlike traditional RPA tools that are cumbersome to use, autoMate leverages the power of large language models to complete complex automation processes simply by describing tasks in natural language. Say goodbye to repetitive work and focus on what truly creates value!

**Let automation create more possibilities for your life.**

## 💡 Project Introduction
autoMate is a revolutionary AI+RPA automation tool built on OmniParser that can:

- 📊 Understand your requirements and automatically plan tasks
- 🔍 Intelligently comprehend screen content, simulating human vision and operations
- 🧠 Make autonomous decisions, judging and taking actions based on task requirements
- 💻 Support local deployment, protecting your data security and privacy

## ✨ Features

- 🔮 No-Code Automation - Describe tasks in natural language, no programming knowledge required
- 🖥️ Full Interface Control - Support operations on any visual interface, not limited to specific software
- 🚅 Simplified Installation - Support for Chinese environment, one-click deployment

## 🚀 Quick Start

### 📥 Direct Usage
You can directly download the executable file from github release.

### 📦 Installation
We strongly recommend installing miniConda first and using miniconda to install dependencies. There are many tutorials available online, or you can ask AI for help. Then follow these commands to set up the environment:

```bash
# Clone the project
git clone https://github.com/yuruotong1/autoMate.git
cd autoMate
# Create python3.12 environment
conda create -n "automate" python==3.12
# Activate environment
conda activate automate
# Install dependencies
python install.py
```

After installation, you can start the application using the command line:

```bash
python main.py
```

Then open `http://localhost:7888/` in your browser to configure your API key and basic settings.

### 🔔 Note

Currently tested and supported models are as follows:

> PS: Below are the large model vendors that have been tested and are working. These vendors have no relationship with us, so we don't promise after-sales service, functional guarantees, or stability maintenance. Please consider the payment situation carefully.

| Vendor| Model |
| --- | --- |
|[yeka](https://2233.ai/api)|gpt-4o,o1|
|openai|gpt-4o,gpt-4o-2024-08-06,gpt-4o-2024-11-20,o1,4.gpt-4.5-preview-2025-02-27|

## 📝 FAQ
### What models are supported?
Currently only OpenAI series models are supported. If you can't access OpenAI in China, we recommend using [yeka](https://2233.ai/api) as a proxy.

Why don't we support other models? We use multimodal + structured output capabilities, and few other model vendors support both capabilities simultaneously. Adapting to other models would require significant changes to the underlying architecture, and we can't guarantee the results. However, we are actively looking for solutions and will update immediately when available.

### Why is my execution speed slow?
If your computer doesn't have an NVIDIA dedicated graphics card, it will run slower because we frequently call OCR for visual annotation, which consumes a lot of GPU resources. We are actively optimizing and adapting. We recommend using an NVIDIA graphics card with at least 4GB of VRAM, and the version should match your torch version:

1. Run `pip list` to check torch version;
2. Check supported cuda version from [official website](https://pytorch.org/get-started/locally/);
3. Uninstall installed torch and torchvision;
4. Copy the official torch installation command and reinstall torch suitable for your cuda version.

For example, if your cuda version is 12.4, you need to install torch using the following command:

```bash
pip3 uninstall -y torch torchvision
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

## 🤝 Join Us

Every excellent open-source project embodies collective wisdom. The growth of autoMate is inseparable from your participation and contribution. Whether it's fixing bugs, adding features, or improving documentation, your every contribution will help thousands of people break free from repetitive work.

Join us in creating a more intelligent future.

<a href="https://github.com/yuruotong1/autoMate/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=yuruotong1/autoMate" />
</a>

---

<div align="center">
⭐ Every Star is an encouragement to the creators and an opportunity for more people to discover and benefit from autoMate ⭐
Your support today is our motivation for tomorrow's progress
</div>
