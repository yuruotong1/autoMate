"""
Worker thread for handling agent operations
"""
import json
from PyQt6.QtCore import QThread, pyqtSignal

from auto_control.loop import sampling_loop_sync
from xbrain.utils.config import Config

class AgentWorker(QThread):
    """Worker thread for running agent operations asynchronously"""
    
    update_signal = pyqtSignal(list, list)
    status_signal = pyqtSignal(str)  # Signal for status updates
    task_signal = pyqtSignal(str)    # Signal for current task
    error_signal = pyqtSignal(str)   # Error signal
    
    def __init__(self, user_input, state, vision_agent):
        super().__init__()
        self.user_input = user_input
        self.state = state
        self.vision_agent = vision_agent
        
    def run(self):
        # Reset stop flag
        if self.state["stop"]:
            self.state["stop"] = False
            
        # Configure API
        config = Config()
        config.set_openai_config(
            base_url=self.state["base_url"], 
            api_key=self.state["api_key"], 
            model=self.state["model"]
        )
        
        # Add user message
        self.state["messages"].append({"role": "user", "content": self.user_input})
        self.state["chatbox_messages"].append({"role": "user", "content": self.user_input})
        
        # Send initial update
        self.update_signal.emit(self.state["chatbox_messages"], [])
        self.status_signal.emit("Starting analysis...")
        
        try:
            # Process with agent
            loop_iterator = sampling_loop_sync(
                model=self.state["model"],
                messages=self.state["messages"],
                vision_agent=self.vision_agent,
                screen_region=self.state.get("screen_region", None)
            )
            
            for _ in loop_iterator:
                # 首先检查停止标志，如果停止则立即退出循环
                if self.state["stop"]:
                    # 添加停止消息
                    self.state["chatbox_messages"].append({"role": "assistant", "content": "<span style='color:red'>⚠️ 操作已被用户停止</span>"})
                    self.status_signal.emit("操作已被用户停止")
                    # 更新UI
                    self.update_signal.emit(self.state["chatbox_messages"], 
                                      [[task["status"], task["task"]] for task in self.state["tasks"]])
                    # 立即返回，不再继续处理
                    return

                # task_plan_agent first response
                if len(self.state["messages"]) == 2:
                    task_list = json.loads(self.state["messages"][-1]["content"])["task_list"]
                    for task in task_list:
                        self.state["tasks"].append({
                            "status": "⬜",
                            "task": task
                        })
                else:
                    # Reset all task statuses
                    for i in range(len(self.state["tasks"])):
                        self.state["tasks"][i]["status"] = "⬜"
                        
                    # Update task progress
                    content_json = json.loads(self.state["messages"][-1]["content"])
                    if "current_task_id" in content_json:
                        task_completed_number = content_json["current_task_id"]
                    else:
                        task_completed_number = 0
                    
                    # Update status with reasoning
                    if "reasoning" in content_json:
                        self.status_signal.emit(content_json["reasoning"])
                    
                    # Update current task
                    if task_completed_number < len(self.state["tasks"]):
                        current_task = self.state["tasks"][task_completed_number]["task"]
                        self.task_signal.emit(current_task)
                    
                    if task_completed_number > len(self.state["tasks"]) + 1:
                        for i in range(len(self.state["tasks"])):
                            self.state["tasks"][i]["status"] = "✅"
                    else:
                        for i in range(task_completed_number + 1):
                            self.state["tasks"][i]["status"] = "✅"
                
                # Check stop flag again
                if self.state["stop"]:
                    self.state["chatbox_messages"].append({"role": "assistant", "content": "<span style='color:red'>⚠️ Operation stopped by user</span>"})
                    self.status_signal.emit("Operation stopped by user")
                    self.update_signal.emit(self.state["chatbox_messages"], 
                                        [[task["status"], task["task"]] for task in self.state["tasks"]])
                    return
                         
                # Reconstruct chat messages from original messages
                self.state["chatbox_messages"] = []
                
                for message in self.state["messages"]:
                    formatted_content, json_reasoning = self.format_message_content(message["content"])
                    
                    # Add json reasoning as a separate message if exists
                    if json_reasoning:
                        self.state["chatbox_messages"].append({
                            "role": message["role"],
                            "content": json_reasoning
                        })
                    
                    # Add formatted content
                    self.state["chatbox_messages"].append({
                        "role": message["role"],
                        "content": formatted_content
                    })
                    
                # Convert data format before returning results
                tasks_2d = [[task["status"], task["task"]] for task in self.state["tasks"]]
                self.update_signal.emit(self.state["chatbox_messages"], tasks_2d)
            
            # All done
            self.status_signal.emit("Task completed")
        
        except Exception as e:
            # Send error signal
            import traceback
            error_message = f"Error occurred: {str(e)}\n{traceback.format_exc()}"
            print(error_message)
            
            # Add error message to chat
            self.state["chatbox_messages"].append({
                "role": "assistant", 
                "content": f"<span style='color:red'>⚠️ Network connection error: {str(e)}</span><br>Please check your network connection and API settings, or try again later."
            })
            self.update_signal.emit(self.state["chatbox_messages"], 
                                   [[task["status"], task["task"]] for task in self.state["tasks"]])
            self.error_signal.emit(str(e))
            self.status_signal.emit(f"Error: {str(e)}")
            
    def format_message_content(self, content):
        """Format message content for display"""
        # Handle list-type content (multimodal)
        if isinstance(content, list):
            formatted_content = ""
            json_reasoning = None
            
            for item in content:
                if item["type"] == "image_url":
                    # Changed image style to be smaller
                    formatted_content += f'<br/><img style="width: 50%; max-width: 400px;" src="{item["image_url"]["url"]}">'
                elif item["type"] == "text":
                    if self.is_json_format(item["text"]):
                        reasoning, details = self.format_json_content(item["text"])
                        json_reasoning = reasoning
                        formatted_content += details
                    else:
                        formatted_content += item["text"]
            
            return formatted_content, json_reasoning
        
        # Handle string content
        if self.is_json_format(content):
            reasoning, _ = self.format_json_content(content)
            formatted_content = json.dumps(json.loads(content), indent=4, ensure_ascii=False)
            return formatted_content, reasoning
        
        return content, None
    
    def format_json_content(self, json_content):
        """Format JSON content with reasoning and details"""
        content_json = json.loads(json_content)
        reasoning = f'<h3>{content_json["reasoning"]}</h3>'
        details = f'<br/> <details> <summary>Detail</summary> <pre>{json.dumps(content_json, indent=4, ensure_ascii=False)}</pre> </details>'
        return reasoning, details
    
    def is_json_format(self, text):
        try:
            json.loads(text)
            return True
        except:
            return False 