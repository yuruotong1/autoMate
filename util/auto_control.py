import sys
import os
import time
import json

from auto_control.agent.few_shot_generate_agent import FewShotGenerateAgent
# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pynput import mouse, keyboard

# Now you can import from auto_control
from auto_control.tools.screen_capture import get_screenshot

class ActionRecord:
    """Standardized data structure for all user actions"""
    def __init__(self, 
                 action_type: str,
                 position: tuple = (0, 0),
                 button: str = "",
                 key: str = "",
                 text: str = "",
                 base64_image = None):
        self.data = {
            "type": action_type,          # 'click', 'key_press', 'text_input'
            "timestamp": time.time(),
            "position": position,         # Mouse position or input position
            "button": button,             # Mouse button or keyboard key
            "key": key,                   # Keyboard key
            "text": text,                 # Input text content
            "base64_image": base64_image                # Screenshot image object
        }

class AutoControl:
    def __init__(self):
        self.auto_list = []
        self.tmp_auto_list = []
        self.text_buffer = []  # Buffer for collecting continuous text input
        self.last_key_time = 0  # Timestamp of last keypress
        self.input_timeout = 1.0  # Input timeout in seconds

    def start_listen(self):
        # Create both mouse and keyboard listeners
        self.mouse_listener = mouse.Listener(
            on_click=self.on_click,
            on_scroll=self.on_scroll)
        
        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        
        # Start both listeners
        self.mouse_listener.start()
        self.keyboard_listener.start()

    def stop_listen(self):
        self.mouse_listener.stop()
        self.keyboard_listener.stop()

    def on_click(self, x, y, button, pressed, injected):
        if not pressed:
            screenshot, _ = get_screenshot(is_base64=True)
            record = ActionRecord(
                action_type="click",
                position=(x, y),
                button=str(button),
                base64_image=screenshot
            )
            self.auto_list.append(record.data)
        
    def on_scroll(self, x, y, dx, dy, injected):
        screenshot, _ = get_screenshot(is_base64=True)
        record = ActionRecord(
            action_type="scroll",
            text=f"{'down' if dy < 0 else 'up'}",
            base64_image=screenshot
        )
        self.auto_list.append(record.data)
        
    def crop_image_if_position_in_coordinates(self, image, image_path, position, coordinates):
        """
        Check if position is within coordinates and crop image if true
        
        Args:
            image: PIL Image object
            position: tuple of (x, y) - current position
            coordinates: tuple of (x1, y1, x2, y2) - target area
        
        Returns:
            bool: True if position is in coordinates
        """
        x, y = position
        x1, y1, x2, y2 = coordinates
        
        # Check if position is within coordinates
        if (x1 <= x <= x2) and (y1 <= y <= y2):
            # Crop the image to the coordinates
            cropped_image = image.crop(coordinates)
            # Save the cropped image with proper path and format
            save_path = str(image_path).replace('.png', '_cropped.png')
            cropped_image.save(save_path, 'PNG')
            return True
        
        return False

    def on_press(self, key, injected):
        try:
            current_time = time.time()
            
            try:
                char = key.char
            except AttributeError:
                if self.text_buffer and key in [keyboard.Key.space, keyboard.Key.enter]:
                    self._process_text_buffer()
                
                # Record special key press
                screenshot, _ = get_screenshot(is_base64=True)
                record = ActionRecord(
                    action_type="key_press",
                    key=str(key),
                    base64_image=screenshot
                )
                self.auto_list.append(record.data)
                return
            
            if current_time - self.last_key_time > self.input_timeout and self.text_buffer:
                self._process_text_buffer()
            
            self.text_buffer.append(char)
            self.last_key_time = current_time
            
        except Exception as e:
            print(f"Error in on_press: {e}")
    
    def on_release(self, key, injected):
        try:
            # Process buffer immediately for these keys
            if key in [keyboard.Key.enter, keyboard.Key.tab]:
                if self.text_buffer:
                    self._process_text_buffer()
                    
            # Record special keys
            if not hasattr(key, 'char'):
                screenshot, _ = get_screenshot(is_base64=True)
                record = ActionRecord(
                    action_type="special_key",
                    key=str(key),
                    base64_image=screenshot
                )
                self.auto_list.append(record.data)
        except Exception as e:
            print(f"Error in on_release: {e}")
    
    def _process_text_buffer(self):
        if not self.text_buffer:
            return
            
        text = ''.join(self.text_buffer)
        screenshot, _ = get_screenshot(is_base64=True)
        
        record = ActionRecord(
            action_type="text_input",
            text=text,
            base64_image=screenshot
        )
        self.auto_list.append(record.data)
        
        self.text_buffer = []

    def stop_listen(self):
        """Stop listening and prepare data for LLM analysis"""
        self.keyboard_listener.stop()
        self.mouse_listener.stop()
        few_shot_generate_agent = FewShotGenerateAgent()
        return few_shot_generate_agent(self.auto_list)

if __name__ == "__main__":
    auto_control = AutoControl()
    auto_control.start_listen()

