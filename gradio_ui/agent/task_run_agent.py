import json

from pydantic import BaseModel, Field
from gradio_ui.agent.base_agent import BaseAgent
from xbrain.core.chat import run
import platform
import re
class TaskRunAgent(BaseAgent):
    def __init__(self, config, task_plan: str, screen_info):
        super().__init__(config)
        self.OUTPUT_DIR = "./tmp/outputs"
        device = self.get_device()
        self.SYSTEM_PROMPT = system_prompt.format(task_plan=task_plan, 
                                                  device=device, 
                                                  screen_info=screen_info)

    def get_device(self):
        # 获取当前操作系统信息
        system = platform.system()
        if system == "Windows":
            device = f"Windows {platform.release()}"
        elif system == "Darwin":
            device = f"Mac OS {platform.mac_ver()[0]}"
        elif system == "Linux":
            device = f"Linux {platform.release()}"
        else:
            device = system
        return device
    
    def chat(self, task):
        res = run([{"role": "user", "content": task}], user_prompt=self.SYSTEM_PROMPT, response_format=TaskRunAgentResponse)
        return res

    def extract_data(self, input_string, data_type):
        # Regular expression to extract content starting from '```python' until the end if there are no closing backticks
        pattern = f"```{data_type}" + r"(.*?)(```|$)"
        # Extract content
        # re.DOTALL allows '.' to match newlines as well
        matches = re.findall(pattern, input_string, re.DOTALL)
        # Return the first match if exists, trimming whitespace and ignoring potential closing backticks
        return matches[0][0].strip() if matches else input_string

class TaskRunAgentResponse(BaseModel):
    reasoning: str = Field(description="描述当前屏幕上的内容，考虑历史记录，然后描述您如何实现任务的逐步思考，一次从可用操作中选择一个操作。")
    next_action: str = Field(description="一次一个操作，简短精确地描述它。")
    action_type: str = Field(
        description="选择一个操作类型",
        json_schema_extra={
            "enum": ["type", "left_click", "right_click", "double_click", 
                    "hover", "scroll_up", "scroll_down", "wait"]
        }
    )
    box_id: int = Field(description="要操作的框ID，当action_type为left_click、right_click、double_click、hover时提供，否则为None", default=None)
    value: str = Field(description="仅当action_type为type时提供，否则为None", default=None)

system_prompt = """
### 目标 ###
你正在使用{device}设备，请你根据【总体任务】、【历史操作记录】和【当前屏幕信息】确定【下一步操作】：

1. 结合【当前屏幕信息】、【历史操作记录】，思考一下当前处于【总体任务】的哪一阶段了，然后再确定【下一步操作】。

你当前的【总体任务】是：
{task_plan}

以下是检测当前屏幕上所有的【当前屏幕信息】：

{screen_info}
##########

### 注意 ###
1. 每次应该只给出一个操作。
2. 应该对当前屏幕进行分析，通过查看历史记录反思已完成的工作，然后描述您如何实现任务的逐步思考。
3. 在"Next Action"中附上下一步操作预测。
4. 不应包括其他操作，例如键盘快捷键。
5. 当任务完成时，不要完成额外的操作。你应该在json字段中说"Next Action": "None"。
6. 任务涉及购买多个产品或浏览多个页面。你应该将其分解为子目标，并按照说明的顺序一个一个地完成每个子目标。
7. 避免连续多次选择相同的操作/元素，如果发生这种情况，反思自己，可能出了什么问题，并预测不同的操作。
8. 如果您收到登录信息页面或验证码页面的提示，或者您认为下一步操作需要用户许可，您应该在json字段中说"Next Action": "None"。
9. 你只能使用鼠标和键盘与计算机进行交互。
10. 你只能与桌面图形用户界面交互（无法访问终端或应用程序菜单）。


##########
### 输出格式 ###
```json
{
    "Reasoning": str, # 描述当前屏幕上的内容，考虑历史记录，然后描述您如何实现任务的逐步思考，一次从可用操作中选择一个操作。
    "Next Action": "action_type, action description" | "None" # 一次一个操作，简短精确地描述它。
    "Box ID": n,
    "value": "xxx" # 仅当操作为type时提供value字段，否则不包括value键
}
```

【Next Action】仅包括下面之一：
- type：输入一串文本。
- left_click：将鼠标移动到框ID并左键单击。
- right_click：将鼠标移动到框ID并右键单击。
- double_click：将鼠标移动到框ID并双击。
- hover：将鼠标移动到框ID。
- scroll_up：向上滚动屏幕以查看之前的内容。
- scroll_down：当所需按钮不可见或您需要查看更多内容时，向下滚动屏幕。
- wait：等待1秒钟让设备加载或响应。

##########
### 案例 ###
一个例子：
```json
{  
    "Reasoning": "当前屏幕显示亚马逊的谷歌搜索结果，在之前的操作中，我已经在谷歌上搜索了亚马逊。然后我需要点击第一个搜索结果以转到amazon.com。",
    "Next Action": "left_click",
    "Box ID": m
}
```

另一个例子：
```json
{
    "Reasoning": "当前屏幕显示亚马逊的首页。没有之前的操作。因此，我需要在搜索栏中输入"Apple watch"。",
    "Next Action": "type",
    "Box ID": n,
    "value": "Apple watch"
}
```

另一个例子：
```json
{
    "Reasoning": "当前屏幕没有显示'提交'按钮，我需要向下滚动以查看按钮是否可用。",
    "Next Action": "scroll_down"
}
""" 

