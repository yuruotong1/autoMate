import json
import uuid
from anthropic.types.beta import BetaMessage, BetaTextBlock, BetaToolUseBlock, BetaMessageParam, BetaUsage
from PIL import ImageDraw
import base64
from io import BytesIO
from pydantic import BaseModel, Field
from gradio_ui.agent.base_agent import BaseAgent
from xbrain.core.chat import run
import platform
import re
class TaskRunAgent(BaseAgent):
    def __init__(self, output_callback):
        self.output_callback = output_callback
        self.OUTPUT_DIR = "./tmp/outputs"
       
    def __call__(self, task_plan, parsed_screen):
        screen_info = str(parsed_screen['parsed_content_list'])
        self.SYSTEM_PROMPT = system_prompt.format(task_plan=task_plan, 
                                                  device=self.get_device(), 
                                                  screen_info=screen_info)
        
        screen_width, screen_height = parsed_screen['width'], parsed_screen['height']
        img_to_show = parsed_screen["image"]
        buffered = BytesIO()
        img_to_show.save(buffered, format="PNG")
        img_to_show_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        vlm_response = run([
            {
                "role": "user", 
                "content": [
                    {"type": "text", "text": "图片是当前屏幕的截图，请根据图片以及解析出来的元素，确定下一步操作"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{img_to_show_base64}"
                        }
                    }
                ]
            }
        ], user_prompt=self.SYSTEM_PROMPT, response_format=TaskRunAgentResponse)
        vlm_response_json = json.loads(vlm_response)
        if "box_id" in vlm_response_json:
            try:
                bbox = parsed_screen["parsed_content_list"][int(vlm_response_json["box_id"])].coordinates
                vlm_response_json["box_centroid_coordinate"] = [int((bbox[0] + bbox[2]) / 2 ), int((bbox[1] + bbox[3]) / 2 )]
                x, y = vlm_response_json["box_centroid_coordinate"] 
                radius = 10
                draw = ImageDraw.Draw(img_to_show)
                draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill='red')
                draw.ellipse((x - radius*3, y - radius*3, x + radius*3, y + radius*3), fill=None, outline='red', width=2)
                buffered = BytesIO()
                img_to_show.save(buffered, format="PNG")
                img_to_show_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
            except Exception as e:
                print(f"Error parsing: {vlm_response_json}")
                print(f"Error: {e}")
        self.output_callback(f'<img src="data:image/png;base64,{img_to_show_base64}">', sender="bot")
        self.output_callback(
                    f'<details>'
                    f'  <summary>Parsed Screen elemetns by OmniParser</summary>'
                    f'  <pre>{screen_info}</pre>'
                    f'</details>',
                    sender="bot"
                )
        response_content = [BetaTextBlock(text=vlm_response_json["reasoning"], type='text')]
        if 'box_centroid_coordinate' in vlm_response_json:
            move_cursor_block = BetaToolUseBlock(id=f'toolu_{uuid.uuid4()}',
                                            input={'action': 'mouse_move', 'coordinate': vlm_response_json["box_centroid_coordinate"]},
                                            name='computer', type='tool_use')
            response_content.append(move_cursor_block)

        if vlm_response_json["next_action"] == "None":
            print("Task paused/completed.")
        elif vlm_response_json["next_action"] == "type":
            sim_content_block = BetaToolUseBlock(id=f'toolu_{uuid.uuid4()}',
                                        input={'action': vlm_response_json["next_action"], 'text': vlm_response_json["value"]},
                                        name='computer', type='tool_use')
            response_content.append(sim_content_block)
        else:
            sim_content_block = BetaToolUseBlock(id=f'toolu_{uuid.uuid4()}',
                                            input={'action': vlm_response_json["next_action"]},
                                            name='computer', type='tool_use')
            response_content.append(sim_content_block)
        response_message = BetaMessage(id=f'toolu_{uuid.uuid4()}', content=response_content, model='', role='assistant', type='message', stop_reason='tool_use', usage=BetaUsage(input_tokens=0, output_tokens=0))
        return response_message, vlm_response_json


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
    next_action: str = Field(
        description="选择一个操作类型，如果找不到合适的操作，请选择None",
        json_schema_extra={
            "enum": ["type", "left_click", "right_click", "double_click", 
                    "hover", "scroll_up", "scroll_down", "wait", "None"]
        }
    )
    box_id: int = Field(description="要操作的框ID，当next_action为left_click、right_click、double_click、hover时提供，否则为None", default=None)
    value: str = Field(description="仅当next_action为type时提供，否则为None", default=None)

system_prompt = """
### 目标 ###
你是一个自动化规划师，需要完成用户的任务。请你根据屏幕信息确定【下一步操作】，以完成任务：

你当前的任务是：
{task_plan}

以下是用yolo检测的当前屏幕上的所有元素：

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
11. 如果当前屏幕没有显示任何可操作的元素，并且当前屏幕不能下滑，请返回None。

##########
### 输出格式 ###
```json
{{
    "reasoning": str, # 描述当前屏幕上的内容，考虑历史记录，然后描述您如何实现任务的逐步思考，一次从可用操作中选择一个操作。
    "next_action": "action_type, action description" | "None" # 一次一个操作，简短精确地描述它。
    "box_id": n,
    "value": "xxx" # 仅当操作为type时提供value字段，否则不包括value键
}}
```

【next_action】仅包括下面之一：
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
{{  
    "reasoning": "当前屏幕显示亚马逊的谷歌搜索结果，在之前的操作中，我已经在谷歌上搜索了亚马逊。然后我需要点击第一个搜索结果以转到amazon.com。",
    "next_action": "left_click",
    "box_id": m
}}
```

另一个例子：
```json
{{
    "reasoning": "当前屏幕显示亚马逊的首页。没有之前的操作。因此，我需要在搜索栏中输入"Apple watch"。",
    "next_action": "type",
    "box_id": n,
    "value": "Apple watch"
}}
```

另一个例子：
```json
{{
    "reasoning": "当前屏幕没有显示'提交'按钮，我需要向下滚动以查看按钮是否可用。",
    "next_action": "scroll_down"
}}
""" 

