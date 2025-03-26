"""
Input area component for user message entry
"""
from PyQt6.QtWidgets import (QWidget, QTextEdit, QPushButton, QHBoxLayout, QVBoxLayout)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class InputArea(QWidget):
    """
    Input area for user to type and send messages
    """
    def __init__(self, message_callback, parent=None):
        """
        Initialize input area
        
        Args:
            message_callback: Function to call when a message is submitted
            parent: Parent widget
        """
        super().__init__(parent)
        self.message_callback = message_callback
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI components"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 8, 15, 15)
        
        # Input area with send button
        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)
        input_layout.setContentsMargins(0, 0, 0, 0)
        
        # Text edit for input
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Please enter your response...")
        self.text_edit.setMinimumHeight(50)
        self.text_edit.setMaximumHeight(100)
        self.text_edit.setFont(QFont("Arial", 11))
        self.text_edit.setStyleSheet("""
            QTextEdit {
                border: 1px solid #e6e6e6;
                border-radius: 18px;
                padding: 10px 15px;
                background-color: #ffffff;
                color: #333333;
            }
            QTextEdit:focus {
                border: 1px solid #cccccc;
            }
        """)
        
        # Make return key submit the message
        self.text_edit.installEventFilter(self)
        
        # Send button
        self.send_button = QPushButton("Send")
        self.send_button.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.send_button.setMinimumSize(80, 50)
        self.send_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #1e88e5;
                color: white;
                border-radius: 18px;
                padding: 8px 16px;
                border: none;
            }
            QPushButton:hover {
                background-color: #1976d2;
            }
            QPushButton:pressed {
                background-color: #1565c0;
            }
            QPushButton:disabled {
                background-color: #e0e0e0;
                color: #9e9e9e;
            }
        """)
        self.send_button.clicked.connect(self.send_message)
        
        # Add widgets to layout
        input_layout.addWidget(self.text_edit)
        input_layout.addWidget(self.send_button)
        input_layout.setStretchFactor(self.text_edit, 8)
        input_layout.setStretchFactor(self.send_button, 1)
        
        main_layout.addLayout(input_layout)
    
    def eventFilter(self, obj, event):
        """
        Handle keyboard events in the text edit
        
        Args:
            obj: Object that triggered the event
            event: The event object
        """
        if obj is self.text_edit and event.type() == event.Type.KeyPress:
            # Check for Enter key (without Shift for newline)
            if event.key() == Qt.Key.Key_Return and not event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                self.send_message()
                return True
        return super().eventFilter(obj, event)
    
    def send_message(self):
        """Send the current message"""
        message = self.text_edit.toPlainText().strip()
        if message:
            # Call the callback
            self.message_callback(message)
            # Clear the input only if there is text
            if len(message) > 0:
                self.text_edit.clear()
    
    def set_enabled(self, enabled):
        """
        Enable or disable the input area
        
        Args:
            enabled: Whether the input area should be enabled
        """
        self.text_edit.setEnabled(enabled)
        self.send_button.setEnabled(enabled) 