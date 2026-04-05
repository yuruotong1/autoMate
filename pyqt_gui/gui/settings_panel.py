"""
Settings panel widget for API configuration and task input.
"""
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton,
    QHBoxLayout, QLabel, QTextEdit, QGroupBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class SettingsPanel(QWidget):
    """Widget for API settings, task input, and execution controls."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

        # Load defaults from environment
        self.base_url_input.setText(os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"))
        self.api_key_input.setText(os.environ.get("OPENAI_API_KEY", ""))
        self.model_input.setText(os.environ.get("OPENAI_MODEL", "gpt-4o"))

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # API Settings Group
        settings_group = QGroupBox("API Settings")
        settings_group.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        settings_layout = QFormLayout(settings_group)

        self.base_url_input = QLineEdit()
        self.base_url_input.setPlaceholderText("https://api.openai.com/v1")
        self.base_url_input.setMinimumWidth(250)
        settings_layout.addRow("Base URL:", self.base_url_input)

        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("sk-...")
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        settings_layout.addRow("API Key:", self.api_key_input)

        self.model_input = QLineEdit()
        self.model_input.setPlaceholderText("gpt-4o")
        settings_layout.addRow("Model:", self.model_input)

        main_layout.addWidget(settings_group)

        # Screen Region Group
        region_group = QGroupBox("Screen Region (Optional)")
        region_group.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        region_layout = QVBoxLayout(region_group)

        self.region_label = QLabel("Full screen (default)")
        region_layout.addWidget(self.region_label)

        self.select_region_btn = QPushButton("Select Region")
        self.select_region_btn.clicked.connect(self._on_select_region)
        region_layout.addWidget(self.select_region_btn)

        self.screen_region = None
        main_layout.addWidget(region_group)

        # Task Input Group
        task_group = QGroupBox("Task")
        task_group.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        task_layout = QVBoxLayout(task_group)

        self.task_input = QTextEdit()
        self.task_input.setPlaceholderText("Describe the task you want to automate...\n\nExample: Open Chrome and search for latest AI news")
        self.task_input.setMaximumHeight(100)
        self.task_input.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #cccccc;
                border: 1px solid #3c3c3c;
                font-family: 'Segoe UI';
            }
        """)
        task_layout.addWidget(self.task_input)

        main_layout.addWidget(task_group)

        # Control Buttons
        btn_layout = QHBoxLayout()

        self.start_btn = QPushButton("▶ Start")
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:disabled {
                background-color: #3c3c3c;
                color: #808080;
            }
        """)
        btn_layout.addWidget(self.start_btn)

        self.stop_btn = QPushButton("⏹ Stop")
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #c42b1c;
                color: white;
                border: none;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #a5261b;
            }
            QPushButton:disabled {
                background-color: #3c3c3c;
                color: #808080;
            }
        """)
        btn_layout.addWidget(self.stop_btn)

        main_layout.addLayout(btn_layout)
        main_layout.addStretch()

    def _on_select_region(self):
        """Handle screen region selection."""
        # Defer import to avoid circular dependencies
        try:
            from util.screen_selector import ScreenSelector
            selector = ScreenSelector()
            region = selector.select()
            if region:
                self.screen_region = region
                self.region_label.setText(f"Selected: {region}")
            else:
                self.screen_region = None
                self.region_label.setText("Full screen (default)")
        except Exception as e:
            self.region_label.setText(f"Selection failed: {e}")

    def get_settings(self) -> dict:
        """
        Get the current settings.

        Returns:
            dict with keys: base_url, api_key, model, screen_region
        """
        return {
            "base_url": self.base_url_input.text().strip(),
            "api_key": self.api_key_input.text().strip(),
            "model": self.model_input.text().strip(),
            "screen_region": self.screen_region
        }

    def get_task(self) -> str:
        """Get the task description."""
        return self.task_input.toPlainText().strip()

    def set_running(self, running: bool):
        """Set the UI state to running or stopped."""
        self.start_btn.setEnabled(not running)
        self.stop_btn.setEnabled(running)
        self.task_input.setEnabled(not running)
        self.base_url_input.setEnabled(not running)
        self.api_key_input.setEnabled(not running)
        self.model_input.setEnabled(not running)

    def clear_task(self):
        """Clear the task input."""
        self.task_input.clear()
