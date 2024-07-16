<div align="center"><a name="readme-top"></a>

<img src="./resources/logo.png" width="120" height="120" alt="autoMate logo">
<h1>autoMate</h1>

An Open Source Development Platform for Agent+RPA.

[![][issues-helper-image]][issues-helper-url] [![Issues need help][help-wanted-image]][help-wanted-url]


📚[Documentations](https://s0soyusc93k.feishu.cn/wiki/JhhIwAUXJiBHG9kmt3YcXisWnec?from=from_copylink)|🎞️[Introduction Video](https://www.bilibili.com/video/BV1LW421R7Ai/?share_source=copy_web&vd_source=c28e503b050f016c21660b69e391d391)|🗨[QQ Channel](https://pd.qq.com/s/1ygylejjb)

![](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

[issues-helper-image]: https://img.shields.io/badge/using-actions--cool-blue?style=flat-square
[issues-helper-url]: https://github.com/actions-cool
[help-wanted-image]: https://flat.badgen.net/github/label-issues/yuruotong1/autoMate/enhancement/open
[help-wanted-url]: https://github.com/yuruotong1/autoMate/labels/enhancement

</div>

[![](./resources/autoMate.png)](https://ant.design)


## ✨ Features

- 🌈 Generate automation code by chatting.
- 🔍 Run automation code with one click from quick search.
- 📦 Comprehensive automation toolkit
- ⚙️ Integrated framework and tools for automation development.
- 🥳 Compatible with all online and local LLMs.

## 🖥 Enviroment

- LLM APIs formatted by OpenAI.
- Refer to the following LiteLLM configuration for detailed information:

| LLMs                                                                            | [Completion](https://docs.litellm.ai/docs/#basic-usage) | [Streaming](https://docs.litellm.ai/docs/completion/stream#streaming-responses) | [Async Completion](https://docs.litellm.ai/docs/completion/stream#async-completion) | [Async Streaming](https://docs.litellm.ai/docs/completion/stream#async-streaming) | [Async Embedding](https://docs.litellm.ai/docs/embedding/supported_embedding) | [Async Image Generation](https://docs.litellm.ai/docs/image_generation) |
|-------------------------------------------------------------------------------------|---------------------------------------------------------|---------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------|-------------------------------------------------------------------------------|-------------------------------------------------------------------------|
| [openai](https://docs.litellm.ai/docs/providers/openai)                             | ✅                                                       | ✅                                                                               | ✅                                                                                   | ✅                                                                                 | ✅                                                                             | ✅                                                                       |
| [azure](https://docs.litellm.ai/docs/providers/azure)                               | ✅                                                       | ✅                                                                               | ✅                                                                                   | ✅                                                                                 | ✅                                                                             | ✅                                                                       |
| [aws - sagemaker](https://docs.litellm.ai/docs/providers/aws_sagemaker)             | ✅                                                       | ✅                                                                               | ✅                                                                                   | ✅                                                                                 | ✅                                                                             |                                                                         |
| [aws - bedrock](https://docs.litellm.ai/docs/providers/bedrock)                     | ✅                                                       | ✅                                                                               | ✅                                                                                   | ✅                                                                                 | ✅                                                                             |                                                                         |
| [google - vertex_ai](https://docs.litellm.ai/docs/providers/vertex)                 | ✅                                                       | ✅                                                                               | ✅                                                                                   | ✅                                                                                 | ✅                                                                             | ✅                                                                       |
| [google - palm](https://docs.litellm.ai/docs/providers/palm)                        | ✅                                                       | ✅                                                                               | ✅                                                                                   | ✅                                                                                 |                                                                               |                                                                         |
| [google AI Studio - gemini](https://docs.litellm.ai/docs/providers/gemini)          | ✅                                                       | ✅                                                                               | ✅                                                                                   | ✅                                                                                 |                                                                               |                                                                         |
| [mistral ai api](https://docs.litellm.ai/docs/providers/mistral)                    | ✅                                                       | ✅                                                                               | ✅                                                                                   | ✅                                                                                 | ✅                                                                             |                                                                         |
| [cloudflare AI Workers](https://docs.litellm.ai/docs/providers/cloudflare_workers)  | ✅                                                       | ✅                                                                               | ✅                                                                                   | ✅                                                                                 |                                                                               |                                                                         |
| [cohere](https://docs.litellm.ai/docs/providers/cohere)                             | ✅                                                       | ✅                                                                               | ✅                                                                                   | ✅                                                                                 | ✅                                                                             |                                                                         |
| [anthropic](https://docs.litellm.ai/docs/providers/anthropic)                       | ✅                                                       | ✅                                                                               | ✅                                                                                   | ✅                                                                                 |                                                                               |                                                                         |
| [huggingface](https://docs.litellm.ai/docs/providers/huggingface)                   | ✅                                                       | ✅                                                                               | ✅                                                                                   | ✅                                                                                 | ✅                                                                             |                                                                         |
| [replicate](https://docs.litellm.ai/docs/providers/replicate)                       | ✅                                                       | ✅                                                                               | ✅                                                                                   | ✅                                                                                 |                                                                               |                                                                         |
| [together_ai](https://docs.litellm.ai/docs/providers/togetherai)                    | ✅                                                       | ✅                                                                               | ✅                                                                                   | ✅                                                                                 |                                                                               |                                                                         |
| [openrouter](https://docs.litellm.ai/docs/providers/openrouter)                     | ✅                                                       | ✅                                                                               | ✅                                                                                   | ✅                                                                                 |                                                                               |                                                                         |
| [ai21](https://docs.litellm.ai/docs/providers/ai21)                                 | ✅                                                       | ✅                                                                               | ✅                                                                                   | ✅                                                                                 |                                                                               |                                                                         |
| [baseten](https://docs.litellm.ai/docs/providers/baseten)                           | ✅                                                       | ✅                                                                               | ✅                                                                                   | ✅                                                                                 |                                                                               |                                                                         |
| [vllm](https://docs.litellm.ai/docs/providers/vllm)                                 | ✅                                                       | ✅                                                                               | ✅                                                                                   | ✅                                                                                 |                                                                               |                                                                         |
| [nlp_cloud](https://docs.litellm.ai/docs/providers/nlp_cloud)                       | ✅                                                       | ✅                                                                               | ✅                                                                                   | ✅                                                                                 |                                                                               |                                                                         |
| [aleph alpha](https://docs.litellm.ai/docs/providers/aleph_alpha)                   | ✅                                                       | ✅                                                                               | ✅                                                                                   | ✅                                                                                 |                                                                               |                                                                         |
| [petals](https://docs.litellm.ai/docs/providers/petals)                             | ✅                                                       | ✅                                                                               | ✅                                                                                   | ✅                                                                                 |                                                                               |                                                                         |
| [ollama](https://docs.litellm.ai/docs/providers/ollama)                             | ✅                                                       | ✅                                                                               | ✅                                                                                   | ✅                                                                                 | ✅                                                                             |                                                                         |
| [deepinfra](https://docs.litellm.ai/docs/providers/deepinfra)                       | ✅                                                       | ✅                                                                               | ✅                                                                                   | ✅                                                                                 |                                                                               |                                                                         |
| [perplexity-ai](https://docs.litellm.ai/docs/providers/perplexity)                  | ✅                                                       | ✅                                                                               | ✅                                                                                   | ✅                                                                                 |                                                                               |                                                                         |
| [Groq AI](https://docs.litellm.ai/docs/providers/groq)                              | ✅                                                       | ✅                                                                               | ✅                                                                                   | ✅                                                                                 |                                                                               |                                                                         |
| [Deepseek](https://docs.litellm.ai/docs/providers/deepseek)                         | ✅                                                       | ✅                                                                               | ✅                                                                                   | ✅                                                                                 |                                                                               |                                                                         |
| [anyscale](https://docs.litellm.ai/docs/providers/anyscale)                         | ✅                                                       | ✅                                                                               | ✅                                                                                   | ✅                                                                                 |                                                                               |                                                                         |
| [IBM - watsonx.ai](https://docs.litellm.ai/docs/providers/watsonx)                  | ✅                                                       | ✅                                                                               | ✅                                                                                   | ✅                                                                                 | ✅                                                                             |                                                                         |
| [voyage ai](https://docs.litellm.ai/docs/providers/voyage)                          |                                                         |                                                                                 |                                                                                     |                                                                                   | ✅                                                                             |                                                                         |
| [xinference [Xorbits Inference]](https://docs.litellm.ai/docs/providers/xinference) |                                                         |                                                                                 |                                                                                     |                                                                                   | ✅                                                                             |                                                                         |
| [FriendliAI](https://docs.litellm.ai/docs/providers/friendliai)                              | ✅                                                       | ✅                                                                               | ✅                                                                                   | ✅                                                                                 |                                                                               |                                                                         |


## 🔗 Related Links


- [Basic Features](https://s0soyusc93k.feishu.cn/wiki/JhhIwAUXJiBHG9kmt3YcXisWnec#O9W8dEqfBo13oQxCslycFUWonFd)

- [Project Overview](https://s0soyusc93k.feishu.cn/wiki/SR9ywLMZmin7gakGo21cnyaFnRf?from=from_copylink)

## 🍬 Quick Start

Download the latest version from the release and double-click to run directly; no dependencies are required.

## ⌨️ Local LLM Application Development

This project is divided into two parts: front-end and back-end. The front-end project is in the `app` directory, and the back-end project is in the `server` directory. This means that to run autoMate, you need to start both the front-end and back-end simultaneously. The project will create an SQLite database autoMate.db in the home directory. To view the database contents, we recommend using the open-source database software `DBeaver`.

### Initiate the Front-End

1. Install Node.js (version v18.x is required).
2. Navigate to the app directory using the command line.
3. Run `npm install` to install dependencies.
4. Run `npm run dev` to initiate the front-end

### Initiate the Back-End：

1. Install Python 3, preferably version 3.9+.
2. Navigate to the `server` directory using the command line.
3. Create and activate virtual env, and run `python -m venv .venv`.
4. Run `pip install -r requirements.txt` to install the required dependencies.
5. Run `flask --app main run` to start the back-end.

### Packaging

Back-end packaging command:

`pyinstaller main.spec`

Front-end packaging command:

`npm run build:win`

After packaging, place `main.exe` in the front-end root directory.

## 🤝 Collaborations

Please refer to [Contribution Guidance](https://s0soyusc93k.feishu.cn/wiki/ZE7KwtRweicLbNkHSdMcBMTxngg?from=from_copylink).

> Highly recommended reading [HOW TO ASK QUESTIONS THE SMART WAY](https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way)、[HOW TO ASK QUESTIONS TO OPEN SOURCE COMMUNITY](https://github.com/seajs/seajs/issues/545) 和 [HOW TO REPORT BUGS EFFICIENTLY](http://www.chiark.greenend.org.uk/%7Esgtatham/bugs-cn.html)、[HOW TO SUBMIT A GOOD ISSUE TO OPEN SOURCE PROJECTS](https://zhuanlan.zhihu.com/p/25795393). Better questions are more likely to get help.

<a href="https://github.com/yuruotong1/autoMate/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=yuruotong1/autoMate" />
</a>