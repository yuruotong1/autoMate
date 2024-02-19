# autoMate

autoMate是一个让大模型为你打工的工具。它能够根据你输入的任务，在网上找资料并参考优秀案例来执行任务，并最终给出一个结果。你只需要像一个老板一样反馈结果好还是坏，autoMate会自动优化方案。

如果你对 autoMate 感兴趣，欢迎加群一起讨论，群内有机器人每日推送 AI 新闻：
![](./source/group_code.jpg)

# 角色

autoMate定义了三种角色：

- 总经理：负责整体的任务管理和决策。
- 计划者：负责制定任务的具体计划和策略。
- 工人：负责执行具体的任务。

# 工作原则
人们在工作中总结了很多原则，运用这些工作原则可以大幅度提高效率、评估风险、资源管理、目标对齐。是否可以把这些原则运用在大模型中呢？让大模型像员工一样工作。

## OKR工作原则

大模型的回答内容缺少精准度，本质上是对任务理解不透彻，如何解决这个问题呢？我想到了OKR工作体系，把上层的O向下拆解成KR，并且中间不断对焦！我认为这是一个非常高效的工作体系，AutoMate 引入OKR就像是给整个团队配上了高级导航系统，各agent都能清清楚楚知道自己要完成的任务，同时不断与上级对焦能够避免任务失真。

在 o_kr.py 中定义了目标（Objective）并为每个目标关联多个关键成果（Key Results），用户可以通过实例化`OKR_Object`来创建一个目标，然后通过`add_key_result`方法添加关联的关键成果。每个关键成果的进度可以通过`set_progress`方法单独更新。目标的总体进度将根据其所有关键成果的进度自动更新，示例代码如下：

```python
from o_kr import OKR_Object, OKR_KeyResult

# 创建一个目标
objective = OKR_Object("提升品牌知名度")

# 创建关键成果并添加到目标中
kr1 = OKR_KeyResult("完成市场调研")
kr2 = OKR_KeyResult("开展线上营销活动")
objective.add_key_result(kr1)
objective.add_key_result(kr2)

# 更新关键成果的进度
kr1.set_progress(50)
kr2.set_progress(75)

# 打印目标的进度
print(objective.progress)  # 输出应该是两个关键成果进度的平均值
```

# 工具
使用selenium工具操作浏览器进行网络搜索和内容爬取。以下是一个简单的示例：

```python
from selenium import webdriver

driver = webdriver.Firefox()
driver.get("http://www.python.org")
assert "Python" in driver.title
driver.quit()
```
# 安装和运行

## 修改 config
运行前需要配置一下config.yaml文件，将目录中的config.yaml.tmp更名为config.yaml，输入你的chatgpt的api_key和api_url！


## 安装依赖
安装python的3.9+版本。

安装包依赖管理工具 poetry，打开 PowerShell 或命令提示符，使用以下命令下载并安装 Poetry：
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
python main.py
```