"""
Chat area component for displaying message history
"""
from PyQt6.QtWidgets import (QScrollArea, QWidget, QVBoxLayout)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QPen, QColor, QPixmap, QFont
import datetime
import os

from src.ui.message_widgets import MessageWidget, SystemMessageWidget


class ChatArea(QScrollArea):
    """
    Scrollable chat area for displaying messages
    """
    def __init__(self, parent=None):
        """
        Initialize the chat area
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Apply styling
        self.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: white;
            }
            QScrollBar:vertical {
                border: none;
                background: #f8f8f8;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #d0d0d0;
                min-height: 30px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: #b0b0b0;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Create content container
        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("""
            background-color: white;
            padding-left: 20px;
            padding-right: 20px;
        """)
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(10, 5, 10, 5)  # Reduce vertical margins further
        self.content_layout.setSpacing(8)  # Keep same spacing between messages
        self.content_layout.addStretch()
        
        self.setWidget(self.content_widget)
        
        # Create avatar images
        self.create_avatars()
    
    def create_avatars(self):
        """Create avatar images for the chat participants"""
        # Try to load the intern avatar
        avatar_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                "imgs", "xiaohong.jpg")
        try:
            self.intern_avatar = QPixmap(avatar_path)
            if self.intern_avatar.isNull():
                self.create_fallback_avatar()
            else:
                self.intern_avatar = self.intern_avatar.scaled(40, 40, 
                                                       Qt.AspectRatioMode.KeepAspectRatio, 
                                                       Qt.TransformationMode.SmoothTransformation)
        except:
            self.create_fallback_avatar()
        
        # Create a user avatar
        avatar_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                 "imgs", "user.png")
        original_pixmap = QPixmap(avatar_path)
        self.user_avatar = original_pixmap.scaled(40, 40, 
                                              Qt.AspectRatioMode.KeepAspectRatio, 
                                              Qt.TransformationMode.SmoothTransformation)
        
        # Create circular mask
        mask = QPixmap(40, 40)
        mask.fill(Qt.GlobalColor.transparent)
        painter = QPainter(mask)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor("black"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(0, 0, 40, 40)
        painter.end()
        
        # Apply mask to avatar
        masked_pixmap = QPixmap(40, 40)
        masked_pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(masked_pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.drawPixmap(0, 0, mask)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        painter.drawPixmap(0, 0, self.user_avatar)
        painter.end()
        
        self.user_avatar = masked_pixmap
    
    def create_fallback_avatar(self):
        """Create a fallback avatar when image loading fails"""
        self.intern_avatar = QPixmap(40, 40)
        self.intern_avatar.fill(Qt.GlobalColor.transparent)
        painter = QPainter(self.intern_avatar)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor("#ffebee"))
        painter.setPen(QPen(QColor("#f44336"), 2))
        painter.drawEllipse(2, 2, 36, 36)
        painter.setPen(QPen(QColor("#d32f2f"), 2))
        painter.setFont(QFont("Arial", 15, QFont.Weight.Bold))
        painter.drawText(14, 26, "小红")
        painter.end()
    
    def add_message(self, sender, text, is_user=False):
        """
        Add a new message to the chat area
        
        Args:
            sender: Message sender name
            text: Message content
            is_user: Whether this is a user message
        """
        timestamp = datetime.datetime.now().strftime("%H:%M")
        
        if sender == "System":
            message_widget = SystemMessageWidget(text)
        else:
            if is_user:
                message_widget = MessageWidget("", self.user_avatar, text, timestamp, True)
            else:
                message_widget = MessageWidget("", self.intern_avatar, text, timestamp, False)
        
        # Insert the message widget above the spacer
        self.content_layout.insertWidget(self.content_layout.count() - 1, message_widget)
        
        # Scroll to the bottom to show new message
        QTimer.singleShot(100, self.scroll_to_bottom)
    
    def scroll_to_bottom(self):
        """Scroll the chat area to the bottom to show the latest messages"""
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum()) 