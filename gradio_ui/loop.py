"""
Agentic sampling loop that calls the Anthropic API and local implenmentation of anthropic-defined computer use tools.
"""
import base64
from io import BytesIO
import cv2
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
    parsed_screen_result = parsed_screen(vision_agent, screen_region)
    task_plan_agent(messages=messages, parsed_screen_result=parsed_screen_result)
    yield
    while True:    
        execute_result = execute_task_plan(vision_agent, task_run_agent, executor, messages, screen_region)
        if execute_result['next_action'] == 'None':
            break
        yield

    
def execute_task_plan(vision_agent, task_run_agent, executor, messages, screen_region):
    parsed_screen_result = parsed_screen(vision_agent, screen_region)
    tools_use_needed, vlm_response_json = task_run_agent(parsed_screen_result=parsed_screen_result, messages=messages)
    executor(tools_use_needed, messages)
    return vlm_response_json

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
        # Generate unique color for each element (using element_id as seed)
        def get_distinct_color(element_id):
            import hashlib
            # Use id to generate unique but consistent color
            hash_value = int(hashlib.md5(str(element_id).encode()).hexdigest(), 16)
            r = (hash_value & 0xFF0000) >> 16
            g = (hash_value & 0x00FF00) >> 8
            b = hash_value & 0x0000FF
            return (r, g, b)

        # Use semi-transparent effect and unique color when drawing rectangle
        color = get_distinct_color(element.element_id)
        # Draw semi-transparent rectangle (assuming there's original rectangle drawing code)
        cv2.rectangle(opencv_image, (x1, y1), (x2, y2), color, 1)  # Reduce thickness from 2 to 1

        # Calculate the size of the bounding box
        box_width = x2 - x1
        box_height = y2 - y1
        
        # Dynamically adjust font size based on box size
        # Smaller boxes get smaller text
        base_font_size = 0.5
        min_dimension = min(box_width, box_height)
        if min_dimension < 30:
            font_size = max(0.3, base_font_size * min_dimension / 30)
        else:
            font_size = base_font_size
            
        text = str(element.element_id)
        (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_size, 1)
        
        # Position text at the top-left corner with small padding
        text_x = x1 + 2
        text_y = y1 + text_height + 2
        
        # Create transparent overlay for text background (alpha blending)
        overlay = opencv_image.copy()
        cv2.rectangle(overlay, 
                     (text_x - 2, text_y - text_height - 2),
                     (text_x + text_width + 2, text_y + 2),
                     (0, 0, 0), -1)
        
        # Apply transparency (alpha value: 0.5)
        alpha = 0.5
        cv2.addWeighted(overlay, alpha, opencv_image, 1 - alpha, 0, opencv_image)
        
        # Place text at the top-left corner of the box
        cv2.putText(opencv_image, text, 
                    (text_x, text_y), 
                    cv2.FONT_HERSHEY_SIMPLEX, font_size, color, 1)
    
    # convert opencv image format back to PIL format
    opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(opencv_image)
    
    return pil_image

