"""
Conversation manager module for handling dialog flow and states
"""
import json
import time
from PyQt6.QtCore import QObject, QThread, QTimer, pyqtSignal, pyqtSlot
from src.core.few_shot_agent import FewShotGenerateAgent
from src.core.input_listener import InputListener
from src.utils.audio_recorder import AudioRecorder
from xbrain.core.chat import run
import multiprocessing
from multiprocessing import Process, Queue, Manager



class AnalysisWorker(QObject):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    # 将信号改回只接受一个参数
    progress_update = pyqtSignal(str)
    
    def __init__(self, agent, task_demonstration, user_instruction):
        super().__init__()
        self.agent = agent
        self.task_demonstration = task_demonstration
        self.user_instruction = user_instruction
    
    @pyqtSlot()
    def process(self):
        try:
            # 执行分析，获取生成器
            result_generator = self.agent(self.task_demonstration, self.user_instruction)
            
            # 迭代生成器，处理每个产生的值
            for content in result_generator:
                # 发送每个生成的内容更新
                self.progress_update.emit(content)
            
            self.finished.emit("分析完成")
        except Exception as e:
            self.error.emit(str(e))
    

    # 处理流式输出的进度更新
    def handle_analysis_progress(self, segment_text, is_thinking):
        """处理分析过程中的流式输出"""
        if self.current_ai_message_id is not None:
            # 根据is_thinking参数应用不同样式
            if is_thinking:
                # 思考过程使用浅色样式
                styled_text = f"<span style='color: #888888; font-style: italic;'>{segment_text}</span>"
                self.chat_area.update_message(self.current_ai_message_id, styled_text, preserve_html=True)
            else:
                # 结果使用正常样式
                self.chat_area.update_message(self.current_ai_message_id, segment_text)

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
        
        # 新增：语音录制和意图检测
        self.is_voice_recording = False
        self.utterances = []
        
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
                      "Click 'Finish Demo' when you're done, and I'll record your steps. " + \
                      "I'll also record your voice to understand your intentions while performing actions."
            self.chat_area.add_message("Xiao Hong", response)
            self.conversation_state = "task_demonstration"
            self.is_recording = True
            
            # 清空之前的记录
            self.task_demonstration = []
            self.utterances = []
            
            # Delay 1 second before starting recording mode
            QTimer.singleShot(1000, self.start_recording_mode)
        else:
            response = "No problem, just let me know whenever you're ready to demonstrate. I'll be here."
            self.chat_area.add_message("Xiao Hong", response)
    
    def handle_utterance(self, utterance_data):
        """
        处理检测到的语音意图
        
        Args:
            utterance_data: 包含语音识别结果的字典
        """
        # 添加到utterances列表
        self.utterances.append(utterance_data)
        
        # 添加步骤计数
        utterance_data['step_number'] = self.step_counter
        
        # 更新状态显示
        status_text = f"语音命令: \"{utterance_data['text']}\""
        self.update_mini_window_status(status_text)
        
        # 这里我们不把utterance添加到task_demonstration列表
        # 因为我们需要将其作为分割点，而不是直接作为动作
    
    def analyze_action(self, action):
        """Analyze user actions during demonstration"""
        self.step_counter += 1
        
        # 准备简化的动作数据
        action_data = {
            'type': 'action',  # 新增：明确标记为action类型
            'event': str(action['event']),
            'step_number': self.step_counter,
            'timestamp': time.time(),  # 新增：添加时间戳
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
        self.chat_area.add_message("System", "Recording your demonstration and voice...")
        
        # Create input listener
        self.keyboard_mouse_listen = InputListener()
        self.keyboard_mouse_listen.action_detected.connect(self.analyze_action)
        
        # Set up thread for input listening
        self.listen_thread = QThread()
        self.keyboard_mouse_listen.terminated.connect(self.listen_thread.quit)
        self.keyboard_mouse_listen.moveToThread(self.listen_thread)
        self.listen_thread.started.connect(self.keyboard_mouse_listen.start_listen)
        
        # 新增：创建语音录制器
        self.audio_recorder = AudioRecorder()
        self.audio_recorder.utterance_detected.connect(self.handle_utterance)
        self.audio_recorder.recording_status.connect(self.update_audio_status)
        
        # 设置语音录制线程
        self.audio_thread = QThread()
        self.audio_recorder.terminated.connect(self.audio_thread.quit)
        self.audio_recorder.moveToThread(self.audio_thread)
        self.audio_thread.started.connect(self.audio_recorder.start_recording)
        
        # Start threads
        self.listen_thread.start()
        self.audio_thread.start()
        self.is_voice_recording = True
    
    def update_audio_status(self, status):
        """
        更新语音状态信息
        
        Args:
            status: 语音状态文本
        """
        # 在mini window使用专用语音状态标签
        if hasattr(self.mini_window, 'set_voice_status'):
            self.mini_window.set_voice_status(status)
        
        # 同时也更新主状态区域的显示
        current_text = self.mini_window.status_label.text() if hasattr(self.mini_window, 'status_label') else ""
        if "语音" not in current_text:
            self.update_mini_window_status(f"{current_text}\n语音: {status}")
        else:
            # 替换语音状态部分
            lines = current_text.split("\n")
            updated_lines = [line if "语音" not in line else f"语音: {status}" for line in lines]
            self.update_mini_window_status("\n".join(updated_lines))
    
    def finish_demonstration(self):
        """Complete the demonstration recording process"""
        # Clean up keyboard/mouse listener
        self.keyboard_mouse_listen.stop_listen()
        
        # 新增：停止语音录制
        if self.is_voice_recording:
            self.audio_recorder.stop_recording()
            self.is_voice_recording = False
        
        # Restore main window
        if hasattr(self, 'parent'):
            self.parent().showNormal()
        
        # Hide mini window
        self.mini_window.hide()
        
        self.is_recording = False
        
        # 合并utterances和actions
        self.prepare_mixed_sequence()
        
        # 保存演示数据
        self.save_task_demonstration()
        
        # 显示学习中的消息
        self.chat_area.add_message("System", "Learning in progress, please wait...")
        
        # 创建分析线程而不是进程池
        self.analysis_thread = QThread()
        self.agent = FewShotGenerateAgent()
        
        # 使用合并后的混合序列而不是仅使用action序列
        self.worker = AnalysisWorker(self.agent, self.task_demonstration, self.user_instruction)
        
        # 连接信号到槽函数
        self.worker.finished.connect(self.handle_analysis_result)
        self.worker.error.connect(self.handle_analysis_error)
        self.worker.progress_update.connect(self.handle_progress_update)
        
        # 迁移worker到线程
        self.worker.moveToThread(self.analysis_thread)
        self.analysis_thread.started.connect(self.worker.process)
        self.worker.finished.connect(self.analysis_thread.quit)
        self.worker.error.connect(self.analysis_thread.quit)
        
        # 启动线程
        self.analysis_thread.start()
        
        # 添加一个进度提示
        self.progress_timer = QTimer(self)
        self.progress_timer.timeout.connect(self.update_analysis_progress)
        self.progress_counter = 0
        self.progress_timer.start(1000)
    
    def prepare_mixed_sequence(self):
        """
        准备混合序列，将utterances和actions合并成按时间排序的混合序列
        """
        # 将utterances添加到task_demonstration中
        mixed_sequence = self.task_demonstration.copy()
        
        for utterance in self.utterances:
            # 确保每个utterance都有timestamp
            if 'timestamp' not in utterance:
                utterance['timestamp'] = time.time()  # 如果没有时间戳，使用当前时间
            
            mixed_sequence.append(utterance)
        
        # 按时间戳排序
        self.task_demonstration = sorted(mixed_sequence, key=lambda x: x.get('timestamp', 0))

    def update_analysis_progress(self):
        """更新分析进度"""
        self.progress_counter += 1
        if self.progress_counter % 15 == 0:  # 每15秒更新一次消息
            self.chat_area.add_message("System", f"Analysis in progress... ({self.progress_counter} seconds)")
    
    def handle_analysis_result(self, result):
        """处理分析结果"""
        self.progress_timer.stop()
        if result != "分析完成":
            self.chat_area.add_message("Xiao Hong", result)
        self.conversation_state = "ready"
    
    def handle_analysis_error(self, error_msg):
        """处理分析错误"""
        self.progress_timer.stop()
        self.chat_area.add_message("System", f"Error during analysis: {error_msg}")
        print(f"Error during analysis: {error_msg}")
        self.conversation_state = "ready"
    
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

    def handle_progress_update(self, content):
        """处理分析过程中的进度更新"""
        self.chat_area.add_message("Xiao Hong", content)

    def __del__(self):
        """析构函数，确保进程池正确关闭"""
        if hasattr(self, 'pool'):
            self.pool.close()
            self.pool.join()
        if hasattr(self, 'manager'):
            self.manager.shutdown() 