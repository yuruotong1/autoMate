"""
Task panel for autoMate
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView

class TaskPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Initialize task panel UI"""
        task_layout = QVBoxLayout(self)
        task_label = QLabel("Task List")
        self.task_table = QTableWidget(0, 2)
        self.task_table.setHorizontalHeaderLabels(["Status", "Task"])
        self.task_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        task_layout.addWidget(task_label)
        task_layout.addWidget(self.task_table)
        
    def update_tasks(self, tasks):
        """Update task table with new tasks"""
        self.task_table.setRowCount(len(tasks))
        for i, (status, task) in enumerate(tasks):
            self.task_table.setItem(i, 0, QTableWidgetItem(status))
            self.task_table.setItem(i, 1, QTableWidgetItem(task))
    
    def clear(self):
        """Clear all tasks"""
        self.task_table.setRowCount(0) 