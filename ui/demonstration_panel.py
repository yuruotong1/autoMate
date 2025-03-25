"""
Demonstration panel for autoMate
"""
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QApplication
from PyQt6.QtCore import Qt, QPoint

class DemonstrationPanel(QWidget):
    def __init__(self, parent=None, stop_callback=None):
        super().__init__(parent, Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        self.stop_callback = stop_callback
        self.setup_ui()
        self.position_to_bottom_right()
        
    def setup_ui(self):
        demo_layout = QHBoxLayout()
        self.setLayout(demo_layout)
        
        # autoMate logo
        logo_label = QLabel("autoMate recording...")
        logo_label.setStyleSheet("color: #4CAF50; font-weight: bold; font-size: 14px;")
        demo_layout.addWidget(logo_label)
        
        # 停止按钮
        stop_demo_button = QPushButton("Stop") 
        stop_demo_button.setStyleSheet("background-color: #ff0000; color: white;")
        stop_demo_button.clicked.connect(self.on_stop_clicked)
        demo_layout.addWidget(stop_demo_button)
        
        demo_layout.addStretch()
        
        # 设置窗口样式
        self.setStyleSheet("background-color: #f0f0f0; border: 1px solid #999; padding: 8px;")
        self.setFixedHeight(50)  # 固定高度使其更紧凑
        self.resize(250, 50)
        
    def position_to_bottom_right(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = self.frameGeometry()
        position = QPoint(
            screen_geometry.width() - window_geometry.width() - 20,
            screen_geometry.height() - window_geometry.height() - 20
        )
        self.move(position)
        
    def on_stop_clicked(self):
        if self.stop_callback:
            self.stop_callback() 