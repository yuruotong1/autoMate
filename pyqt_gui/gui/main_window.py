"""
Main application window for autoMate PyQt6 GUI.
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSplitter,
    QMessageBox, QLabel
)
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QFont

from gui.screenshot_viewer import ScreenshotViewer
from gui.chat_panel import ChatPanel
from gui.task_panel import TaskPanel
from gui.settings_panel import SettingsPanel
from worker.task_worker import TaskWorker


class MainWindow(QMainWindow):
    """Main application window composing all panels."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("autoMate Control Center")
        self.setMinimumSize(1200, 800)

        # Worker instance
        self.worker = None

        # Setup UI
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        """Setup the main UI layout."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left panel: Settings + Tasks
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)

        self.settings_panel = SettingsPanel()
        self.task_panel = TaskPanel()

        left_layout.addWidget(self.settings_panel)
        left_layout.addWidget(self.task_panel, 1)

        # Right panel: Screenshot + Log
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)

        self.screenshot_viewer = ScreenshotViewer()
        self.chat_panel = ChatPanel()

        right_layout.addWidget(self.screenshot_viewer, 2)
        right_layout.addWidget(self.chat_panel, 1)

        # Add to splitter
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([350, 850])  # 1/3 left, 2/3 right

        main_layout.addWidget(splitter)

        # Apply dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QGroupBox {
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                margin-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)

    def _connect_signals(self):
        """Connect signals between components."""
        # Settings buttons to window methods
        self.settings_panel.start_btn.clicked.connect(self._on_start_clicked)
        self.settings_panel.stop_btn.clicked.connect(self._on_stop_clicked)

    @pyqtSlot()
    def _on_start_clicked(self):
        """Handle Start button click."""
        task = self.settings_panel.get_task()
        if not task:
            QMessageBox.warning(self, "No Task", "Please enter a task description.")
            return

        settings = self.settings_panel.get_settings()

        # Validate settings
        if not settings["api_key"]:
            QMessageBox.warning(self, "Missing API Key", "Please enter your API key.")
            return
        if not settings["base_url"]:
            QMessageBox.warning(self, "Missing Base URL", "Please enter the API base URL.")
            return
        if not settings["model"]:
            QMessageBox.warning(self, "Missing Model", "Please enter a model name.")
            return

        # Update UI state
        self.settings_panel.set_running(True)
        self.task_panel.clear()
        self.chat_panel.clear()
        self.screenshot_viewer.clear()

        # Log start
        self.chat_panel.info(f"Starting task: {task[:50]}{'...' if len(task) > 50 else ''}")
        self.chat_panel.info(f"Model: {settings['model']}")
        self.chat_panel.info(f"Base URL: {settings['base_url']}")

        # Create and start worker
        self.worker = TaskWorker(
            task=task,
            model=settings["model"],
            base_url=settings["base_url"],
            api_key=settings["api_key"],
            screen_region=settings.get("screen_region")
        )

        # Connect worker signals
        self.worker.signals.step_completed.connect(self._on_step_completed)
        self.worker.signals.task_list_received.connect(self._on_task_list_received)
        self.worker.signals.task_updated.connect(self._on_task_updated)
        self.worker.signals.message.connect(self._on_message)
        self.worker.signals.finished.connect(self._on_finished)
        self.worker.signals.error.connect(self._on_error)

        self.worker.start()

    @pyqtSlot()
    def _on_stop_clicked(self):
        """Handle Stop button click."""
        if self.worker and self.worker.isRunning():
            self.chat_panel.step("Stopping task...")
            self.worker.stop()

    @pyqtSlot(dict)
    def _on_step_completed(self, parsed_screen: dict):
        """Handle step completed signal."""
        # Update screenshot
        self.screenshot_viewer.update_screenshot(parsed_screen)

        # Update task status based on progress
        parsed_content = parsed_screen.get('parsed_content_list', [])
        self.chat_panel.step(f"Detected {len(parsed_content)} UI elements")

    @pyqtSlot(list)
    def _on_task_list_received(self, tasks: list):
        """Handle task list received signal."""
        self.task_panel.update_tasks(tasks)
        task_str = ", ".join(tasks[:3])
        if len(tasks) > 3:
            task_str += f" ... (+{len(tasks) - 3} more)"
        self.chat_panel.info(f"Task plan: {task_str}")

    @pyqtSlot(int, str)
    def _on_task_updated(self, index: int, status: str):
        """Handle task status update signal."""
        self.task_panel.update_task_status(index, status)

    @pyqtSlot(str)
    def _on_message(self, message: str):
        """Handle generic message signal."""
        self.chat_panel.info(message)

    @pyqtSlot(str)
    def _on_finished(self, message: str):
        """Handle task finished signal."""
        self.chat_panel.success(message)
        self.settings_panel.set_running(False)

        # Mark all pending tasks as completed
        for i in range(self.task_panel.table.rowCount()):
            item = self.task_panel.table.item(i, 0)
            if item and item.text() != "✅":
                self.task_panel.mark_completed(i)

    @pyqtSlot(str)
    def _on_error(self, message: str):
        """Handle error signal."""
        self.chat_panel.error(message)
        self.settings_panel.set_running(False)

    def closeEvent(self, event):
        """Handle window close event."""
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait(2000)  # Wait up to 2 seconds
        event.accept()
