<div align="center"><a name="readme-top"></a>

<img src="./imgs/logo.png" width="120" height="120" alt="autoMate logo">
<h1>autoMate</h1>
<p><b>🤖 AI-powered Local Automation Tool | Make Your Computer Work For You</b></p>

[中文](./README_CN.md) | [日本語](./README_JA.md)

>"Automate the tedious, reclaim your time for life"

https://github.com/user-attachments/assets/bf27f8bd-136b-402e-bc7d-994b99bcc368


</div>

> Special Note: The autoMate project is still in a very early stage and is currently more for learning purposes. We are constantly looking for breakthroughs and continuously integrating the latest technologies! If you have any questions, you can also add WeChat friends to join the group for communication.

<div align="center">
<img src="./imgs/wxchat.png" width="120" height="120" alt="autoMate logo">
</div>


## 💫 Redefine Your Relationship with Computers

Unlike the complexity of traditional RPA tools, autoMate leverages the power of large language models to complete complex automation processes with just natural language descriptions of tasks. Say goodbye to repetitive work and focus on what truly creates value!

**Let automation create more possibilities for your life.**

## 💡 Project Introduction
autoMate is a revolutionary AI+RPA automation tool built on OmniParser that can:

- 📊 Understand your needs and automatically plan tasks
- 🔍 Intelligently comprehend screen content, simulating human vision and operations
- 🧠 Make autonomous decisions, judging and taking actions based on task requirements
- 💻 Support local deployment to protect your data security and privacy

## ✨ Features

- 🔮 No-Code Automation - Describe tasks in natural language, no programming knowledge required
- 🖥️ Full Interface Control - Support operations on any visual interface, not limited to specific software
- 🚅 Simplified Installation - Support for Chinese environment, one-click deployment


## 🚀 Quick Start

### 📥 Direct Use
You can directly download the executable file from GitHub release to use.

### 📦 Installation
It is strongly recommended to install miniConda first and use miniconda to install dependencies. There are many tutorials online; if you're still confused, you can ask AI. Then install the environment according to the following commands:

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
Launch Application

```bash
python main.py
```
Then open `http://localhost:7888/` in your browser to configure your API key and basic settings.

### 🔔 Notice
The models that have been tested and are currently supported are as follows:

> PS: The following are large language model providers that have been tested and confirmed to work. We have no business relationship with these providers, therefore we cannot guarantee after-sales service, feature assurance, or stability maintenance. Please consider carefully when using paid services.


| Vendor| Model |
| --- | --- |
|[yeka](https://2233.ai/api)|gpt-4o,o1|
|openai|gpt-4o,gpt-4o-2024-08-06,gpt-4o-2024-11-20,o1,4.gpt-4.5-preview-2025-02-27|


## 📝 FAQ
### What models are supported?
Currently, only OpenAI series models are supported. If you cannot access OpenAI from mainland China, it is recommended to use [yeka](https://2233.ai/api) as a proxy.

Why don't we support other models yet? We utilize multimodal + structured output capabilities, and few other model providers can simultaneously support these two capabilities. Adapting to other models would require significant changes to our underlying architecture, and effectiveness cannot be guaranteed. However, we are actively seeking solutions and will update as soon as progress is made.


### Why is my execution speed slow?
If your computer doesn't have an NVIDIA dedicated GPU, it will run relatively slowly because we frequently call OCR to annotate visuals, which consumes a lot of GPU resources. We are actively optimizing and adapting. It is recommended to use an NVIDIA graphics card with no less than 4GB of memory, and ensure the version is compatible with your torch version:

1. Run `pip list` to check your torch version;
2. Check supported CUDA versions from the [official website](https://pytorch.org/get-started/locally/);
3. Uninstall existing torch and torchvision;
3. Copy the official torch installation command and reinstall torch suitable for your CUDA version.

For example, if my CUDA version is 12.4, I need to install torch using the following command:

```bash
pip3 uninstall -y torch torchvision
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```


## 🤝 Contribute

Every excellent open-source project crystallizes collective wisdom. The growth of autoMate depends on your participation and contribution. Whether fixing bugs, adding features, or improving documentation, each of your efforts will help thousands of people break free from repetitive work.

Join us in creating a smarter future.

<a href="https://github.com/yuruotong1/autoMate/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=yuruotong1/autoMate" />
</a>

---

<div align="center">
⭐ Every star is encouragement for the creators and an opportunity for more people to discover and benefit from autoMate ⭐
Your support today is our motivation to move forward tomorrow
</div>
