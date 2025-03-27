"""
Conversation manager module for handling dialog flow and states
"""
import json
import time
from PyQt6.QtCore import QObject, QThread, QTimer
from src.core.few_shot_agent import FewShotGenerateAgent
from src.core.input_listener import InputListener
from xbrain.core.chat import run
import multiprocessing
from multiprocessing import Process, Queue, Manager



class ConversationManager(QObject):
    """
    Manages conversation state and process user interactions
    """
    def __init__(self, chat_area, mini_window):
        """
        Initialize the conversation manager
        
        Args:
            chat_area: ChatArea widget to display messages
            mini_window: MiniWindow for demonstration mode
        """
        super().__init__()
        self.chat_area = chat_area
        self.mini_window = mini_window
        
        # Initialize state
        self.conversation_state = "greeting"
        self.task_demonstration = []
        self.is_recording = False
        self.text_buffer = ""
        self.last_keypress_time = 0
        self.step_counter = 0  # Add step counter
        self.agent_queue = Queue()
        self.agent_process = None
        self.analysis_results = {}  # Store analysis results by step number
        self.pool = multiprocessing.Pool(processes=1)  # 使用进程池
        
        # 使用Manager创建共享字典
        self.manager = Manager()
        self.analysis_results = self.manager.dict()
        self.pool = multiprocessing.Pool(processes=1)
        self.user_instruction = ""
        # Start the conversation
        self.start_conversation()
    
    def start_conversation(self):
        """Initialize the conversation with a greeting"""
        greeting = "Hello! I'm Xiao Hong, 23 years old, recently graduated from East China Normal University " + \
                  "with a Computer Science degree. I'm skilled in data analysis and document processing, " + \
                  "and have a positive and detail-oriented personality. Looking forward to working with you!"
        self.chat_area.add_message("Xiao Hong", greeting)
        self.chat_area.add_message("System", "Please enter your response...")
    
    def process_message(self, message):
        """
        Process incoming user message based on conversation state
        
        Args:
            message: Text message from user
        """
        # Add user message to chat
        self.chat_area.add_message("You", message, True)
        
        # Process message based on current state
        if self.conversation_state == "greeting":
            self.handle_greeting_response(message)
        elif self.conversation_state == "ask_for_demo":
            self.handle_demo_request(message)
        elif self.conversation_state == "ready":
            self.handle_ready_state(message)
    
    def handle_greeting_response(self, message):
        """Handle user's response to the initial greeting"""
        response = "Nice to meet you! I heard you want to demonstrate a task for me, " + \
                  "so I can learn and help you with similar tasks in the future. When would you like to start?"
        self.chat_area.add_message("Xiao Hong", response)
        self.user_instruction = message
        self.conversation_state = "ask_for_demo"
    
    def handle_demo_request(self, message):
        """Handle user's response to the demo request"""
        if any(keyword in message.lower() for keyword in ["can", "yes", "now", "start", "demo"]):
            response = "Great! I'll minimize the window but keep a small control in the corner. " + \
                      "Click 'Finish Demo' when you're done, and I'll record your steps."
            self.chat_area.add_message("Xiao Hong", response)
            self.conversation_state = "task_demonstration"
            self.is_recording = True
            
            # Delay 1 second before starting recording mode
            QTimer.singleShot(1000, self.start_recording_mode)
        else:
            response = "No problem, just let me know whenever you're ready to demonstrate. I'll be here."
            self.chat_area.add_message("Xiao Hong", response)
    
    def analyze_action(self, action):
        """Analyze user actions during demonstration"""
        self.step_counter += 1
        
        # 准备简化的动作数据
        action_data = {
            'type': action['type'],
            'event': str(action['event']),
            'step_number': self.step_counter,
            'base64_image': action['base64_image']
        }
        
        if action['type'] == 'keyboard' and self.text_buffer:
            action_data['text_buffer'] = self.text_buffer
            
        # 记录动作
        action['step_number'] = self.step_counter
        self.task_demonstration.append(action_data)
        
        # 状态文本
        status_text = f"Step {self.step_counter}: "
        if action["type"] == "mouse":
            self.text_buffer = ""
            status_text += f"Mouse action: {action['event']}"
        elif action["type"] == "keyboard":
            current_time = time.time()
            # Process keyboard input
            key_str = str(action["event"])
            # Handle printable characters
            if len(key_str) == 3 and key_str.startswith("'") and key_str.endswith("'"):
                self.text_buffer += key_str[1]
            
            # Handle special keys
            elif "key.space" in key_str.lower():
                self.text_buffer += " "
            elif "key.enter" in key_str.lower() or "return" in key_str.lower():
                status_text = f"Keyboard input completed: \"{self.text_buffer}\""
                self.update_mini_window_status(status_text)
                self.text_buffer = ""
                
                # 为键盘输入添加文本缓冲
                action_data['text_buffer'] = self.text_buffer
            
            elif "key.backspace" in key_str.lower() and self.text_buffer:
                self.text_buffer = self.text_buffer[:-1]
            
            # Display buffer if timeout occurred
            if current_time - self.last_keypress_time > 2.0 and self.text_buffer:
                status_text += f"Keyboard input: \"{self.text_buffer}\""
                
                # 为键盘输入添加文本缓冲
                action_data['text_buffer'] = self.text_buffer
            
            else:
                status_text += f"Keyboard action: {action['event']} (current input: \"{self.text_buffer}\")"
            
            self.last_keypress_time = current_time
        # 更新状态显示
        self.update_mini_window_status(status_text)
    


    def update_mini_window_status(self, text):
        """
        Update the status text in the mini window
        
        Args:
            text: Status text to display
        """
        if hasattr(self.mini_window, 'status_label'):
            self.mini_window.status_label.setText(text)
    
    def start_recording_mode(self):
        """Start recording user interactions"""
        # Call to parent window to minimize
        if hasattr(self, 'parent'):
            self.parent().showMinimized()
        
        # Show mini window
        self.mini_window.show()
        self.chat_area.add_message("System", "Recording your demonstration...")
        
        # Create input listener
        self.keyboard_mouse_listen = InputListener()
        self.keyboard_mouse_listen.action_detected.connect(self.analyze_action)
        
        # Set up thread
        self.listen_thread = QThread()
        self.keyboard_mouse_listen.terminated.connect(self.listen_thread.quit)
        self.keyboard_mouse_listen.moveToThread(self.listen_thread)
        self.listen_thread.started.connect(self.keyboard_mouse_listen.start_listen)
        
        # Start thread
        self.listen_thread.start()
    
    def finish_demonstration(self):
        """Complete the demonstration recording process"""
        # 关闭进程池并等待所有任务完成        
        # Clean up
        self.keyboard_mouse_listen.stop_listen()
        
        # Restore main window
        if hasattr(self, 'parent'):
            self.parent().showNormal()
        
        # Hide mini window
        self.mini_window.hide()
        
        self.is_recording = False
        self.save_task_demonstration()
        
        # 显示学习中的消息
        self.chat_area.add_message("System", "Learning in progress, please wait...")
        # Create process pool for few shot agent
        self.pool = multiprocessing.Pool(processes=1)
        
        # Call few shot agent asynchronously
        agent = FewShotGenerateAgent()
        # Get user instruction from main window
        result = self.pool.apply_async(agent, args=(self.task_demonstration, self.user_instruction))
        
        try:
            # Get result with timeout
            response = result.get(timeout=999)
            # Display response from agent
            self.chat_area.add_message("Xiao Hong", "I've analyzed your demonstration. Here's what I learned:\n" + response)
            
        except TimeoutError:
            self.chat_area.add_message("System", "Analysis timed out. Please try again.")
        except Exception as e:
            self.chat_area.add_message("System", f"Error during analysis: {str(e)}")
        finally:
            # Clean up pool
            self.pool.close()
            self.pool.join()
       
    
    
    
    def handle_ready_state(self, message):
        """
        Handle messages in the ready state
        
        Args:
            message: User message
        """
        response = "How else can I help you? I've learned the task you demonstrated and am ready to assist!"
        self.chat_area.add_message("Xiao Hong", response)
    
    def save_task_demonstration(self):
        """Save the recorded task demonstration to a file"""
        try:
            with open("task_demonstration.json", "w", encoding="utf-8") as f:
                json.dump(self.task_demonstration, f, ensure_ascii=False, indent=2)
            self.chat_area.add_message("System", "Task demonstration saved successfully")
        except Exception as e:
            self.chat_area.add_message("System", f"Error saving task demonstration: {str(e)}")

    def __del__(self):
        """析构函数，确保进程池正确关闭"""
        if hasattr(self, 'pool'):
            self.pool.close()
            self.pool.join()
        if hasattr(self, 'manager'):
            self.manager.shutdown() 