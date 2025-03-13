"""
Agentic sampling loop that calls the Anthropic API and local implenmentation of anthropic-defined computer use tools.
"""
from collections.abc import Callable
from time import sleep
import cv2
from gradio_ui.agent.verification_agent import VerificationAgent
from gradio_ui.agent.vision_agent import VisionAgent
from gradio_ui.tools.screen_capture import get_screenshot
from anthropic import APIResponse
from anthropic.types.beta import (
    BetaContentBlock,
    BetaMessage,
    BetaMessageParam
)
from gradio_ui.agent.task_plan_agent import TaskPlanAgent
from gradio_ui.agent.task_run_agent import TaskRunAgent
from gradio_ui.tools import ToolResult
from gradio_ui.executor.anthropic_executor import AnthropicExecutor
import numpy as np
from PIL import Image

OUTPUT_DIR = "./tmp/outputs"

def sampling_loop_sync(
    *,
    model: str,
    messages: list[BetaMessageParam],
    output_callback: Callable[[BetaContentBlock], None],
    tool_output_callback: Callable[[ToolResult, str], None],
    vision_agent: VisionAgent
):
    """
    Synchronous agentic sampling loop for the assistant/tool interaction of computer use.
    """
    print('in sampling_loop_sync, model:', model)
    task_plan_agent = TaskPlanAgent(output_callback=output_callback)
    executor = AnthropicExecutor(
        output_callback=output_callback,
        tool_output_callback=tool_output_callback,
    )
    tool_result_content = None
    plan_list = task_plan_agent(user_task = messages[-1]["content"][0].text)
    task_run_agent = TaskRunAgent(output_callback=output_callback)
    for plan in plan_list:
        parsed_screen = parse_screen(vision_agent)
        tools_use_needed, __ = task_run_agent(task_plan=plan, parsed_screen=parsed_screen)
        sleep(2)
        for message, tool_result_content in executor(tools_use_needed, messages):
            yield message
        if not tool_result_content:
            return messages
        sampling_loop_with_recovery(model, messages, vision_agent)
    
        
def parse_screen(vision_agent: VisionAgent):
    screenshot, screenshot_path = get_screenshot()
    response_json = {}
    response_json['parsed_content_list'] = vision_agent(str(screenshot_path))
    response_json['width'] = screenshot.size[0]
    response_json['height'] = screenshot.size[1]
    response_json['image'] = draw_elements(screenshot, response_json['parsed_content_list'])
    return response_json

def draw_elements(screenshot, parsed_content_list):
    """
    将PIL图像转换为OpenCV兼容格式并绘制边界框
    
    Args:
        screenshot: PIL Image对象
        parsed_content_list: 包含边界框信息的列表
    
    Returns:
        带有绘制边界框的PIL图像
    """
    # 将PIL图像转换为opencv格式
    opencv_image = np.array(screenshot)
    opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_RGB2BGR)
    # 绘制边界框
    for idx, element in enumerate(parsed_content_list):
        bbox = element.coordinates
        x1, y1, x2, y2 = bbox
        # 转换坐标为整数
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        # 绘制矩形
        cv2.rectangle(opencv_image, (x1, y1), (x2, y2), (0, 0, 255), 2)
        # 在矩形边框左上角绘制序号
        cv2.putText(opencv_image, str(idx+1), (x1, y1-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    # 将OpenCV图像格式转换回PIL格式
    opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(opencv_image)
    
    return pil_image

def sampling_loop_with_recovery(model, messages, vision_agent, max_retries=3):
    retries = 0
    
    while retries < max_retries:
        # 执行原始操作
        for message, tool_result_content in executor(tools_use_needed, messages):
            yield message
            
        if not tool_result_content:
            return messages
            
        # 验证结果
        verification_result = verification_agent(plan["expected_result"])
        
        # 如果验证成功，返回结果
        if verification_result["verification_status"] == "success":
            messages.append({
                "role": "system",
                "content": "验证成功：操作达到预期结果"
            })
            return messages
            
        # 如果验证失败，执行补救措施
        elif verification_result["verification_status"] == "error":
            retries += 1
            
            # 添加验证失败消息
            messages.append({
                "role": "system",
                "content": f"验证失败（第{retries}次尝试）：{verification_result.get('error_message', '未达到预期结果')}"
            })
            
            if retries >= max_retries:
                messages.append({
                    "role": "system",
                    "content": "达到最大重试次数，操作失败。"
                })
                return messages
                
            # 执行补救措施
            recovery_plan = generate_recovery_plan(model, messages, verification_result)
            messages.append({
                "role": "system",
                "content": f"正在执行补救措施：{recovery_plan['description']}"
            })
            
            # 执行补救操作
            for recovery_message, recovery_result in executor(recovery_plan["recovery_actions"], messages):
                yield recovery_message
                
            # 继续循环，重新验证