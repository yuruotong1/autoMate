"""
Task worker thread that runs the sampling loop in the background.
"""
import os
import sys

from PyQt6.QtCore import QThread

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from auto_control.llm_client import configure
from auto_control.loop import sampling_loop_sync
from auto_control.agent.vision_agent import VisionAgent
from util.download_weights import OMNI_PARSER_DIR

from worker.signals import TaskSignals


class TaskWorker(QThread):
    """
    Background worker thread that executes automation tasks.

    Runs sampling_loop_sync() in a separate thread to keep the UI responsive.
    Emits signals for each step, allowing the UI to display progress.
    """

    def __init__(
        self,
        task: str,
        model: str,
        base_url: str,
        api_key: str,
        screen_region: tuple = None,
        parent=None
    ):
        super().__init__(parent)
        self.signals = TaskSignals()

        self.task = task
        self.model = model
        self.base_url = base_url
        self.api_key = api_key
        self.screen_region = screen_region
        self._stop_requested = False

    def run(self):
        """Execute the task in the background thread."""
        try:
            # Configure LLM client
            configure(
                base_url=self.base_url,
                api_key=self.api_key,
                model=self.model
            )
            self.signals.message.emit("LLM client configured")

            # Initialize vision agent
            yolo_path = os.path.join(OMNI_PARSER_DIR, "icon_detect", "model.pt")
            vision_agent = VisionAgent(yolo_model_path=yolo_path)
            self.signals.message.emit("Vision agent initialized")

            # Create messages list
            messages = [{"role": "user", "content": self.task}]

            # Run the sampling loop
            for parsed_screen in sampling_loop_sync(
                model=self.model,
                messages=messages,
                vision_agent=vision_agent,
                screen_region=self.screen_region
            ):
                # Check for stop request
                if self._stop_requested:
                    self.signals.message.emit("Task stopped by user")
                    return

                # Emit the parsed screen for UI update
                self.signals.step_completed.emit(parsed_screen)

            # Task completed
            self.signals.finished.emit(f"Task completed: {self.task}")

        except Exception as e:
            self.signals.error.emit(f"Error: {str(e)}")
            import traceback
            traceback.print_exc()

    def stop(self):
        """Request the worker to stop."""
        self._stop_requested = True
