"""
Task panel widget for displaying task list with status indicators.
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QHeaderView
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class TaskPanel(QWidget):
    """Widget that displays the task list with status indicators."""

    # Status icons
    STATUS_PENDING = "⬜"
    STATUS_IN_PROGRESS = "🔄"
    STATUS_COMPLETED = "✅"
    STATUS_FAILED = "❌"

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel("Task List")
        label.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        layout.addWidget(label)

        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Status", "Task"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.setColumnWidth(0, 50)
        self.table.setShowGrid(False)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #252526;
                color: #cccccc;
                border: 1px solid #3c3c3c;
                font-size: 12px;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #2d2d2d;
                color: #cccccc;
                padding: 5px;
                border: none;
                border-bottom: 1px solid #3c3c3c;
            }
        """)
        layout.addWidget(self.table)

    def update_tasks(self, tasks: list):
        """
        Initialize the task list with the given tasks.

        Args:
            tasks: List of task description strings
        """
        self.table.setRowCount(len(tasks))
        for i, task in enumerate(tasks):
            status_item = QTableWidgetItem(self.STATUS_PENDING)
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 0, status_item)
            self.table.setItem(i, 1, QTableWidgetItem(task))

    def update_task_status(self, index: int, status: str):
        """
        Update the status of a specific task.

        Args:
            index: Task index (0-based)
            status: One of STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_COMPLETED, STATUS_FAILED
        """
        if 0 <= index < self.table.rowCount():
            item = self.table.item(index, 0)
            if item:
                item.setText(status)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

    def mark_in_progress(self, index: int):
        """Mark task at index as in progress."""
        self.update_task_status(index, self.STATUS_IN_PROGRESS)

    def mark_completed(self, index: int):
        """Mark task at index as completed."""
        self.update_task_status(index, self.STATUS_COMPLETED)

    def mark_failed(self, index: int):
        """Mark task at index as failed."""
        self.update_task_status(index, self.STATUS_FAILED)

    def clear(self):
        """Clear all tasks."""
        self.table.setRowCount(0)
