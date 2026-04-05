"""
PyQt6 Signal definitions for task worker communication.
"""
from PyQt6.QtCore import QObject, pyqtSignal


class TaskSignals(QObject):
    """Signals emitted by TaskWorker to communicate with the UI."""

    # Emitted when a step completes with parsed screen data
    # dict contains: base64_image, image (PIL), parsed_content_list, width, height
    step_completed = pyqtSignal(dict)

    # Emitted when task list is first received from LLM
    # list of task strings
    task_list_received = pyqtSignal(list)

    # Emitted to update a task's status
    # (task_index, status_icon_string)
    task_updated = pyqtSignal(int, str)

    # Emitted for log/status messages
    # str message
    message = pyqtSignal(str)

    # Emitted when execution finishes
    # str final status message
    finished = pyqtSignal(str)

    # Emitted on error
    # str error message
    error = pyqtSignal(str)
