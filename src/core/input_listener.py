"""
Input listener module for keyboard and mouse events
"""
from pynput import mouse, keyboard
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

from src.utils.screenshot import get_screenshot


class InputListener(QObject):
    """
    Class for listening to keyboard and mouse input events
    Emits signals when actions are detected
    """
    action_detected = pyqtSignal(dict)
    terminated = pyqtSignal()

    def __init__(self):
        """Initialize the input listener"""
        super().__init__()
        self.mouse_listener = None
        self.keyboard_listener = None

    @pyqtSlot()
    def start_listen(self):
        """Start listening for mouse and keyboard events"""
        # Create both mouse and keyboard listeners
        self.mouse_listener = mouse.Listener(
            on_click=self.on_click,
            on_scroll=self.on_scroll
        )
        
        self.keyboard_listener = keyboard.Listener(
            on_release=self.on_release
        )
        
        # Start both listeners
        self.mouse_listener.start()
        self.keyboard_listener.start()

    def on_click(self, x, y, button, pressed, injected):
        """
        Handle mouse click events
        Only emit on release (when pressed is False)
        """
        if not pressed:
            screenshot, _ = get_screenshot(is_base64=True)
            self.action_detected.emit({
                "type": "mouse",
                "event": button.name + " click",
                "position": (x, y),
                "base64_image": screenshot
            })

    def on_scroll(self, x, y, dx, dy, injected):
        """Handle mouse scroll events"""
        screenshot, _ = get_screenshot(is_base64=True)
        scroll_direction = 'down' if dy < 0 else 'up'
        self.action_detected.emit({
            "type": "mouse",
            "event": f"scroll {scroll_direction}",
            "position": (x, y),
            "base64_image": screenshot
        })

    def on_release(self, key, injected):
        """Handle keyboard release events"""
        screenshot, _ = get_screenshot(is_base64=True)
        self.action_detected.emit({
            "type": "keyboard",
            "event": str(key),
            "base64_image": screenshot
        })

    def stop_listen(self):
        """Stop all listeners and emit terminated signal"""
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        self.terminated.emit() 