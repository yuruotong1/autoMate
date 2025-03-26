"""
Conversation manager module for handling dialog flow and states
"""
import json
import time
from PyQt6.QtCore import QObject, QThread, QTimer
from src.core.input_listener import InputListener
from xbrain.core.chat import run


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
        elif self.conversation_state == "task_demonstration" and self.is_recording:
            self.handle_task_demonstration(message)
        elif self.conversation_state == "ready":
            self.handle_ready_state(message)
    
    def handle_greeting_response(self, message):
        """Handle user's response to the initial greeting"""
        response = "Nice to meet you! I heard you want to demonstrate a task for me, " + \
                  "so I can learn and help you with similar tasks in the future. When would you like to start?"
        self.chat_area.add_message("Xiao Hong", response)
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
        """
        Analyze user actions during demonstration
        
        Args:
            action: Dict containing action data
        """
        self.task_demonstration.append(action)
        
        # Initialize status text
        status_text = f"Action detected: {action}"
        
        # Format display based on action type
        if action["type"] == "mouse":
           
            self.text_buffer = ""

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
                return
            elif "key.backspace" in key_str.lower() and self.text_buffer:
                self.text_buffer = self.text_buffer[:-1]
            
            # Display buffer if timeout occurred
            if current_time - self.last_keypress_time > 2.0 and self.text_buffer:
                status_text = f"Keyboard input: \"{self.text_buffer}\""
            else:
                status_text = f"Keyboard action: {action['event']} (current input: \"{self.text_buffer}\")"
            
            self.last_keypress_time = current_time
        
        # Update mini window status
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
        # Clean up
        self.keyboard_mouse_listen.stop_listen()
        
        # Restore main window
        if hasattr(self, 'parent'):
            self.parent().showNormal()
        
        # Hide mini window
        self.mini_window.hide()
        
        self.is_recording = False
        self.save_task_demonstration()
        
        # Show summary
        action_count = len(self.task_demonstration)
        response = f"I've successfully learned this task! Recorded and analyzed {action_count} key actions. " + \
                  "Feel free to assign similar tasks to me in the future. 😊"
        self.chat_area.add_message("Xiao Hong", response)
        self.conversation_state = "ready"
    
    def handle_task_demonstration(self, message):
        """
        Handle messages during task demonstration
        
        Args:
            message: User message
        """
        self.task_demonstration.append(message)
        
        if any(keyword in message.lower() for keyword in ["done", "finish", "completed", "complete"]):
            self.is_recording = False
            self.save_task_demonstration()
            response = "I've learned this task! Thank you for the demonstration. " + \
                      "You can now assign similar tasks to me in the future. 😊"
            self.chat_area.add_message("Xiao Hong", response)
            self.conversation_state = "ready"
        else:
            response = "I'm still learning... Please continue your demonstration."
            self.chat_area.add_message("Xiao Hong", response)
    
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