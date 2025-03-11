"""
Agentic sampling loop that calls the Anthropic API and local implenmentation of anthropic-defined computer use tools.
"""
import base64
from collections.abc import Callable
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
from gradio_ui.agent.llm_utils.utils import encode_image
from gradio_ui.agent.llm_utils.omniparserclient import OmniParserClient
from gradio_ui.agent.vlm_agent import VLMAgent
from gradio_ui.executor.anthropic_executor import AnthropicExecutor
from pathlib import Path
OUTPUT_DIR = "./tmp/outputs"

def sampling_loop_sync(
    *,
    model: str,
    messages: list[BetaMessageParam],
    output_callback: Callable[[BetaContentBlock], None],
    tool_output_callback: Callable[[ToolResult, str], None],
    api_response_callback: Callable[[APIResponse[BetaMessage]], None],
    api_key: str,
    only_n_most_recent_images: int | None = 0,
    max_tokens: int = 4096,
    omniparser_url: str,
    base_url: str,
    vision_agent: VisionAgent
):
    """
    Synchronous agentic sampling loop for the assistant/tool interaction of computer use.
    """
    print('in sampling_loop_sync, model:', model)
    # omniparser_client = OmniParserClient(url=f"http://{omniparser_url}/parse/")
    task_plan_agent = TaskPlanAgent()
    # actor = VLMAgent(
    #     model=model,
    #     api_key=api_key,
    #     base_url=base_url,
    #     api_response_callback=api_response_callback,
    #     output_callback=output_callback,
    #     max_tokens=max_tokens,
    #     only_n_most_recent_images=only_n_most_recent_images
    # )
    executor = AnthropicExecutor(
        output_callback=output_callback,
        tool_output_callback=tool_output_callback,
    )
    tool_result_content = None
    plan = task_plan_agent(user_task = messages[-1]["content"][0].text)
    task_run_agent = TaskRunAgent()


    while True:
        parsed_screen = parse_screen(vision_agent)
        tools_use_needed, __ = task_run_agent(task_plan=plan, parsed_screen=parsed_screen)
        for message, tool_result_content in executor(tools_use_needed, messages):
            yield message
        if not tool_result_content:
            return messages
        
def parse_screen(vision_agent: VisionAgent):
    screenshot, screenshot_path = get_screenshot()
    response_json = {}
    response_json['parsed_content_list'] = vision_agent(str(screenshot_path))
    response_json['width'] = screenshot.size[0]
    response_json['height'] = screenshot.size[1]
    return response_json
