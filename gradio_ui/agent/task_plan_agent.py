import json
from pydantic import BaseModel, Field
from gradio_ui.agent.base_agent import BaseAgent
from xbrain.core.chat import run

from gradio_ui.tools.computer import Action

class TaskPlanAgent(BaseAgent):
    def __call__(self, messages, parsed_screen_result):
        messages[-1] =  {"role": "user", 
             "content": [
                    {"type": "text", "text": messages[-1]["content"]},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{parsed_screen_result['base64_image']}"}
                    }
                ]
            }
        response = run(messages, user_prompt=system_prompt.format(action_list=str(Action)), response_format=TaskPlanResponse)
        print("task_plan_agent response: ", response)
        return json.loads(response)


class TaskPlanResponse(BaseModel):
    reasoning: str = Field(description="描述您规划任务的逻辑")
    task_list: list[str] = Field(description="任务列表")


system_prompt = """
### 目标 ###
你是自动化操作规划专家，根据屏幕内容和用户需求，规划精确可执行的操作序列。


### 输入 ###
1. 用户需求：文本描述形式的任务目标
2. 当前环境：屏幕上可见的元素和状态

### 输出格式 ###
操作序列应采用以下JSON格式：
[
  {{
     "reasoning": "描述您规划任务的逻辑",
     "task_plan": ["任务1", "任务2", "任务3"]
  }}
]

任务中的操作应该仅包含：
{action_list}

### 限制 ###

- 不要说点击xx坐标，这样用户无法理解，应该说点击地址栏、搜索框、输入按钮等；


### 例子 ###
输入：获取AI新闻
输出：
[
  {{
    "reasoning": "看到有一个地址栏，所以应该在地址栏输入https://www.baidu.com",
    "task_plan": ["在地址栏输入https://www.baidu.com"]
  }},
  {{
    "reasoning": "这是百度页面，看到有一个搜索框，所以应该在搜索框输入AI最新新闻",
    "task_plan": ["在搜索框输入AI最新新闻"]
  }},
  {{
    "reasoning": "看到有一个搜索按钮，所以应该点击搜索按钮",
    "task_plan": ["点击搜索按钮"]
  }}
]
"""

