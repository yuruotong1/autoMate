import json
import uuid
from anthropic.types.beta import BetaMessage, BetaTextBlock, BetaToolUseBlock, BetaMessageParam, BetaUsage
from pydantic import Field, create_model
from gradio_ui.agent.base_agent import BaseAgent
from xbrain.core.chat import run

from gradio_ui.tools.computer import Action
class TaskRunAgent(BaseAgent):
    def __init__(self):
        self.OUTPUT_DIR = "./tmp/outputs"
       
    def __call__(self, parsed_screen_result, messages):
        messages.append(
            {"role": "user", 
             "content": [
                    {"type": "text", "text": "Image is the screenshot of the current screen"},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{parsed_screen_result['base64_image']}"}
                    }
                ]
            }
        )
        task_list = json.loads(messages[1]['content'])['task_list']
        # Convert task_list to a numbered format
        formatted_task_list = "\n".join([f"{i}.{task}" for i, task in enumerate(task_list)])
        system_prompt = prompt.format(task_list=formatted_task_list)
        vlm_response = run(
            messages,
            user_prompt=system_prompt, 
            response_format=create_dynamic_response_model(parsed_screen_result)
        )
        vlm_response_json = json.loads(vlm_response)
        response_content = [BetaTextBlock(text=vlm_response_json["reasoning"], type='text')]
        # Handle cursor movement based on box_id
        if "box_id" in vlm_response_json:
            action_types_without_cursor = ["None", "key", "type", "scroll_down", "scroll_up", "cursor_position", "wait"]
            
            if vlm_response_json["box_id"] != -1 and vlm_response_json["next_action"] not in action_types_without_cursor:
                # Move cursor to the center of the identified element
                element = self.find_element_by_id(parsed_screen_result, vlm_response_json["box_id"])
                bbox = element.coordinates
                box_centroid_coordinate = [
                    int((bbox[0] + bbox[2]) / 2),
                    int((bbox[1] + bbox[3]) / 2)
                ]
                move_cursor_block = BetaToolUseBlock(
                    id=f'toolu_{uuid.uuid4()}',
                    input={'action': 'mouse_move', 'coordinate': box_centroid_coordinate},
                    name='computer', 
                    type='tool_use'
                )
                response_content.append(move_cursor_block)
            
            elif vlm_response_json["box_id"] == -1 and len(vlm_response_json["coordinates"]) == 2:
                # Move cursor to specified coordinates
                move_cursor_block = BetaToolUseBlock(
                    id=f'toolu_{uuid.uuid4()}',
                    input={'action': 'mouse_move', 'coordinate': vlm_response_json["coordinates"]},
                    name='computer', 
                    type='tool_use'
                )
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
    
    def find_element_by_id(self, parsed_screen_result, box_id):
        for element in parsed_screen_result["parsed_content_list"]:
            if element.element_id == box_id:
                return element
        return None
    

def create_dynamic_response_model(parsed_screen_result):
    available_box_ids = [item.element_id for item in parsed_screen_result['parsed_content_list']]
    available_box_ids.append(-1)
    task_run_agent_response = create_model(
        'TaskRunAgentResponse',
        reasoning = (str, Field(
            description="描述当前屏幕上的内容，考虑历史记录，然后说出你要这么做的理由。"
        )),
        next_action = (str, Field(
            description="选择一个操作类型，如果找不到合适的操作，请选择None",
            json_schema_extra={
                "enum": Action
                }
        )),
        box_id = (int, Field(
            description="要操作的框ID，如果框ID不存在就返回-1",
            json_schema_extra={
                "enum": available_box_ids
            }
        )),
        coordinates = (list[int], Field(
            description="当 box_id 为-1时，直接返回要操作对象的坐标，只返回x,y这2个整数"
        )),
        value = (str, Field(
            description="仅当next_action为type时提供，否则为None"
        )),
        current_task_id = (int, Field(
            description="请判断一下，你正在完成第几个任务，第一个任务是0"
        ))
    )
    return task_run_agent_response


prompt = """
### 目标 ###
你是一个任务执行者。请你根据屏幕截图和【所有元素】确定接下来要做什么，如果任务完成把next_action设置为None：

请根据以下任务列表判断一下你正在执行第几个任务（current_task_id），第一个任务是0，任务列表如下：
{task_list}
##########

### 注意 ###
- 要结合用户传入的屏幕图片观察其中的 box_id 框框和标号，确定要操作哪一个box_id，如果没有合适的请返回-1，然后通过coordinates给出要操作对象的坐标。
- 每次应该只给出一个操作，告诉我要对哪个box_id进行操作、输入什么内容或者滚动或者其他操作。
- 应该对当前屏幕进行分析，通过查看历史记录反思已完成的工作，然后描述您如何实现任务的逐步思考。
- 避免连续多次选择相同的操作/元素，如果发生这种情况，反思自己，可能出了什么问题，并预测不同的操作。
- 任务不是连续的，上一次是1下一次不一定是2，你要根据next_action进行判断。
- current_task_id 要在任务列表中找到，不要随便写。
- 当你觉得任务已经完成时，请一定把next_action设置为'None'，不然会重复执行。
- 涉及到输入type、key操作时，其上一步操作一定是点击输入框操作。

##########
### 输出格式 ###
```json
{{
    "reasoning": str, # 综合当前屏幕上的内容和历史记录，描述您是如何思考的。
    "next_action": str, # 要执行的动作。
    "box_id": int, # 要操作的框ID，当next_action为left_click、right_click、double_click、hover时提供，否则为None
    "value": "xxx" # 仅当操作为type时提供value字段，否则不包括value键
    "current_task_id": int # 当前正在执行第几个任务，第一个任务是0,
    "coordinates": list[int] # 仅当box_id为-1时提供，返回要操作对象的坐标，只返回x,y这2个整数
}}
```

##########
### 案例 ###
任务列表：
0. 打开浏览器
1. 搜索亚马逊
2. 点击第一个搜索结果

一个例子：
```json
{{  
    "reasoning": "当前屏幕显示亚马逊的谷歌搜索结果，在之前的操作中，我已经在谷歌上搜索了亚马逊。然后我需要点击第一个搜索结果以转到amazon.com。",
    "next_action": "left_click",
    "box_id": 35,
    "current_task_id": 0
}}
```

另一个例子：
```json
{{
    "reasoning": "当前屏幕显示亚马逊的首页。没有之前的操作。因此，我需要在搜索栏中输入"Apple watch"。",
    "next_action": "type",
    "box_id": 27,
    "value": "Apple watch",
    "current_task_id": 1
}}
```

另一个例子：
```json
{{
    "reasoning": "当前屏幕没有显示'提交'按钮，我需要向下滚动以查看按钮是否可用。",
    "next_action": "scroll_down",
    "current_task_id": 2
}}
""" 

