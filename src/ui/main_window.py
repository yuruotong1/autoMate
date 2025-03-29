"""
Main application window for the AutoMate interface
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QApplication
)
from PyQt6.QtCore import Qt
from src.ui.chat_area import ChatArea
from src.ui.input_area import InputArea
from src.ui.profile_widget import ProfileWidget
from src.ui.mini_window import MiniWindow
from src.core.conversation_manager import ConversationManager


class MainWindow(QMainWindow):
    """
    Main application window containing all UI components
    """
    def __init__(self):
        """Initialize the main window"""
        super().__init__()
        self.setWindowTitle("Chat with Xiao Hong")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(900, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
            }
        """)
        
        # Center the window on screen
        screen = QApplication.primaryScreen().availableGeometry()
        window_size = self.geometry()
        x = (screen.width() - window_size.width()) // 2
        y = (screen.height() - window_size.height()) // 2
        self.move(x, y)
        
        # Create mini window for demonstration mode first
        self.mini_window = MiniWindow(self.finish_demonstration)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create profile widget
        self.profile_widget = ProfileWidget()
        
        # Create chat container
        chat_container = QWidget()
        chat_layout = QVBoxLayout(chat_container)
        chat_layout.setContentsMargins(0, 0, 0, 0)
        chat_layout.setSpacing(0)
        chat_container.setStyleSheet("""
            background-color: white;
        """)
        
        # Create chat area
        self.chat_area = ChatArea()
        
        # Create conversation manager
        self.conversation_manager = ConversationManager(self.chat_area, self.mini_window)
        
        # Set parent for conversation manager
        self.conversation_manager.parent = lambda: self
        
        # Connect mini window to chat area avatar
        self.mini_window.set_avatar(self.chat_area.intern_avatar)
        
        # Create input area
        self.input_area = InputArea(self.conversation_manager.process_message)
        
        # Add to chat layout
        chat_layout.addWidget(self.chat_area, 1)
        chat_layout.addWidget(self.input_area, 0)
        
        # Add to main layout
        main_layout.addWidget(self.profile_widget, 1)
        main_layout.addWidget(chat_container, 5)
    
    def finish_demonstration(self):
        """Finish demonstration callback for mini window"""
        self.conversation_manager.finish_demonstration()