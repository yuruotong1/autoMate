"""
python app.py --windows_host_url localhost:8006 --omniparser_server_url localhost:8000
"""

import json
import os
from pathlib import Path
import argparse
import gradio as gr
from gradio_ui.agent.vision_agent import VisionAgent
from gradio_ui.loop import (
    sampling_loop_sync,
)
import base64
from xbrain.utils.config import Config
import platform

from util.download_weights import OMNI_PARSER_DIR
CONFIG_DIR = Path("~/.anthropic").expanduser()
API_KEY_FILE = CONFIG_DIR / "api_key"

INTRO_TEXT = '''
Base on Omniparser to control desktop!
'''

def parse_arguments():

    parser = argparse.ArgumentParser(description="Gradio App")
    parser.add_argument("--windows_host_url", type=str, default='localhost:8006')
    parser.add_argument("--omniparser_server_url", type=str, default="localhost:8000")
    return parser.parse_args()
args = parse_arguments()


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
    if "chatbox_messages" not in state:
        state["chatbox_messages"] = []
    if "auth_validated" not in state:
        state["auth_validated"] = False
    if "responses" not in state:
        state["responses"] = {}
    if "tools" not in state:
        state["tools"] = {}
    if "tasks" not in state:
        state["tasks"] = []
    if "only_n_most_recent_images" not in state:
        state["only_n_most_recent_images"] = 2
    if 'stop' not in state:
        state['stop'] = False
    # update state
    return (
        state["model"],      # model textbox
        state["base_url"],   # base_url textbox
        state["api_key"],    # api_key textbox
        state["chatbox_messages"],  # chatbot
        [[task["status"], task["task"]] for task in state["tasks"]]  # task_list
    )

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

def format_json_content(json_content):
    """Format JSON content with reasoning and details"""
    content_json = json.loads(json_content)
    reasoning = f'<h3>{content_json["reasoning"]}</h3>'
    details = f'<br/> <details> <summary>Detail</summary> <pre>{json.dumps(content_json, indent=4, ensure_ascii=False)}</pre> </details>'
    return reasoning, details

def format_message_content(content):
    """Format message content for gradio chatbox display"""
    # Handle list-type content (multimodal)
    if isinstance(content, list):
        formatted_content = ""
        json_reasoning = None
        
        for item in content:
            if item["type"] == "image_url":
                formatted_content += f'<br/><img style="width: 100%;" src="{item["image_url"]["url"]}">'
            elif item["type"] == "text":
                if is_json_format(item["text"]):
                    reasoning, details = format_json_content(item["text"])
                    json_reasoning = reasoning
                    formatted_content += details
                else:
                    formatted_content += item["text"]
        
        return formatted_content, json_reasoning
    
    # Handle string content
    if is_json_format(content):
        reasoning, _ = format_json_content(content)
        formatted_content = json.dumps(json.loads(content), indent=4, ensure_ascii=False)
        return formatted_content, reasoning
    
    return content, None

def process_input(user_input, state, vision_agent_state):
    # Reset the stop flag
    if state["stop"]:
        state["stop"] = False
        
    # Configure API
    config = Config()
    config.set_openai_config(base_url=state["base_url"], api_key=state["api_key"], model=state["model"])
    
    # Add user message
    state["messages"].append({"role": "user", "content": user_input})
    state["chatbox_messages"].append({"role": "user", "content": user_input})
    yield state["chatbox_messages"], []
    # Process with agent
    agent = vision_agent_state["agent"]
    for _ in sampling_loop_sync(
        model=state["model"],
        messages=state["messages"],
        vision_agent=agent,
        screen_region=state.get("screen_region", None)
    ):
        if state["stop"]:
            state["chatbox_messages"].append({"role": "user", "content": "Stop !"})
            return

        # task_plan_agent first response
        if len(state["messages"]) == 2:
            task_list = json.loads(state["messages"][-1]["content"])["task_list"]
            for task in task_list:
                state["tasks"].append({
                    "status": "⬜",
                    "task": task
                })
        else:
            # Reset all tasks to pending status
            for i in range(len(state["tasks"])):
                state["tasks"][i]["status"] = "⬜"
            task_completed_number = json.loads(state["messages"][-1]["content"])["current_task_id"]
            if task_completed_number > len(state["tasks"]) + 1:
                for i in range(len(state["tasks"])):
                    state["tasks"][i]["status"] = "✅"
            else:
                for i in range(task_completed_number + 1):
                    state["tasks"][i]["status"] = "✅"
                 
        # Rebuild chatbox messages from the original messages
        state["chatbox_messages"] = []
        
        for message in state["messages"]:
            formatted_content, json_reasoning = format_message_content(message["content"])
            
            # Add json reasoning as a separate message if exists
            if json_reasoning:
                state["chatbox_messages"].append({
                    "role": message["role"],
                    "content": json_reasoning
                })
            
            # Add the formatted content
            state["chatbox_messages"].append({
                "role": message["role"],
                "content": formatted_content
            })
            
        # 在返回结果前转换数据格式
        tasks_2d = [[task["status"], task["task"]] for task in state["tasks"]]
        yield state["chatbox_messages"], tasks_2d

def is_json_format(text):
    try:
        json.loads(text)
        return True
    except:
        return False

def stop_app(state):
    state["stop"] = True
    return

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
    
def _get_region(queue):
    from util.screen_selector import ScreenSelector
    region = ScreenSelector().get_selection()
    queue.put(region)


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
            gr.HTML('<h1 style="text-align: center; font-weight: normal;">autoMate</h1>')
        else:
            gr.Markdown("# autoMate")

        if not os.getenv("HIDE_WARNING", False):
            gr.Markdown(INTRO_TEXT, elem_classes="markdown-text")

        with gr.Accordion("Settings", open=True): 
            with gr.Row():
                with gr.Column():
                    with gr.Row():
                        with gr.Column():
                            model = gr.Textbox(
                                label="Model",
                                value=state.value["model"],
                                placeholder="Input model name",
                                interactive=True,
                            )
                        with gr.Column():
                            base_url = gr.Textbox(
                                label="Base URL",
                                value=state.value["base_url"],
                                placeholder="input base url",
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

                with gr.Column():
                        select_region_btn = gr.Button(value="Select Screen Region", variant="primary")
                        def select_screen_region(state):
                            from util.screen_selector import ScreenSelector
                            region = ScreenSelector().get_selection()
                            if region:
                                state["screen_region"] = region
                                return f"Selected region: {region}"
                            return "Selection cancelled"

                        def select_screen_region_mac(state):
                            import multiprocessing as mp
                            ctx = mp.get_context('spawn')
                            queue = ctx.Queue()
                            
                            p = ctx.Process(target=_get_region, args=(queue,))
                            p.start()
                            p.join()  
                            
                            region = queue.get() if not queue.empty() else None
                            
                            if region:
                                state["screen_region"] = region
                                return f"Selected region: {region}"
                            return "Selection cancelled"

                        if platform.system() == 'Darwin':
                            select_region_btn.click(fn=select_screen_region_mac, inputs=[state], outputs=[gr.Textbox(label="Region Info")])
                        else:
                            select_region_btn.click(fn=select_screen_region_mac, inputs=[state], outputs=[gr.Textbox(label="Region Info")])
        with gr.Row():
            with gr.Column(scale=8):
                chat_input = gr.Textbox(show_label=False, placeholder="Type a message to send to Omniparser + X ...", container=False)
            with gr.Column(scale=1, min_width=50):
                submit_button = gr.Button(value="Send", variant="primary")
            with gr.Column(scale=1, min_width=50):
                stop_button = gr.Button(value="Stop", variant="secondary")

        with gr.Row():
            with gr.Column(scale=2):
                task_list = gr.Dataframe(
                    headers=["status", "task"],
                    datatype=["str", "str"],
                    value=[],
                    label="Task List",
                    interactive=False)
                
            with gr.Column(scale=8):
                chatbot = gr.Chatbot(
                    label="Chatbot History",
                    autoscroll=True,
                    height=580,
                    type="messages")
                
        def update_model(model, state):
            state["model"] = model

        def update_api_key(api_key_value, state):
            state["api_key"] = api_key_value
        
        def update_base_url(base_url, state):
            state["base_url"] = base_url

        def clear_chat(state):
            # Reset message-related state
            state["messages"] = []
            state["chatbox_messages"] = []
            state["responses"] = {}
            state["tools"] = {}
            state["tasks"] = []
            return state["chatbox_messages"]

        model.change(fn=update_model, inputs=[model, state], outputs=None)
        api_key.change(fn=update_api_key, inputs=[api_key, state], outputs=None)
        chatbot.clear(fn=clear_chat, inputs=[state], outputs=[chatbot])
        vision_agent = VisionAgent(yolo_model_path=os.path.join(OMNI_PARSER_DIR, "icon_detect", "model.pt"))
        vision_agent_state = gr.State({"agent": vision_agent})
        submit_button.click(process_input, [chat_input, state, vision_agent_state], [chatbot, task_list])
        stop_button.click(stop_app, [state], None)
        base_url.change(fn=update_base_url, inputs=[base_url, state], outputs=None)

        demo.load(
            setup_state, 
            inputs=[state], 
            outputs=[model, base_url, api_key, chatbot, task_list]
        )
        demo.launch(server_name="0.0.0.0", quiet=True, server_port=7888, prevent_thread_lock=True)

        BLUE = "\033[34m"
        BOLD = "\033[1m"
        UNDERLINE = "\033[4m"
        RESET = "\033[0m"

        print(f"\n\n🚀 Server is running at: {BLUE}{BOLD}{UNDERLINE}http://127.0.0.1:7888{RESET}")
    
        import time
        try:
            while True:
                time.sleep(1) 
        except KeyboardInterrupt:
            print("\n💤 closing server")
