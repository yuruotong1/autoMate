"""
Mini window component for task demonstration mode
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QPushButton, QApplication)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class MiniWindow(QMainWindow):
    """
    Small floating window displayed during task demonstration
    """
    def __init__(self, finish_callback, parent=None):
        """
        Initialize the mini window
        
        Args:
            finish_callback: Function to call when demonstration is finished
            parent: Parent widget
        """
        super().__init__(parent)
        self.setWindowTitle("Learning Mode")
        self.setFixedSize(250, 150)
        
        # Position in bottom-right corner
        desktop = QApplication.primaryScreen().availableGeometry()
        self.move(desktop.width() - 270, desktop.height() - 170)
        
        # Set frameless and always-on-top flags
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint
        )
        
        # Set window style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #fff8f8;
                border: 2px solid #ffcdd2;
                border-radius: 10px;
            }
        """)
        
        # Create central widget
        mini_central = QWidget()
        self.setCentralWidget(mini_central)
        
        # Create layout
        mini_layout = QVBoxLayout(mini_central)
        
        # Create header with avatar and title
        mini_header = QWidget()
        header_layout = QHBoxLayout(mini_header)
        
        self.mini_avatar = QLabel()
        # Avatar will be set from the main window
        header_layout.addWidget(self.mini_avatar)
        
        mini_title = QLabel("Learning in progress...")
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