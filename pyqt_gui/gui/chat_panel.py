"""
Chat panel widget for displaying execution logs.
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel
from PyQt6.QtGui import QTextCursor, QTextCharFormat, QColor, QFont
from PyQt6.QtCore import Qt


class ChatPanel(QWidget):
    """Widget that displays execution log messages with color coding."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel("Execution Log")
        label.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        layout.addWidget(label)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Consolas", 9))
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #cccccc;
                border: 1px solid #3c3c3c;
            }
        """)
        layout.addWidget(self.log_text)

    def append_message(self, message: str, color: str = None):
        """
        Append a message to the log.

        Args:
            message: The message text to append
            color: Optional color name - "green", "red", "blue", "yellow"
        """
        cursor = self.log_text.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)

        fmt = QTextCharFormat()

        if color == "green":
            fmt.setForeground(QColor(78, 201, 176))  # #4ec9b0
        elif color == "red":
            fmt.setForeground(QColor(241, 76, 76))   # #f14c4c
        elif color == "blue":
            fmt.setForeground(QColor(0, 120, 212))   # #0078d4
        elif color == "yellow":
            fmt.setForeground(QColor(220, 220, 170))  # #dcdcaa
        else:
            fmt.setForeground(QColor(204, 204, 204))  # #cccccc

        cursor.setCharFormat(fmt)
        cursor.insertText(message)
        cursor.insertText("\n")

        self.log_text.setTextCursor(cursor)
        self.log_text.ensureCursorVisible()

    def info(self, message: str):
        """Append an info message (default gray)."""
        self.append_message(f"[INFO] {message}")

    def success(self, message: str):
        """Append a success message (green)."""
        self.append_message(f"[OK] {message}", "green")

    def error(self, message: str):
        """Append an error message (red)."""
        self.append_message(f"[ERROR] {message}", "red")

    def step(self, message: str):
        """Append a step message (yellow)."""
        self.append_message(f"[STEP] {message}", "yellow")

    def clear(self):
        """Clear all log messages."""
        self.log_text.clear()
