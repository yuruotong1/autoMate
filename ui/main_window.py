"""
Main application window
"""
import os
import keyboard
from pathlib import Path
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                           QTextEdit, QSplitter, QMessageBox, QHeaderView, QDialog, QSystemTrayIcon)
from PyQt6.QtCore import Qt, pyqtSlot, QSize, QTimer
from PyQt6.QtGui import QPixmap, QIcon, QTextCursor, QTextCharFormat, QColor

from xbrain.utils.config import Config
from auto_control.agent.vision_agent import VisionAgent
from util.download_weights import OMNI_PARSER_DIR

from ui.theme import apply_theme
from ui.settings_dialog import SettingsDialog
from ui.agent_worker import AgentWorker
from ui.tray_icon import StatusTrayIcon
from ui.hotkey_edit import DEFAULT_STOP_HOTKEY

# Intro text for application
INTRO_TEXT = '''
Based on Omniparser to control desktop!
'''

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self, args):
        super().__init__()
        self.args = args
        
        # Initialize state
        self.state = self.setup_initial_state()
        
        # Initialize Agent
        self.vision_agent = VisionAgent(
            yolo_model_path=os.path.join(OMNI_PARSER_DIR, "icon_detect", "model.pt")
        )
        
        # Create tray icon
        self.setup_tray_icon()
        
        self.setWindowTitle("autoMate")
        self.setMinimumSize(1200, 800)
        
        self.init_ui()
        self.apply_theme()
        
        # Register hotkey handler
        self.hotkey_handler = None
        self.register_stop_hotkey()
        
        # Print startup information
        print(f"\n\n🚀 PyQt6 application launched")
    
    def setup_tray_icon(self):
        """Setup system tray icon"""
        # Create or load icon
        try:
            script_dir = Path(__file__).parent
            
            # Use logo.png as icon
            image_path = script_dir.parent / "imgs" / "logo.png"
            # Load image and create suitable icon size
            pixmap = QPixmap(str(image_path))
            # Resize to suitable icon size
            icon_pixmap = pixmap.scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            app_icon = QIcon(icon_pixmap)
            # Set application icon
            self.setWindowIcon(app_icon)
            
            # Create system tray icon
            self.tray_icon = StatusTrayIcon(app_icon, self)
            self.tray_icon.show()
            
        except Exception as e:
            print(f"Error setting up tray icon: {e}")
            self.tray_icon = None
    
    def setup_initial_state(self):
        """Set up initial state"""
        state = {}
        
        # Load data from config
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
        
        # Default to light theme
        state["theme"] = "Light"
        
        # Default stop hotkey
        state["stop_hotkey"] = DEFAULT_STOP_HOTKEY
        
        state["messages"] = []
        state["chatbox_messages"] = []
        state["auth_validated"] = False
        state["responses"] = {}
        state["tools"] = {}
        state["tasks"] = []
        state["only_n_most_recent_images"] = 2
        state["stop"] = False
        
        return state
    
    def register_stop_hotkey(self):
        """Register the global stop hotkey"""
        # First unregister any existing hotkey
        if self.hotkey_handler:
            try:
                keyboard.unhook(self.hotkey_handler)
                self.hotkey_handler = None
            except:
                pass
        
        # 确保所有旧的热键处理器都被清除
        try:
            keyboard.unhook_all_hotkeys()
        except:
            pass
        
        # Get the current hotkey from state
        hotkey = self.state.get("stop_hotkey", DEFAULT_STOP_HOTKEY)
        
        # Check if hotkey is valid
        if not hotkey:
            return
            
        try:
            # Register new hotkey with suppress=False to ensure it doesn't block the key
            self.hotkey_handler = keyboard.add_hotkey(hotkey, self.handle_stop_hotkey, suppress=False)
            print(f"Registered stop hotkey: {hotkey}")
        except Exception as e:
            print(f"Error registering hotkey '{hotkey}': {e}")
            # Try with a different method if the first fails
            try:
                keyboard.unhook_all()  # Clear all previous hotkeys
                self.hotkey_handler = keyboard.add_hotkey(hotkey, self.handle_stop_hotkey, suppress=False)
                print(f"Registered stop hotkey (alternate method): {hotkey}")
            except Exception as e2:
                print(f"All attempts to register hotkey '{hotkey}' failed: {e2}")
    
    def handle_stop_hotkey(self):
        """Handle stop hotkey press - redirects to stop_process with hotkey flag"""
        self.stop_process(from_hotkey=True)
    
    def apply_theme(self):
        """Apply the current theme to the application"""
        theme_name = self.state.get("theme", "Light")
        apply_theme(self, theme_name)
    
    def init_ui(self):
        """Initialize UI components"""
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        
        # Load top image
        header_layout = QVBoxLayout()
        try:
            script_dir = Path(__file__).parent
            image_path = script_dir.parent.parent / "imgs" / "header_bar_thin.png"
            if image_path.exists():
                pixmap = QPixmap(str(image_path))
                header_label = QLabel()
                header_label.setPixmap(pixmap.scaledToWidth(self.width()))
                header_layout.addWidget(header_label)
        except Exception as e:
            print(f"Failed to load header image: {e}")
        
        title_label = QLabel("autoMate")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = title_label.font()
        font.setPointSize(20)
        title_label.setFont(font)
        header_layout.addWidget(title_label)
        
        # Introduction text
        intro_label = QLabel(INTRO_TEXT)
        intro_label.setWordWrap(True)
        font = intro_label.font()
        font.setPointSize(12)
        intro_label.setFont(font)
        
        # Settings button and clear chat button (at top)
        top_buttons_layout = QHBoxLayout()
        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(self.open_settings_dialog)
        self.clear_button = QPushButton("Clear Chat")
        self.clear_button.clicked.connect(self.clear_chat)
        top_buttons_layout.addWidget(self.settings_button)
        top_buttons_layout.addWidget(self.clear_button)
        top_buttons_layout.addStretch()  # Add elastic space to left-align buttons
        
        # Input area
        input_layout = QHBoxLayout()
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Type a message to send to Omniparser + X ...")
        # Send message on Enter key
        self.chat_input.returnPressed.connect(self.process_input)
        self.submit_button = QPushButton("Send")
        self.submit_button.clicked.connect(self.process_input)
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_process)
        
        input_layout.addWidget(self.chat_input, 8)
        input_layout.addWidget(self.submit_button, 1)
        input_layout.addWidget(self.stop_button, 1)
        
        # Main content area
        content_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Task list
        task_widget = QWidget()
        task_layout = QVBoxLayout(task_widget)
        task_label = QLabel("Task List")
        self.task_table = QTableWidget(0, 2)
        self.task_table.setHorizontalHeaderLabels(["Status", "Task"])
        self.task_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        task_layout.addWidget(task_label)
        task_layout.addWidget(self.task_table)
        
        # Chat area
        chat_widget = QWidget()
        chat_layout = QVBoxLayout(chat_widget)
        chat_label = QLabel("Chat History")
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        chat_layout.addWidget(chat_label)
        chat_layout.addWidget(self.chat_display)
        
        # Add to splitter
        content_splitter.addWidget(task_widget)
        content_splitter.addWidget(chat_widget)
        content_splitter.setSizes([int(self.width() * 0.2), int(self.width() * 0.8)])
        
        # Add all components to main layout
        main_layout.addLayout(header_layout)
        main_layout.addWidget(intro_label)
        main_layout.addLayout(top_buttons_layout)  # Add top button area
        main_layout.addLayout(input_layout)
        main_layout.addWidget(content_splitter, 1)  # 1 is the stretch factor
        
        self.setCentralWidget(central_widget)
    
    def open_settings_dialog(self):
        """Open settings dialog"""
        dialog = SettingsDialog(self, self.state)
        result = dialog.exec()
        
        if result == QDialog.DialogCode.Accepted:
            # Get and apply new settings
            settings = dialog.get_settings()
            
            # Check if stop hotkey changed
            old_hotkey = self.state.get("stop_hotkey", DEFAULT_STOP_HOTKEY)
            new_hotkey = settings["stop_hotkey"]
            
            self.state["model"] = settings["model"]
            self.state["base_url"] = settings["base_url"]
            self.state["api_key"] = settings["api_key"]
            self.state["stop_hotkey"] = new_hotkey
            
            # Update theme if changed
            if settings["theme"] != self.state.get("theme", "Light"):
                self.state["theme"] = settings["theme"]
                self.apply_theme()
                
            if settings["screen_region"]:
                self.state["screen_region"] = settings["screen_region"]
                
            # Update hotkey if changed
            if old_hotkey != new_hotkey:
                self.register_stop_hotkey()
    
    def process_input(self):
        """Process user input"""
        user_input = self.chat_input.text()
        if not user_input.strip():
            return
            
        # Clear input box
        self.chat_input.clear()
        
        # Show hotkey reminder with auto-close functionality
        hotkey = self.state.get("stop_hotkey", DEFAULT_STOP_HOTKEY)
        msgBox = QMessageBox(self)
        msgBox.setIcon(QMessageBox.Icon.Information)
        msgBox.setWindowTitle("Automation Starting")
        msgBox.setText(f"Automation will start now. You can press {hotkey} to stop at any time.")
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        
        # Timer to auto-close after 3 seconds
        QTimer.singleShot(3000, msgBox.accept)
        
        # Add countdown display
        self.countdown_timer = QTimer(self)
        self.countdown_time = 3
        
        # Update text with countdown
        def update_countdown():
            self.countdown_time -= 1
            msgBox.setText(f"Automation will start now. You can press {hotkey} to stop at any time.\n\nThis window will close in {self.countdown_time} seconds...")
            if self.countdown_time <= 0:
                self.countdown_timer.stop()
        
        # Update text every second
        self.countdown_timer.timeout.connect(update_countdown)
        self.countdown_timer.start(1000)
        
        # Initial text with countdown
        msgBox.setText(f"Automation will start now. You can press {hotkey} to stop at any time.\n\nThis window will close in {self.countdown_time} seconds...")
        
        msgBox.exec()
        
        # Minimize main window
        self.showMinimized()
        
        # Create and start worker thread
        self.worker = AgentWorker(user_input, self.state, self.vision_agent)
        self.worker.update_signal.connect(self.update_ui)
        self.worker.error_signal.connect(self.handle_error)
        
        # Connect signals to tray icon if available
        if hasattr(self, 'tray_icon') and self.tray_icon is not None:
            self.worker.status_signal.connect(self.tray_icon.update_status)
            self.worker.task_signal.connect(self.tray_icon.update_task)
        
        self.worker.start()
    
    def handle_error(self, error_message):
        """Handle error messages"""
        # Restore main window to show the error
        self.showNormal()
        self.activateWindow()
        
        # Show error message
        QMessageBox.warning(self, "Connection Error", 
                           f"Error connecting to AI service:\n{error_message}\n\nPlease check your network connection and API settings.")
    
    @pyqtSlot(list, list)
    def update_ui(self, chatbox_messages, tasks):
        """Update UI display"""
        # Update chat display
        self.chat_display.clear()
        
        for msg in chatbox_messages:
            role = msg["role"]
            content = msg["content"]
            
            # Set different formats based on role
            format = QTextCharFormat()
            if role == "user":
                format.setForeground(QColor(0, 0, 255))  # Blue for user
                self.chat_display.append("You:")
            else:
                format.setForeground(QColor(0, 128, 0))  # Green for AI
                self.chat_display.append("AI:")
            
            # Add content
            cursor = self.chat_display.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.End)
            
            # Special handling for HTML content
            if "<" in content and ">" in content:
                self.chat_display.insertHtml(content)
                self.chat_display.append("")  # Add empty line
            else:
                self.chat_display.append(content)
                self.chat_display.append("")  # Add empty line
            
            # Scroll to bottom
            self.chat_display.verticalScrollBar().setValue(
                self.chat_display.verticalScrollBar().maximum()
            )
        
        # Update task table
        self.task_table.setRowCount(len(tasks))
        for i, (status, task) in enumerate(tasks):
            self.task_table.setItem(i, 0, QTableWidgetItem(status))
            self.task_table.setItem(i, 1, QTableWidgetItem(task))
    
    def stop_process(self, from_hotkey=False):
        """Stop processing - handles both button click and hotkey press
        
        Args:
            from_hotkey (bool): Whether this was triggered by a hotkey (True) or button (False)
        """
        self.state["stop"] = True
        if hasattr(self, 'worker') and self.worker is not None:
            self.worker.terminate()
        if self.isMinimized():
            self.showNormal()
            self.activateWindow()
        
        self.chat_display.append("<span style='color:red'>⚠️ Operation stopped by user</span>")
        self.register_stop_hotkey()
        # self.ask_for_teaching()

    def ask_for_teaching(self):
        """Ask for teaching"""
        msgBox = QMessageBox(self)
        msgBox.setIcon(QMessageBox.Icon.Information)
        msgBox.setWindowTitle("Teaching")
        msgBox.setText("Do you want to teach me how to do this?")
        msgBox.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msgBox.setWindowModality(Qt.WindowModality.NonModal)

        msgBox.exec()

    def clear_chat(self):
        """Clear chat history"""
        self.state["messages"] = []
        self.state["chatbox_messages"] = []
        self.state["responses"] = {}
        self.state["tools"] = {}
        self.state["tasks"] = []
        
        self.chat_display.clear()
        self.task_table.setRowCount(0)
    
    def closeEvent(self, event):
        """Handle window close event"""
        # This allows the app to continue running in the system tray
        # when the main window is closed
        if hasattr(self, 'tray_icon') and self.tray_icon is not None and self.tray_icon.isVisible():
            self.hide()
            event.ignore()
        # Check if this close event was triggered due to a hotkey stop
        elif self.state.get("stop", False) and hasattr(self, 'worker') and self.worker is not None:
            # Don't close the app, just stop the current task
            self.state["stop"] = False  # Reset stop flag
            event.ignore()
        # Prevent automatic closure when worker is still running
        elif hasattr(self, 'worker') and self.worker is not None and self.worker.isRunning():
            # Ask user if they really want to exit
            reply = QMessageBox.question(self, 'Exit Confirmation',
                                       '自动化任务仍在运行中，确定要退出程序吗？',
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                       QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                # Clean up on exit
                keyboard.unhook_all()
                event.accept()
            else:
                event.ignore()
        else:
            # Clean up on exit
            keyboard.unhook_all()
            event.accept() 