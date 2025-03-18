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
        screen_info = str([{"box_id": i.element_id, "caption": i.caption, "text": i.text} for i in parsed_screen_result['parsed_content_list']])
        system_prompt = prompt.format(screen_info=screen_info, task_list=formatted_task_list)
        vlm_response = run(
            messages,
            user_prompt=system_prompt, 
            response_format=create_dynamic_response_model(parsed_screen_result)
        )
        vlm_response_json = json.loads(vlm_response)
        response_content = [BetaTextBlock(text=vlm_response_json["reasoning"], type='text')]
        if "box_id" in vlm_response_json and vlm_response_json["next_action"] not in ["None", "key", "type", "scroll_down", "scroll_up","cursor_position", "wait"]:
            bbox = self.find_element_by_id(parsed_screen_result, vlm_response_json["box_id"]).coordinates
            box_centroid_coordinate = [int((bbox[0] + bbox[2]) / 2 ), int((bbox[1] + bbox[3]) / 2 )]
            move_cursor_block = BetaToolUseBlock(id=f'toolu_{uuid.uuid4()}',
                                            input={'action': 'mouse_move', 'coordinate': box_centroid_coordinate},
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
    
    def find_element_by_id(self, parsed_screen_result, box_id):
        for element in parsed_screen_result["parsed_content_list"]:
            if element.element_id == box_id:
                return element
        return None
    

def create_dynamic_response_model(parsed_screen_result):
    available_box_ids = [item.element_id for item in parsed_screen_result['parsed_content_list']]
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
            description="要操作的框ID",
            json_schema_extra={
                "enum": available_box_ids
            }
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

以下是当前屏幕上的【所有元素】，caption和text是辅助你理解当前屏幕内容的，你的决策主要依靠这两个信息截图仅限参考，图标左上角的数字为box_id：
{screen_info}

请根据以下任务列表判断一下你正在执行第几个任务（current_task_id），第一个任务是0，任务列表如下：
{task_list}
##########

### 注意 ###
- box_id 要严格参考【所有元素】中的box_id给出。
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
    "current_task_id": int # 当前正在执行第几个任务，第一个任务是0
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

