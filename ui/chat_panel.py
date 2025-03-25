"""
Chat panel for autoMate
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit
from PyQt6.QtGui import QTextCursor, QTextCharFormat, QColor

class ChatPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Initialize chat panel UI"""
        chat_layout = QVBoxLayout(self)
        chat_label = QLabel("Chat History")
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        chat_layout.addWidget(chat_label)
        chat_layout.addWidget(self.chat_display)
        
    def update_chat(self, chatbox_messages):
        """Update chat display with new messages"""
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
    
    def append_message(self, message, color=None):
        """Append a single message to chat display"""
        if color:
            self.chat_display.append(f"<span style='color:{color}'>{message}</span>")
        else:
            self.chat_display.append(message)
        
        # Scroll to bottom
        self.chat_display.verticalScrollBar().setValue(
            self.chat_display.verticalScrollBar().maximum()
        )
    
    def clear(self):
        """Clear chat history"""
        self.chat_display.clear() 