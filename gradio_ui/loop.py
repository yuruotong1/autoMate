"""
Agentic sampling loop that calls the Anthropic API and local implenmentation of anthropic-defined computer use tools.
"""
import base64
from io import BytesIO
from time import sleep
import cv2
from gradio_ui.agent.verification_agent import VerificationAgent
from gradio_ui.agent.vision_agent import VisionAgent
from gradio_ui.tools.screen_capture import get_screenshot
from anthropic.types.beta import (BetaMessageParam)
from gradio_ui.agent.task_plan_agent import TaskPlanAgent
from gradio_ui.agent.task_run_agent import TaskRunAgent
from gradio_ui.executor.anthropic_executor import AnthropicExecutor
import numpy as np
from PIL import Image

OUTPUT_DIR = "./tmp/outputs"

def sampling_loop_sync(
    *,
    model: str,
    messages: list[BetaMessageParam],
    vision_agent: VisionAgent,
    screen_region: tuple[int, int, int, int]
):
    """
    Synchronous agentic sampling loop for the assistant/tool interaction of computer use.
    """
    print('in sampling_loop_sync, model:', model)
    task_plan_agent = TaskPlanAgent()
    executor = AnthropicExecutor()
    task_run_agent = TaskRunAgent()
    parsed_screen_result = parsed_screen(vision_agent)
    plan_list = task_plan_agent(messages=messages, parsed_screen_result=parsed_screen_result)
    yield
    for plan in plan_list:      
        execute_task_plan(plan, vision_agent, task_run_agent, executor, messages)
        yield

    
def execute_task_plan(plan, vision_agent, task_run_agent, executor, messages):
    parsed_screen_result = parsed_screen(vision_agent)
    tools_use_needed, __ = task_run_agent(task_plan=plan, parsed_screen_result=parsed_screen_result, messages=messages)
    executor(tools_use_needed, messages)

def parsed_screen(vision_agent: VisionAgent, screen_region: tuple[int, int, int, int] = None):
    screenshot, screenshot_path = get_screenshot(screen_region)
    response_json = {}
    response_json['parsed_content_list'] = vision_agent(str(screenshot_path))
    response_json['width'] = screenshot.size[0]
    response_json['height'] = screenshot.size[1]
    response_json['image'] = draw_elements(screenshot, response_json['parsed_content_list'])
    buffered = BytesIO()
    response_json['image'].save(buffered, format="PNG")
    response_json['base64_image'] = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return response_json

def draw_elements(screenshot, parsed_content_list):
    """
    Convert PIL image to OpenCV compatible format and draw bounding boxes
    
    Args:
        screenshot: PIL Image object
        parsed_content_list: list containing bounding box information
    
    Returns:
        PIL image with drawn bounding boxes
    """
    # convert PIL image to opencv format
    opencv_image = np.array(screenshot)
    opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_RGB2BGR)
    # draw bounding boxes
    for element in parsed_content_list:
        bbox = element.coordinates
        x1, y1, x2, y2 = bbox
        # convert coordinates to integers
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        # draw rectangle
        cv2.rectangle(opencv_image, (x1, y1), (x2, y2), (0, 0, 255), 2)
        # draw index number
        cv2.putText(opencv_image, str(element.element_id), (x1, y1-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    # convert opencv image format back to PIL format
    opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(opencv_image)
    
    return pil_image

