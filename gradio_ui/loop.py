"""
Agentic sampling loop that calls the Anthropic API and local implenmentation of anthropic-defined computer use tools.
"""
from collections.abc import Callable
from enum import StrEnum

from anthropic import APIResponse
from anthropic.types import (
    TextBlock,
)
from anthropic.types.beta import (
    BetaContentBlock,
    BetaMessage,
    BetaMessageParam
)
from gradio_ui.tools import ToolResult

from gradio_ui.agent.llm_utils.omniparserclient import OmniParserClient
from gradio_ui.agent.vlm_agent import VLMAgent
from gradio_ui.executor.anthropic_executor import AnthropicExecutor

def sampling_loop_sync(
    *,
    model: str,
    messages: list[BetaMessageParam],
    output_callback: Callable[[BetaContentBlock], None],
    tool_output_callback: Callable[[ToolResult, str], None],
    api_response_callback: Callable[[APIResponse[BetaMessage]], None],
    api_key: str,
    only_n_most_recent_images: int | None = 2,
    max_tokens: int = 4096,
    omniparser_url: str,
    base_url: str
):
    """
    Synchronous agentic sampling loop for the assistant/tool interaction of computer use.
    """
    print('in sampling_loop_sync, model:', model)
    omniparser_client = OmniParserClient(url=f"http://{omniparser_url}/parse/")
    actor = VLMAgent(
        model=model,
        api_key=api_key,
        base_url=base_url,
        api_response_callback=api_response_callback,
        output_callback=output_callback,
        max_tokens=max_tokens,
        only_n_most_recent_images=only_n_most_recent_images
    )
    executor = AnthropicExecutor(
        output_callback=output_callback,
        tool_output_callback=tool_output_callback,
    )
    
    tool_result_content = None
    
    print(f"Start the message loop. User messages: {messages}")

    while True:
        parsed_screen = omniparser_client()
        tools_use_needed, vlm_response_json = actor(messages=messages, parsed_screen=parsed_screen)
        for message, tool_result_content in executor(tools_use_needed, messages):
            yield message
        if not tool_result_content:
            return messages