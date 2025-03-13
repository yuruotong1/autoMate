from gradio_ui.agent.base_agent import BaseAgent
from xbrain.core.chat import run

class TaskPlanAgent(BaseAgent):
    def __init__(self,  output_callback):
        self.output_callback = output_callback
    
    def __call__(self, user_task: str):
        self.output_callback("正在规划任务中...", sender="bot")
        response = run([{"role": "user", "content": user_task}], user_prompt=system_prompt)
        self.output_callback(response, sender="bot")
        return response

system_prompt = """
### 目标 ###
你是电脑任务规划专家，根据用户的需求，规划出要执行的任务。    
##########
### 输入 ###
用户的需求，通常是一个文本描述。
##########
### 输出 ###
一系列任务，包括任务名称
##########
### 例子 ###
（案例1）
输入：获取AI新闻
输出：
1. 打开浏览器
2. 打开百度首页
3. 搜索“AI”相关内容
4. 浏览搜索结果，记录搜索结果
5. 返回搜索内容
（案例2）
输入：删除桌面的txt文件
输出：
1. 进入桌面
2. 寻找所有txt文件
3. 右键txt文件，选择删除
"""

