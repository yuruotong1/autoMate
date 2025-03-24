"""
Hotkey editing widget
"""
import keyboard
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton

# Default stop hotkey
DEFAULT_STOP_HOTKEY = "alt+f3"

class HotkeyEdit(QWidget):
    """Widget for recording hotkey combinations"""
    
    def __init__(self, hotkey="", parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.hotkey_input = QLineEdit(hotkey)
        self.hotkey_input.setReadOnly(True)
        self.hotkey_input.setPlaceholderText("Click to record hotkey")
        
        self.record_btn = QPushButton("Record")
        self.record_btn.clicked.connect(self.start_recording)
        
        layout.addWidget(self.hotkey_input, 1)
        layout.addWidget(self.record_btn)
        
        self.recording = False
        self.keys_pressed = set()
        
    def start_recording(self):
        """Start recording a new hotkey"""
        if self.recording:
            self.stop_recording()
            return
            
        self.hotkey_input.setText("Press keys...")
        self.record_btn.setText("Stop")
        self.recording = True
        self.keys_pressed = set()
        
        # Hook global events
        keyboard.hook(self.on_key_event)
        
    def stop_recording(self):
        """Stop recording and set the hotkey"""
        keyboard.unhook(self.on_key_event)
        self.recording = False
        self.record_btn.setText("Record")
        
        # Convert keys to hotkey string
        if self.keys_pressed:
            hotkey = '+'.join(sorted(self.keys_pressed))
            self.hotkey_input.setText(hotkey)
        else:
            self.hotkey_input.setText("")
    
    def on_key_event(self, event):
        """Handle key events during recording"""
        if not self.recording:
            return
            
        # Skip key up events
        if not event.event_type == keyboard.KEY_DOWN:
            return
            
        # Get key name
        key_name = event.name.lower()
        
        # Special handling for modifier keys
        if key_name in ['ctrl', 'alt', 'shift', 'windows']:
            self.keys_pressed.add(key_name)
        else:
            self.keys_pressed.add(key_name)
            
        # Show current keys
        self.hotkey_input.setText('+'.join(sorted(self.keys_pressed)))
        
        # Stop recording if user presses Escape alone
        if len(self.keys_pressed) == 1 and 'esc' in self.keys_pressed:
            self.keys_pressed.clear()
            self.stop_recording()
    
    def get_hotkey(self):
        """Get the current hotkey string"""
        return self.hotkey_input.text()
        
    def set_hotkey(self, hotkey):
        """Set the hotkey string"""
        self.hotkey_input.setText(hotkey) 