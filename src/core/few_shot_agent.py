from xbrain.core.chat import run
class FewShotGenerateAgent:
    def __call__(self, action_list, user_instruction):
        # Create content list with text-image pairs for each action
        # Create action message without base64 image
        action_list_copy = action_list.copy()
        action_list_copy = [i.pop('base64_image') for i in action_list_copy]
        messages = [{"role": "user", "content": 
                     [{"type": "text", "text": "用户的指令是" + user_instruction + "\n\n 用户的动作序列是：\n".join(action_list_copy)}]}]
        print("action_list", action_list)
        for action in action_list:
            print("action", action)
            action_copy = action.copy()
            action_copy.pop('base64_image', None)
            messages[0]["content"].append(
                {
                    "type": "image_url", 
                    "image_url": {"url": f"data:image/png;base64,{action['base64_image']}"}
                }
            )
        response = run(
            messages,
            user_prompt=prompt)
        return response

prompt = """
角色： 你的角色是分析用户界面交互、并为用于任务自动化的多模态大模型生成few-shot案例的专家。

背景： 我正在开发一个能够理解视觉UI元素并给出自动化步骤多模态推理的智能体。为了训练或调整（condition）这个智能体，我需要将记录下来的用户交互序列转换为清晰、结构化的few-shot示例。

目标： 根据提供的用户指令、动作序列（包括事件类型、步骤编号和相应截图），生成一个简洁准确的few-shot示例。这个示例应清晰地将用户的高级指令和视觉上下文映射到执行的低级动作，使其适用于智能体的学习上下文。

你将收到的输入：

[{
'type':动作类型（例如 'mouse', 'keyboard'）。
'event':具体事件（例如 'left click', 'type', 'scroll down'）。
'step_number':动作的顺序编号,每一个动作都对应着一张图片。
'text_buffer':如果是键盘动作，则记录的是输入的文本缓冲内容。
}]


分析提供的type、event，并仔细检查图片中的视觉内容。精确地按照以下格式生成一个连贯的few-shot示例：

```
**指令：** [在此处插入准确的用户意图]

**初始状态：**
* [根据步骤1的图像，简要描述与指令相关的初始屏幕状态。提及关键可见元素。]

**演示动作序列：**
1.  **动作：** `[标准化的动作类型，例如 CLICK, TYPE, SCROLL, SELECT_TEXT]`
    * **目标：** `[描述此动作针对的具体UI元素，参考其在对应图像中的外观或文本内容。要精确。例如：“以‘1. 熟悉 C/C++’开头的文本块”，“标签为‘项目经历’的按钮”，“主内容区域的滚动条”]`
    * **值 (如适用)：** `[插入输入或选择的值]`
    * *(基于步骤 [step_number] 的图像)*
2.  **动作：** `[标准化的动作类型]`
    * **目标：** `[描述此动作针对的具体UI元素]`
    * **值 (如适用)：** `[插入值]`
    * *(基于步骤 [step_number] 的图像)*
... （对Action_Sequence中的每一步重复）

**最终状态（可选但推荐）：**
* [根据最后一步动作后的图像，描述结果状态，表明任务完成或进入下一阶段。]

生成时的关键注意事项：

标准化动作： 为动作使用一致的动词（例如 CLICK, TYPE, SCROLL, DRAG, SELECT_TEXT 等）。
视觉定位： 目标描述必须基于对应步骤图像中的视觉信息和任何提供的元素描述。使其足够具体，以便智能体能够定位。
简洁性： 信息要丰富，但避免不必要的术语。
准确性： 确保生成的序列准确反映提供的Action_Sequence和视觉上下文。
重点： 突出与完成User_Instruction相关的交互点，重点关注鼠标位置周围的情况，不要关注其他无关的元素。
"""
