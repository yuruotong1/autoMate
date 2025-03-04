from collections.abc import Callable

from anthropic import APIResponse
from gradio_ui.tools import ToolResult

from gradio_ui.agent.llm_utils.omniparserclient import OmniParserClient
from gradio_ui.agent.vlm_agent import VLMAgent

def sampling_loop_sync(
    *,
    model: str,
    messages: list[BetaMessageParam],
    output_callback: Callable[[BetaContentBlock], None],
    tool_output_callback: Callable[[ToolResult, str], None],
    api_response_callback: Callable[[APIResponse[BetaMessage]], None],
    api_key: str,
    base_url: Optional(str),
    only_n_most_recent_images: int | None = 2,
    max_tokens: int = 4096,
    omniparser_url: str
):

    print('in sampling_loop_sync, model:', model)
    omniparser_client = OmniParserClient(url=f"http://{omniparser_url}/parse/")

    actor = VLMAgent(
        model=model,
        api_key=api_key,
        base_url = base_url,
        api_response_callback=api_response_callback,
        output_callback=output_callback,
        max_tokens=max_tokens,
        only_n_most_recent_images=only_n_most_recent_images,
    )
    
    print(f"Model Inited: {model}")

    print(f"Start the message loop. User messages: {messages}")

    while True:
        parsed_screen = omniparser_client()
        tools_use_needed, vlm_response_json = actor(messages=messages, parsed_screen=parsed_screen)

        for message, tool_result_content in executor(tools_use_needed, messages):
            yield message

        if not tool_result_content:
            return messages

