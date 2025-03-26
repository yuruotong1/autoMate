"""
Profile widget component for displaying intern information
"""
import os
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap, QColor, QPainter, QPen


class ProfileWidget(QWidget):
    """
    Widget displaying the intern's profile information
    """
    def __init__(self, parent=None):
        """
        Initialize the profile widget
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.setFixedWidth(280)
        self.setStyleSheet("""
            background-color: white;
        """)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI components"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 30, 20, 20)
        main_layout.setSpacing(20)
        
        # Profile header with avatar and name
        self.create_profile_header(main_layout)
        
        # Add profile information
        self.create_profile_info(main_layout)
        
        # Add spacer
        main_layout.addStretch()
    
    def create_profile_header(self, layout):
        """
        Create the profile header section
        
        Args:
            layout: Layout to add the header widgets to
        """
        # Header layout
        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.setSpacing(12)
        
        # Avatar
        avatar_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                 "imgs", "xiaohong.jpg")
        avatar_label = QLabel()
        avatar_label.setFixedSize(140, 140)
        avatar_label.setStyleSheet("""
            border-radius: 70px;
            background-color: white;
        """)
        
        try:
            avatar_pixmap = QPixmap(avatar_path)
            if not avatar_pixmap.isNull():
                scaled_avatar = avatar_pixmap.scaled(140, 140, 
                                                  Qt.AspectRatioMode.KeepAspectRatio, 
                                                  Qt.TransformationMode.SmoothTransformation)
                
                # Create circular mask
                mask = QPixmap(140, 140)
                mask.fill(Qt.GlobalColor.transparent)
                painter = QPainter(mask)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                painter.setBrush(QColor("black"))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawEllipse(0, 0, 140, 140)
                painter.end()
                
                # Apply mask to avatar
                masked_pixmap = QPixmap(140, 140)
                masked_pixmap.fill(Qt.GlobalColor.transparent)
                painter = QPainter(masked_pixmap)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                painter.drawPixmap(0, 0, mask)
                painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
                painter.drawPixmap(0, 0, scaled_avatar)
                painter.end()
                
                avatar_label.setPixmap(masked_pixmap)
            else:
                self.create_fallback_avatar(avatar_label)
        except:
            self.create_fallback_avatar(avatar_label)
        
        avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(avatar_label)
        
        # Name
        name_label = QLabel("Xiao Hong")
        name_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        name_label.setStyleSheet("color: #333333;")
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(name_label)
        
        # Title
        title_label = QLabel("AI Assistant")
        title_label.setFont(QFont("Arial", 13))
        title_label.setStyleSheet("color: #777777;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title_label)
        
        layout.addLayout(header_layout)
    
    def create_fallback_avatar(self, avatar_label):
        """
        Create a fallback avatar when the image cannot be loaded
        
        Args:
            avatar_label: QLabel to set the fallback avatar to
        """
        avatar_pixmap = QPixmap(140, 140)
        avatar_pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(avatar_pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor("#f8f9fa"))
        painter.setPen(QPen(QColor("#dee2e6"), 3))
        painter.drawEllipse(3, 3, 134, 134)
        painter.setPen(QPen(QColor("#6c757d"), 2))
        painter.setFont(QFont("Arial", 60, QFont.Weight.Bold))
        painter.drawText(38, 90, "XH")
        painter.end()
        
        avatar_label.setPixmap(avatar_pixmap)
    
    def create_profile_info(self, layout):
        """
        Create the profile information section
        
        Args:
            layout: Layout to add the info widgets to
        """
        # Info layout
        info_layout = QVBoxLayout()
        info_layout.setSpacing(14)
        info_layout.setContentsMargins(0, 0, 0, 0)
        
        # Info items
        info_items = [
            ("Age", "23"),
            ("Education", "East China Normal University"),
            ("Major", "Computer Science"),
            ("Skills", "Data Analysis, Document Processing"),
            ("Languages", "Chinese, English")
        ]
        
        for title, value in info_items:
            item_layout = QVBoxLayout()
            item_layout.setSpacing(4)
            item_layout.setContentsMargins(0, 0, 0, 0)
            
            title_label = QLabel(title)
            title_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            title_label.setStyleSheet("color: #555555;")
            
            value_label = QLabel(value)
            value_label.setFont(QFont("Arial", 12))
            value_label.setWordWrap(True)
            value_label.setStyleSheet("color: #333333;")
            
            item_layout.addWidget(title_label)
            item_layout.addWidget(value_label)
            
            info_widget = QWidget()
            info_widget.setLayout(item_layout)
            info_widget.setStyleSheet("background-color: white;")
            
            info_layout.addWidget(info_widget)
        
        layout.addLayout(info_layout)
    
    def create_status_section(self, layout):
        """
        Create the status section - now removed
        
        Args:
            layout: Layout to add the status widgets to
        """
        # This function is now empty as we're removing the status section
        pass 