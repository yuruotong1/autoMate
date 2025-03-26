"""
Message widget components for chat interface
"""
from PyQt6.QtWidgets import (QWidget, QLabel, QHBoxLayout, QVBoxLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QPalette


class MessageWidget(QWidget):
    """
    Widget for displaying chat messages with avatar, name, text and timestamp
    """
    def __init__(self, sender_name, avatar_pixmap, message_text, timestamp, is_user=False):
        """
        Initialize a message widget
        
        Args:
            sender_name: Name of the message sender
            avatar_pixmap: Pixmap for the sender's avatar
            message_text: Text content of the message
            timestamp: Time the message was sent
            is_user: Whether this is a user message (affects styling)
        """
        super().__init__()
        self.is_user = is_user
        self.init_ui(sender_name, avatar_pixmap, message_text, timestamp)
    
    def init_ui(self, sender_name, avatar_pixmap, message_text, timestamp):
        """Initialize the UI components of the message widget"""
        # Create main layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 2, 0, 2)  # Reduce vertical padding further
        main_layout.setSpacing(4)  # Reduce spacing between avatar and message
        
        # Add avatar to left or right based on if user message
        avatar_label = QLabel()
        avatar_label.setPixmap(avatar_pixmap)
        avatar_label.setFixedSize(40, 40)
        avatar_label.setStyleSheet("""
            QLabel {
                border-radius: 20px;
                background-color: transparent;
                min-width: 40px;
                min-height: 40px;
            }
        """)
        
        # Create message content layout
        message_container = QWidget()
        message_layout = QVBoxLayout(message_container)
        message_layout.setContentsMargins(8, 6, 8, 6)  # Reduce message container padding
        message_layout.setSpacing(2)  # Reduce spacing between text and timestamp
        
        # Configure message text
        text_label = QLabel(message_text)
        text_label.setFont(QFont("Arial", 11))
        text_label.setWordWrap(True)
        text_label.setMinimumWidth(600)  # Set minimum width
        text_label.setMaximumWidth(800)  # Increase maximum width
        text_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        
        # Add timestamp
        time_label = QLabel(timestamp)
        time_label.setFont(QFont("Arial", 8))
        time_label.setStyleSheet("color: #888888;")
        
        # Arrange components according to message direction
        if self.is_user:
            message_container.setStyleSheet("""
                background-color: #e8f4ff;
                border-radius: 20px;
                border-top-right-radius: 6px;
                padding: 8px;
                color: #2c3e50;
                margin: 2px;
            """)
            time_label.setAlignment(Qt.AlignmentFlag.AlignRight)
            message_layout.addWidget(text_label)
            message_layout.addWidget(time_label)
            main_layout.addStretch()
            main_layout.addWidget(message_container)
            main_layout.addWidget(avatar_label)
        else:
            message_container.setStyleSheet("""
                background-color: #fff2f2;
                border-radius: 20px;
                border-top-left-radius: 6px;
                padding: 8px;
                color: #2c3e50;
                margin: 2px;
            """)
            message_layout.addWidget(text_label)
            message_layout.addWidget(time_label)
            main_layout.addWidget(avatar_label)
            main_layout.addWidget(message_container)
            main_layout.addStretch()


class SystemMessageWidget(QWidget):
    """Widget for displaying system messages"""
    def __init__(self, message_text):
        """
        Initialize a system message widget
        
        Args:
            message_text: Text content of the system message
        """
        super().__init__()
        self.init_ui(message_text)
    
    def init_ui(self, message_text):
        """Initialize the UI components of the system message widget"""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 3, 20, 3)
        
        # Create system message label
        text_label = QLabel(message_text)
        text_label.setFont(QFont("Arial", 10, QFont.Weight.Normal))
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_label.setMaximumWidth(350)  # Make system messages narrower
        text_label.setStyleSheet("""
            background-color: #f0f0f0;
            border-radius: 16px;
            padding: 8px 14px;
            color: #505050;
        """)
        
        main_layout.addStretch()
        main_layout.addWidget(text_label)
        main_layout.addStretch() 