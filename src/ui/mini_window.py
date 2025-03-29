"""
Mini window module for displaying a small control window during demonstrations
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QFrame
)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QFont, QCursor, QPixmap

class MiniWindow(QMainWindow):
    """
    Mini floating window displayed during demonstration recording
    Provides status information and finish button
    """
    def __init__(self, finish_callback, parent=None):
        """
        Initialize the mini window
        
        Args:
            finish_callback: Function to call when finish button is clicked
            parent: Parent widget
        """
        super().__init__(parent, Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        
        self.setWindowTitle("Recording")
        self.setStyleSheet("background-color: white;")
        
        # Set small window size
        self.resize(300, 150)
        
        # Position in bottom right corner
        screen_geometry = self.screen().geometry()
        self.move(screen_geometry.width() - 320, screen_geometry.height() - 270)
        
        # For window dragging
        self.dragging = False
        self.offset = QPoint()
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        mini_layout = QVBoxLayout(central_widget)
        mini_layout.setContentsMargins(10, 10, 10, 10)
        mini_layout.setSpacing(10)
        
        # 创建标题部分
        mini_header = QFrame()
        mini_header.setFrameShape(QFrame.Shape.NoFrame)
        mini_header.setStyleSheet("background-color: #f5f5f5; border-radius: 8px;")
        header_layout = QHBoxLayout(mini_header)
        header_layout.setContentsMargins(10, 5, 10, 5)
        
        # Avatar placeholder
        self.mini_avatar = QLabel()
        self.mini_avatar.setFixedSize(30, 30)
        self.mini_avatar.setStyleSheet("background-color: #e0e0e0; border-radius: 15px;")
        header_layout.addWidget(self.mini_avatar)
        
        # Title
        mini_title = QLabel("Recording Demo")
        mini_title.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        mini_title.setStyleSheet("color: #d32f2f;")
        header_layout.addWidget(mini_title)
        header_layout.addStretch()
        
        # Status information
        self.status_label = QLabel("Recording your actions, please continue demonstration...")
        self.status_label.setWordWrap(True)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont("Arial", 10))
        self.status_label.setStyleSheet("color: #333333; margin: 10px;")
        
        # 新增：语音状态显示
        self.voice_status_label = QLabel("Voice Recording: Ready")
        self.voice_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.voice_status_label.setFont(QFont("Arial", 9))
        self.voice_status_label.setStyleSheet("color: #1976d2; margin: 0px 10px;")
        
        # Finish button
        finish_button = QPushButton("Finish Demo")
        finish_button.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        finish_button.setCursor(Qt.CursorShape.PointingHandCursor)
        finish_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border-radius: 8px;
                padding: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #ef5350;
            }
            QPushButton:pressed {
                background-color: #d32f2f;
            }
        """)
        finish_button.clicked.connect(finish_callback)
        
        # Add to layout
        mini_layout.addWidget(mini_header)
        mini_layout.addWidget(self.status_label)
        mini_layout.addWidget(self.voice_status_label)  # 添加语音状态标签
        mini_layout.addWidget(finish_button)
    
    def set_avatar(self, avatar_pixmap):
        """
        Set the avatar image for the mini window
        
        Args:
            avatar_pixmap: QPixmap containing the avatar image
        """
        scaled_avatar = avatar_pixmap.scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio, 
                                          Qt.TransformationMode.SmoothTransformation)
        self.mini_avatar.setPixmap(scaled_avatar)
        self.mini_avatar.setFixedSize(30, 30)
    
    def set_voice_status(self, status):
        """
        设置语音状态文本
        
        Args:
            status: 语音状态文本
        """
        self.voice_status_label.setText(f"Voice: {status}")
    
    # Mouse event handling for window dragging
    def mousePressEvent(self, event):
        """Handle mouse press events for dragging"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.offset = event.position().toPoint()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move events for dragging"""
        if self.dragging:
            self.move(self.mapToGlobal(event.position().toPoint() - self.offset))
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release events for dragging"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False 