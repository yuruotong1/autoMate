"""
Main application window
"""
import os
import sys
import keyboard
from pathlib import Path
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QLineEdit, QPushButton, QSplitter, QMessageBox, 
                           QDialog, QSystemTrayIcon, QApplication)
from PyQt6.QtCore import Qt, pyqtSlot, QSize, QMetaObject, Q_ARG, Qt, QObject, pyqtSignal
from PyQt6.QtGui import QPixmap, QIcon, QKeySequence, QShortcut

from auto_control.agent.vision_agent import VisionAgent
from util.download_weights import OMNI_PARSER_DIR

from ui.theme import apply_theme
from ui.settings_dialog import SettingsDialog
from ui.agent_worker import AgentWorker
from ui.tray_icon import StatusTrayIcon
from ui.hotkey_edit import DEFAULT_STOP_HOTKEY
from ui.task_panel import TaskPanel
from ui.chat_panel import ChatPanel
from ui.recording_manager import RecordingManager
from ui.settings_manager import SettingsManager

# Intro text for application
INTRO_TEXT = '''
Based on Omniparser to control desktop!
'''

class MainWindow(QMainWindow):
    """Main application window"""
    
    # 添加一个信号用于安全地在主线程调用stop_process
    stop_signal = pyqtSignal()
    
    def __init__(self, args):
        super().__init__()
        self.args = args
        
        # 连接信号到槽
        self.stop_signal.connect(self._stop_process_main_thread)
        
        # Initialize settings manager
        self.settings_manager = SettingsManager()
        
        # Initialize state
        self.state = self.setup_initial_state()
        
        # Initialize Agent
        self.vision_agent = VisionAgent(
            yolo_model_path=os.path.join(OMNI_PARSER_DIR, "icon_detect", "model.pt")
        )
        
        # Initialize recording manager
        self.recording_manager = RecordingManager(self)
        
        # Setup UI and tray icon
        self.setup_tray_icon()
        self.setWindowTitle("autoMate")
        self.setMinimumSize(1200, 800)
        self.init_ui()
        self.apply_theme()
        
        # Register hotkey handler
        self.hotkey_handler = None
        self.register_stop_hotkey()
    
    def setup_tray_icon(self):
        """Setup system tray icon"""
        try:
            script_dir = Path(__file__).parent
            image_path = script_dir.parent / "imgs" / "logo.png"
            pixmap = QPixmap(str(image_path))
            icon_pixmap = pixmap.scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            app_icon = QIcon(icon_pixmap)
            self.setWindowIcon(app_icon)
            
            self.tray_icon = StatusTrayIcon(app_icon, self)
            self.tray_icon.show()
        except Exception as e:
            print(f"Error setting up tray icon: {e}")
            self.tray_icon = None
    
    def setup_initial_state(self):
        """Set up initial state"""
        # Get settings from settings manager
        settings = self.settings_manager.get_settings()
        
        # Create state dictionary with settings and chat state
        state = {
            # Apply settings
            **settings,
            
            # Chat state
            "messages": [],
            "chatbox_messages": [],
            "auth_validated": False,
            "responses": {},
            "tools": {},
            "tasks": [],
            "stop": False
        }
        
        return state
    
    def register_stop_hotkey(self):
        """Register the global stop hotkey"""
        # Clean up existing hotkeys
        if self.hotkey_handler:
            try:
                keyboard.unhook(self.hotkey_handler)
                self.hotkey_handler = None
            except:
                pass
        
        try:
            keyboard.unhook_all_hotkeys()
        except:
            pass
        
        # Get the current hotkey from state
        hotkey = self.state.get("stop_hotkey", DEFAULT_STOP_HOTKEY)
        if not hotkey:
            return
            
        try:
            # 修改热键回调，改为发送信号
            self.hotkey_handler = keyboard.add_hotkey(hotkey, self._emit_stop_signal, suppress=False)
            print(f"Registered stop hotkey: {hotkey}")
        except Exception as e:
            print(f"Error registering hotkey '{hotkey}': {e}")
            try:
                keyboard.unhook_all()
                # 修改热键回调，改为发送信号
                self.hotkey_handler = keyboard.add_hotkey(hotkey, self._emit_stop_signal, suppress=False)
                print(f"Registered stop hotkey (alternate method): {hotkey}")
            except Exception as e2:
                print(f"All attempts to register hotkey '{hotkey}' failed: {e2}")
    
    def _emit_stop_signal(self):
        """从热键回调中安全地发送停止信号"""
        self.stop_signal.emit()
    
    def _stop_process_main_thread(self):
        """在主线程中安全地执行停止处理"""
        self.state["stop"] = True
        if hasattr(self, 'worker') and self.worker is not None:
            self.worker.terminate()
        if self.isMinimized():
            self.showNormal()
            self.activateWindow()
        self.chat_panel.append_message("⚠️ Stopped by user", "red")
        
        # Use non-modal dialog
        learn_dialog = QMessageBox(self)
        learn_dialog.setIcon(QMessageBox.Icon.Question)
        learn_dialog.setWindowTitle("Learning Opportunity")
        learn_dialog.setText("Would you like to show the correct steps to improve the system?")
        learn_dialog.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        learn_dialog.setDefaultButton(QMessageBox.StandardButton.No)
        learn_dialog.setWindowModality(Qt.WindowModality.NonModal)
        learn_dialog.show()
        
        # Connect signal to callback function
        learn_dialog.buttonClicked.connect(self.handle_learn_dialog_response)
    
    def apply_theme(self):
        """Apply the current theme to the application"""
        apply_theme(self, self.state.get("theme", "Light"))
    
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
        
        # Task panel
        self.task_panel = TaskPanel()
        
        # Chat panel
        self.chat_panel = ChatPanel()
        
        # Add to splitter
        content_splitter.addWidget(self.task_panel)
        content_splitter.addWidget(self.chat_panel)
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
            new_settings = dialog.get_settings()
            
            # Update settings in settings manager
            changes = self.settings_manager.update_settings(new_settings)
            
            # Update state with new settings
            self.state.update(new_settings)
            
            # Apply theme change if needed
            if changes["theme_changed"]:
                self.apply_theme()
                
            # Update hotkey if changed
            if changes["hotkey_changed"]:
                self.register_stop_hotkey()
                
            # Save settings to config
            self.settings_manager.save_to_config()
    
    def process_input(self):
        """Process user input"""
        user_input = self.chat_input.text()
        if not user_input.strip():
            return
            
        # Clear input box
        self.chat_input.clear()
        
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
        self.chat_panel.update_chat(chatbox_messages)
        
        # Update task table
        self.task_panel.update_tasks(tasks)
    
    def stop_process(self):
        """Stop processing - 处理按钮点击"""
        # 直接调用主线程处理方法，因为按钮点击已经在主线程中
        self._stop_process_main_thread()
    
    def handle_learn_dialog_response(self, button):
        if button.text() == "&Yes":
            self.showMinimized()
            self.recording_manager.start_demonstration()
            # Update chat to show demonstration mode is active
            self.chat_panel.append_message("📝 Demonstration mode activated. Please perform the correct actions.", "green")
    
    def clear_chat(self):
        """Clear chat history"""
        self.state["messages"] = []
        self.state["chatbox_messages"] = []
        self.state["responses"] = {}
        self.state["tools"] = {}
        self.state["tasks"] = []
        
        self.chat_panel.clear()
        self.task_panel.clear()
    
    def closeEvent(self, event):
        keyboard.unhook_all()
        event.accept() 
        if hasattr(self, 'worker') and self.worker is not None:
            self.worker.terminate()

# 应用程序入口
def main():
    app = QApplication(sys.argv)
    window = MainWindow(sys.argv)
    window.show()
    sys.exit(app.exec())  # 注意PyQt6中不需要括号

if __name__ == "__main__":
    main()