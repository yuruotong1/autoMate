import json
from pydantic import BaseModel, Field
from gradio_ui.agent.base_agent import BaseAgent
from xbrain.core.chat import run

class TaskPlanAgent(BaseAgent):
    def __call__(self, messages):
        response = run(messages, user_prompt=system_prompt, response_format=TaskPlanResponse)
        return json.loads(response)

class Plan(BaseModel):
    expected_result: str = Field(description="操作后的预期状态")
    error_handling: str = Field(description="操作失败时的替代方案")
    action: str = Field(description="操作类型")
    target_element: str = Field(description="操作目标元素")


class TaskPlanResponse(BaseModel):
    task_plan: list[Plan] = Field(description="具体的操作步骤序列")


system_prompt = """
### 目标 ###
你是自动化操作规划专家，根据屏幕内容和用户需求，规划精确可执行的操作序列。

### 输入 ###
1. 用户需求：文本描述形式的任务目标
2. 当前环境：屏幕上可见的元素和状态

### 输出格式 ###
操作序列应采用以下JSON格式：
[
  {
    "操作类型": "点击/输入/拖拽/等待/判断...",
    "目标元素": "元素描述或坐标",
    "参数": "具体参数，如文本内容",
    "预期结果": "操作后的预期状态",
    "错误处理": "操作失败时的替代方案"
  },
]

### 操作类型说明 ###
- 左键点击：在特定元素或坐标上执行点击
- 右键点击：在特定元素或坐标上执行右键点击
- 输入：在输入框中输入文本
- 等待：等待特定元素出现或状态变化
- 滚动：上下或左右滚动屏幕

### 例子 ###
输入：获取AI新闻
输出：
[
  {
    "操作类型": "点击",
    "目标元素": "浏览器图标",
    "参数": "无",
    "预期结果": "浏览器打开",
    "错误处理": "如未找到浏览器图标，尝试通过开始菜单搜索浏览器"
  },
  {
    "操作类型": "输入",
    "目标元素": "地址栏",
    "参数": "https://www.baidu.com",
    "预期结果": "百度首页加载完成",
    "错误处理": "如连接失败，重试或尝试其他搜索引擎"
  },
  {
    "操作类型": "输入",
    "目标元素": "搜索框",
    "参数": "AI最新新闻",
    "预期结果": "搜索框填充完成",
    "错误处理": "如搜索框不可用，尝试刷新页面"
  },
  {
    "操作类型": "点击",
    "目标元素": "搜索按钮",
    "参数": "无",
    "预期结果": "显示搜索结果页",
    "错误处理": "如点击无反应，尝试按回车键"
  },
  {
    "操作类型": "判断",
    "目标元素": "搜索结果列表",
    "参数": "包含AI相关内容",
    "预期结果": "找到相关新闻",
    "错误处理": "如无相关结果，尝试修改搜索关键词"
  }
]
"""

