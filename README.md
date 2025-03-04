<div align="center"><a name="readme-top"></a>

<img src="./resources/logo.png" width="120" height="120" alt="autoMate logo">
<h1>autoMate</h1>

一个基于OmniParser的AI+RPA工具，简化了官方的安装步骤，支持本地自动化。



</div>

## 安装
Clone项目，然后安装环境：

```bash
cd OmniParser
conda create -n "omni" python==3.12
conda activate omni
pip install -r requirements.txt
```

## 快速启动
```bash
python main.py
```

然后浏览器打开`http://localhost:7888/`，输入你的API KEY、Base URL等基本信息。大模型建议使用gpt-4o。

## 问题
可以通过`pip list`查看pytorch版本，然后从[官网]([官网](https://pytorch.org/get-started/locally/)查看支持的cuda版本。如果cuda不匹配就无法使用GPU，这会导致运行过程非常卡。比如如果`pip list`查看的 torch 版本为 2.6.0，那么它只支持cuda版本为11.8、12.4和12.6，请升级或者降级你的cuda版本到这几个版本。

## 🤝 参与共建

请参考[贡献指南](https://s0soyusc93k.feishu.cn/wiki/ZE7KwtRweicLbNkHSdMcBMTxngg?from=from_copylink).

> 强烈推荐阅读 [《提问的智慧》](https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way)、[《如何向开源社区提问题》](https://github.com/seajs/seajs/issues/545) 和 [《如何有效地报告 Bug》](http://www.chiark.greenend.org.uk/%7Esgtatham/bugs-cn.html)、[《如何向开源项目提交无法解答的问题》](https://zhuanlan.zhihu.com/p/25795393)，更好的问题更容易获得帮助。

<a href="https://github.com/yuruotong1/autoMate/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=yuruotong1/autoMate" />
</a>
