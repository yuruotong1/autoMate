"""
Recorder panel UI for controlling voice and input recording
"""
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QFileDialog, QListWidget, QListWidgetItem,
    QSplitter, QTextEdit, QMessageBox, QStatusBar
)
from PyQt6.QtCore import Qt, pyqtSlot, QSize
from PyQt6.QtGui import QFont, QColor

from src.core.recorder_manager import RecorderManager


class RecorderPanel(QWidget):
    """
    Panel for recording user actions and voice, and visualizing
    the extracted workflows
    """
    
    def __init__(self, parent=None):
        """Initialize recorder panel"""
        super().__init__(parent)
        self.recorder_manager = RecorderManager()
        
        # Connect signals
        self.recorder_manager.recording_started.connect(self.on_recording_started)
        self.recorder_manager.recording_stopped.connect(self.on_recording_stopped)
        self.recorder_manager.sequence_updated.connect(self.on_sequence_updated)
        self.recorder_manager.status_changed.connect(self.on_status_changed)
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        main_layout = QVBoxLayout(self)
        
        # Control buttons
        control_layout = QHBoxLayout()
        
        self.record_button = QPushButton("开始录制")
        self.record_button.clicked.connect(self.toggle_recording)
        self.record_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        
        self.save_button = QPushButton("保存录制")
        self.save_button.clicked.connect(self.save_recording)
        self.save_button.setEnabled(False)
        
        self.load_button = QPushButton("加载录制")
        self.load_button.clicked.connect(self.load_recording)
        
        self.analyze_button = QPushButton("分析工作流")
        self.analyze_button.clicked.connect(self.analyze_workflow)
        self.analyze_button.setEnabled(False)
        
        control_layout.addWidget(self.record_button)
        control_layout.addWidget(self.save_button)
        control_layout.addWidget(self.load_button)
        control_layout.addWidget(self.analyze_button)
        
        main_layout.addLayout(control_layout)
        
        # Status label
        self.status_label = QLabel("就绪")
        self.status_label.setStyleSheet("font-weight: bold; padding: 5px; color: #333;")
        main_layout.addWidget(self.status_label)
        
        # Create splitter for sequence and workflow views
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(1)
        splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #dddddd;
            }
        """)
        
        # Mixed sequence list
        sequence_container = QWidget()
        sequence_layout = QVBoxLayout(sequence_container)
        sequence_layout.setContentsMargins(0, 0, 0, 0)
        
        sequence_header = QLabel("录制序列")
        sequence_header.setStyleSheet("font-weight: bold; font-size: 14px; padding: 5px; background-color: #f5f5f5;")
        sequence_layout.addWidget(sequence_header)
        
        self.sequence_list = QListWidget()
        self.sequence_list.setMinimumWidth(400)
        self.sequence_list.setAlternatingRowColors(True)
        self.sequence_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #dddddd;
                border-radius: 4px;
                padding: 2px;
                background-color: white;
            }
            QListWidget::item {
                padding: 4px;
                border-bottom: 1px solid #eeeeee;
            }
            QListWidget::item:alternate {
                background-color: #f9f9f9;
            }
        """)
        
        sequence_layout.addWidget(self.sequence_list)
        
        # Workflow results view
        workflow_container = QWidget()
        workflow_layout = QVBoxLayout(workflow_container)
        workflow_layout.setContentsMargins(0, 0, 0, 0)
        
        workflow_header = QLabel("工作流分析")
        workflow_header.setStyleSheet("font-weight: bold; font-size: 14px; padding: 5px; background-color: #f5f5f5;")
        workflow_layout.addWidget(workflow_header)
        
        self.workflow_text = QTextEdit()
        self.workflow_text.setReadOnly(True)
        self.workflow_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #dddddd;
                border-radius: 4px;
                padding: 8px;
                background-color: white;
                font-family: Arial, sans-serif;
            }
        """)
        
        workflow_layout.addWidget(self.workflow_text)
        
        # Add containers to splitter
        splitter.addWidget(sequence_container)
        splitter.addWidget(workflow_container)
        
        # Set splitter proportions
        splitter.setSizes([400, 400])
        
        main_layout.addWidget(splitter, 1)  # 1 = stretch factor
        
        # Status bar for detailed status
        self.status_bar = QStatusBar()
        self.status_bar.setSizeGripEnabled(False)
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #f5f5f5;
                color: #333333;
                border-top: 1px solid #dddddd;
            }
        """)
        main_layout.addWidget(self.status_bar)
        
        # Set layout
        self.setLayout(main_layout)
        self.setMinimumSize(800, 600)
        
        # Initial status
        self.status_bar.showMessage('系统就绪，点击"开始录制"按钮开始捕获键盘鼠标和语音')
        
    def toggle_recording(self):
        """Toggle recording state"""
        if not self.recorder_manager.is_recording:
            self.recorder_manager.start_recording()
        else:
            self.recorder_manager.stop_recording()
            
    @pyqtSlot()
    def on_recording_started(self):
        """Handle recording started event"""
        self.record_button.setText("停止录制")
        self.record_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e53935;
            }
            QPushButton:pressed {
                background-color: #d32f2f;
            }
        """)
        self.save_button.setEnabled(False)
        self.load_button.setEnabled(False)
        self.analyze_button.setEnabled(False)
        self.status_label.setText("正在录制中...")
        self.status_bar.showMessage('正在录制，系统将捕获您的键盘鼠标操作和语音指令...')
        self.sequence_list.clear()
        self.workflow_text.clear()
        
    @pyqtSlot()
    def on_recording_stopped(self):
        """Handle recording stopped event"""
        self.record_button.setText("开始录制")
        self.record_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        self.save_button.setEnabled(True)
        self.load_button.setEnabled(True)
        self.analyze_button.setEnabled(True)
        self.status_label.setText("录制完成")
        self.status_bar.showMessage('录制已完成，您可以保存或分析工作流')
        
    @pyqtSlot(list)
    def on_sequence_updated(self, sequence):
        """
        Update the sequence list when new events are recorded
        
        Args:
            sequence: The updated mixed sequence
        """
        self.sequence_list.clear()
        
        for item in sequence:
            item_type = item.get("type", "")
            timestamp = item.get("timestamp", 0)
            
            if item_type == "utterance":
                text = item.get("text", "")
                list_item = QListWidgetItem(f"[语音] {text}")
                list_item.setBackground(QColor("#e8f5e9"))  # Light green background
                list_item.setForeground(QColor("#2e7d32"))  # Dark green text
                font = list_item.font()
                font.setBold(True)
                list_item.setFont(font)
            elif item_type == "action":
                event = item.get("event", "")
                position = item.get("position", None)
                
                if position:
                    position_text = f" @ ({position[0]}, {position[1]})"
                else:
                    position_text = ""
                    
                list_item = QListWidgetItem(f"[动作] {event}{position_text}")
            else:
                continue
                
            self.sequence_list.addItem(list_item)
            
        # Scroll to bottom
        self.sequence_list.scrollToBottom()
        
        # Update status
        self.status_bar.showMessage(f'已录制 {len(sequence)} 个事件')
        
    @pyqtSlot(str)
    def on_status_changed(self, status):
        """
        Update status when it changes
        
        Args:
            status: New status message
        """
        self.status_bar.showMessage(status, 5000)  # Show for 5 seconds
        
    def save_recording(self):
        """Save the current recording to a file"""
        if not self.recorder_manager.mixed_sequence:
            QMessageBox.warning(self, "警告", "没有可保存的录制数据")
            return
            
        filename, _ = QFileDialog.getSaveFileName(
            self, "保存录制", "", "JSON Files (*.json)"
        )
        
        if filename:
            success = self.recorder_manager.save_sequence(filename)
            if success:
                self.status_label.setText(f"已保存到 {filename}")
                self.status_bar.showMessage(f'成功保存录制到: {filename}')
            else:
                QMessageBox.critical(self, "错误", "保存录制失败")
                
    def load_recording(self):
        """Load a recording from a file"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "加载录制", "", "JSON Files (*.json)"
        )
        
        if filename:
            success = self.recorder_manager.load_sequence(filename)
            if success:
                self.status_label.setText(f"已加载 {filename}")
                self.status_bar.showMessage(f'成功加载录制: {filename}')
                self.analyze_button.setEnabled(True)
                self.save_button.setEnabled(True)
            else:
                QMessageBox.critical(self, "错误", "加载录制失败")
                
    def analyze_workflow(self):
        """Analyze the current recording and extract workflows"""
        if not self.recorder_manager.mixed_sequence:
            QMessageBox.warning(self, "警告", "没有可分析的录制数据")
            return
            
        self.status_bar.showMessage('正在分析工作流...')
        
        try:
            workflows = self.recorder_manager.get_workflow_segments()
            
            if not workflows:
                self.workflow_text.setText("未找到工作流片段")
                self.status_bar.showMessage('分析完成，未找到工作流片段')
                return
                
            # Format and display workflows
            result_text = "# 提取的工作流\n\n"
            
            for i, workflow in enumerate(workflows):
                intent = workflow.get("intent", "")
                actions = workflow.get("actions", [])
                
                result_text += f"## 片段 {i+1}: \"{intent}\"\n\n"
                
                if actions:
                    result_text += "操作序列:\n"
                    for j, action in enumerate(actions):
                        event = action.get("event", "")
                        result_text += f"{j+1}. {event}\n"
                else:
                    result_text += "没有相关的操作\n"
                    
                result_text += "\n---\n\n"
                
            self.workflow_text.setText(result_text)
            self.status_bar.showMessage(f'工作流分析完成，找到 {len(workflows)} 个片段')
        except Exception as e:
            self.status_bar.showMessage(f'分析工作流时出错: {str(e)}')
            QMessageBox.critical(self, "错误", f'分析工作流失败: {str(e)}') 