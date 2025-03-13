"""
python app.py --windows_host_url localhost:8006 --omniparser_server_url localhost:8000
"""

import os
from datetime import datetime
from enum import StrEnum
from functools import partial
from pathlib import Path
from typing import cast
import argparse
import gradio as gr
from anthropic import APIResponse
from anthropic.types import TextBlock
from anthropic.types.beta import BetaMessage, BetaTextBlock, BetaToolUseBlock
from anthropic.types.tool_use_block import ToolUseBlock
from gradio_ui.agent.vision_agent import VisionAgent
from gradio_ui.loop import (
    sampling_loop_sync,
)
from gradio_ui.tools import ToolResult
import base64
from xbrain.utils.config import Config

from util.download_weights import MODEL_DIR
CONFIG_DIR = Path("~/.anthropic").expanduser()
API_KEY_FILE = CONFIG_DIR / "api_key"

INTRO_TEXT = '''
基于 Omniparser 的自动化控制桌面工具！
'''

def parse_arguments():

    parser = argparse.ArgumentParser(description="Gradio App")
    parser.add_argument("--windows_host_url", type=str, default='localhost:8006')
    parser.add_argument("--omniparser_server_url", type=str, default="localhost:8000")
    return parser.parse_args()
args = parse_arguments()


class Sender(StrEnum):
    USER = "user"
    BOT = "assistant"
    TOOL = "tool"
def setup_state(state):
    # 如果存在config，则从config中加载数据
    config = Config()
    if config.OPENAI_API_KEY:
        state["api_key"] = config.OPENAI_API_KEY
    else:
        state["api_key"] = ""
    if config.OPENAI_BASE_URL:
        state["base_url"] = config.OPENAI_BASE_URL
    else:
        state["base_url"] = "https://api.openai.com/v1"
    if config.OPENAI_MODEL:
        state["model"] = config.OPENAI_MODEL
    else:
        state["model"] = "gpt-4o"
    
    if "messages" not in state:
        state["messages"] = []
    if "auth_validated" not in state:
        state["auth_validated"] = False
    if "responses" not in state:
        state["responses"] = {}
    if "tools" not in state:
        state["tools"] = {}
    if "only_n_most_recent_images" not in state:
        state["only_n_most_recent_images"] = 2
    if 'chatbot_messages' not in state:
        state['chatbot_messages'] = []
    if 'stop' not in state:
        state['stop'] = False

async def main(state):
    """Render loop for Gradio"""
    setup_state(state)
    return "Setup completed"

def load_from_storage(filename: str) -> str | None:
    """Load data from a file in the storage directory."""
    try:
        file_path = CONFIG_DIR / filename
        if file_path.exists():
            data = file_path.read_text().strip()
            if data:
                return data
    except Exception as e:
        print(f"Debug: Error loading {filename}: {e}")
    return None

def save_to_storage(filename: str, data: str) -> None:
    """Save data to a file in the storage directory."""
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        file_path = CONFIG_DIR / filename
        file_path.write_text(data)
        # Ensure only user can read/write the file
        file_path.chmod(0o600)
    except Exception as e:
        print(f"Debug: Error saving {filename}: {e}")

def _api_response_callback(response: APIResponse[BetaMessage], response_state: dict):
    response_id = datetime.now().isoformat()
    response_state[response_id] = response

def _tool_output_callback(tool_output: ToolResult, tool_id: str, tool_state: dict):
    tool_state[tool_id] = tool_output

def chatbot_output_callback(message, chatbot_state, hide_images=False, sender="bot"):
    def _render_message(message: str | BetaTextBlock | BetaToolUseBlock | ToolResult, hide_images=False):
    
        print(f"_render_message: {str(message)[:100]}")
        
        if isinstance(message, str):
            return message
        
        is_tool_result = not isinstance(message, str) and (
            isinstance(message, ToolResult)
            or message.__class__.__name__ == "ToolResult"
        )
        if not message or (
            is_tool_result
            and hide_images
            and not hasattr(message, "error")
            and not hasattr(message, "output")
        ):  # return None if hide_images is True
            return
        # render tool result
        if is_tool_result:
            message = cast(ToolResult, message)
            if message.output:
                return message.output
            if message.error:
                return f"Error: {message.error}"
            if message.base64_image and not hide_images:
                # somehow can't display via gr.Image
                # image_data = base64.b64decode(message.base64_image)
                # return gr.Image(value=Image.open(io.BytesIO(image_data)))
                return f'<img src="data:image/png;base64,{message.base64_image}">'

        elif isinstance(message, BetaTextBlock) or isinstance(message, TextBlock):
            return f"Analysis: {message.text}"
        elif isinstance(message, BetaToolUseBlock) or isinstance(message, ToolUseBlock):
            # return f"Tool Use: {message.name}\nInput: {message.input}"
            return f"Next I will perform the following action: {message.input}"
        else:  
            return message

    def _truncate_string(s, max_length=500):
        """Truncate long strings for concise printing."""
        if isinstance(s, str) and len(s) > max_length:
            return s[:max_length] + "..."
        return s
    # processing Anthropic messages
    message = _render_message(message, hide_images)
    
    if sender == "bot":
        chatbot_state.append((None, message))
    else:
        chatbot_state.append((message, None))
    
    # Create a concise version of the chatbot state for printing
    concise_state = [(_truncate_string(user_msg), _truncate_string(bot_msg))
                        for user_msg, bot_msg in chatbot_state]
    # print(f"chatbot_output_callback chatbot_state: {concise_state} (truncated)")


def process_input(user_input, state, vision_agent_state):
    # Reset the stop flag
    if state["stop"]:
        state["stop"] = False
    config = Config()
    config.set_openai_config(base_url=state["base_url"], api_key=state["api_key"], model=state["model"])
    # Append the user message to state["messages"]
    state["messages"].append(
        {
            "role": Sender.USER,
            "content": [TextBlock(type="text", text=user_input)],
        }
    )

    # Append the user's message to chatbot_messages with None for the assistant's reply
    state['chatbot_messages'].append((user_input, None))  # 确保格式正确
    yield state['chatbot_messages']  # Yield to update the chatbot UI with the user's message
    # Run sampling_loop_sync with the chatbot_output_callback
    agent = vision_agent_state["agent"]
    for loop_msg in sampling_loop_sync(
        model=state["model"],
        messages=state["messages"],
        output_callback=partial(chatbot_output_callback, chatbot_state=state['chatbot_messages'], hide_images=False),
        tool_output_callback=partial(_tool_output_callback, tool_state=state["tools"]),
        vision_agent = agent
    ):  
        if loop_msg is None or state.get("stop"):
            yield state['chatbot_messages']
            print("End of task. Close the loop.")
            break
            
        yield state['chatbot_messages']  # Yield the updated chatbot_messages to update the chatbot UI

def stop_app(state):
    state["stop"] = True
    return "App stopped"

def get_header_image_base64():
    try:
        # Get the absolute path to the image relative to this script
        script_dir = Path(__file__).parent
        image_path = script_dir.parent / "imgs" / "header_bar_thin.png"
        
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            return f'data:image/png;base64,{encoded_string}'
    except Exception as e:
        print(f"Failed to load header image: {e}")
        return None


def run():
    with gr.Blocks(theme=gr.themes.Default()) as demo:
        gr.HTML("""
            <style>
            .no-padding {
                padding: 0 !important;
            }
            .no-padding > div {
                padding: 0 !important;
            }
            .markdown-text p {
                font-size: 18px;  /* Adjust the font size as needed */
            }
            </style>
        """)
        state = gr.State({})
        
        setup_state(state.value)
        
        header_image = get_header_image_base64()
        if header_image:
            gr.HTML(f'<img src="{header_image}" alt="autoMate Header" width="100%">', elem_classes="no-padding")
            gr.HTML('<h1 style="text-align: center; font-weight: normal;">Omni<span style="font-weight: bold;">Tool</span></h1>')
        else:
            gr.Markdown("# autoMate")

        if not os.getenv("HIDE_WARNING", False):
            gr.Markdown(INTRO_TEXT, elem_classes="markdown-text")

        with gr.Accordion("Settings", open=True): 
            with gr.Row():
                with gr.Column():
                    model = gr.Textbox(
                        label="Model",
                        value=state.value["model"],
                        placeholder="输入模型名称",
                        interactive=True,
                    )
                with gr.Column():
                    base_url = gr.Textbox(
                        label="Base URL",
                        value=state.value["base_url"],
                        placeholder="输入基础 URL",
                        interactive=True
                    )
                with gr.Column():
                    only_n_images = gr.Slider(
                        label="N most recent screenshots",
                        minimum=0,
                        maximum=10,
                        step=1,
                        value=2,
                        interactive=True
                    )
            with gr.Row():
                api_key = gr.Textbox(
                    label="API Key",
                    type="password",
                    value=state.value["api_key"],
                    placeholder="Paste your API key here",
                    interactive=True,
                )
        with gr.Row():
            with gr.Column(scale=8):
                chat_input = gr.Textbox(show_label=False, placeholder="Type a message to send to Omniparser + X ...", container=False)
            with gr.Column(scale=1, min_width=50):
                submit_button = gr.Button(value="Send", variant="primary")
            with gr.Column(scale=1, min_width=50):
                stop_button = gr.Button(value="Stop", variant="secondary")

        with gr.Row():
            with gr.Column(scale=1):
                chatbot = gr.Chatbot(
                    label="Chatbot History",
                    autoscroll=True,
                    height=580
                    )

        def update_model(model, state):
            state["model"] = model

        def update_api_key(api_key_value, state):
            state["api_key"] = api_key_value
        
        def update_base_url(base_url, state):
            state["base_url"] = base_url

        def clear_chat(state):
            # Reset message-related state
            state["messages"] = []
            state["responses"] = {}
            state["tools"] = {}
            state['chatbot_messages'] = []
            return state['chatbot_messages']

        model.change(fn=update_model, inputs=[model, state], outputs=None)
        api_key.change(fn=update_api_key, inputs=[api_key, state], outputs=None)
        chatbot.clear(fn=clear_chat, inputs=[state], outputs=[chatbot])
        vision_agent = VisionAgent(yolo_model_path=os.path.join(MODEL_DIR, "icon_detect", "model.pt"),
                                 caption_model_path=os.path.join(MODEL_DIR, "icon_caption"))
        vision_agent_state = gr.State({"agent": vision_agent})
        submit_button.click(process_input, [chat_input, state, vision_agent_state], chatbot)
        stop_button.click(stop_app, [state], None)
        base_url.change(fn=update_base_url, inputs=[base_url, state], outputs=None)
    demo.launch(server_name="0.0.0.0", server_port=7888)
