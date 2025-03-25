"""
Recording indicator panel for autoMate
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QApplication
from PyQt6.QtCore import Qt, QPoint

class RecordingIndicator(QWidget):
    def __init__(self, parent=None, stop_callback=None):
        super().__init__(parent, Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        self.stop_callback = stop_callback
        self.setup_ui()
        self.position_to_bottom_right()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Recording status label
        self.status_label = QLabel("Recording in progress")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        layout.addWidget(self.status_label)
        
        # Stop button
        self.stop_button = QPushButton("Stop Recording")
        self.stop_button.clicked.connect(self.on_stop_clicked)
        layout.addWidget(self.stop_button)
        
        self.setLayout(layout)
        self.resize(200, 100)
        self.setStyleSheet("background-color: #f0f0f0; border: 1px solid #999;")
        
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