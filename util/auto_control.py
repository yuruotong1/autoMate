import sys
import os
import time

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auto_control.agent.vision_agent import VisionAgent
from util.download_weights import MODEL_DIR
from pynput import mouse, keyboard

# Now you can import from auto_control
from auto_control.tools.screen_capture import get_screenshot

class AutoControl:
    def __init__(self):
        self.auto_list = []

    def start_listen(self):
        # Create both mouse and keyboard listeners
        mouse_listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll)
        
        keyboard_listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        
        # Start both listeners
        mouse_listener.start()
        keyboard_listener.start()
        
        # Keep the program running until keyboard listener stops
        keyboard_listener.join()
        
        # After keyboard stops (ESC pressed), stop mouse listener too
        mouse_listener.stop()

    def on_move(self, x, y, injected):
        print('Pointer moved to {}; it was {}'.format(
            (x, y), 'faked' if injected else 'not faked'))

    def on_click(self, x, y, button, pressed, injected):
        print('Mouse {} {} at {}; it was {}'.format(
            button, 
            'Pressed' if pressed else 'Released',
            (x, y), 
            'faked' if injected else 'not faked'))
        if not pressed:
            # wait right click window
            if button == mouse.Button.right:
                    time.sleep(1)
            screenshot, path = get_screenshot(is_cursor=False)
            self.auto_list.append(
                {"button": button, 
                 "pressed": pressed, 
                 "position": (x, y), 
                 "path": path,
                 "image": screenshot
                 }
            )
            

    def on_scroll(self, x, y, dx, dy, injected):
        print('Scrolled {} at {}; it was {}'.format(
            'down' if dy < 0 else 'up',
            (x, y), 'faked' if injected else 'not faked'))
        
    def on_press(self, key, injected):
        try:
            print('alphanumeric key {} pressed; it was {}'.format(
                key.char, 'faked' if injected else 'not faked'))
        except AttributeError:
            print('special key {} pressed'.format(
                key))

    def on_release(self, key, injected):
        print('{} released; it was {}'.format(
            key, 'faked' if injected else 'not faked'))

        if key == keyboard.Key.esc:
            
            print("self.auto_list", self.auto_list)
            vision_agent = VisionAgent(yolo_model_path=os.path.join(MODEL_DIR, "icon_detect", "model.pt"))
            
            for item in self.auto_list:
                element_list =vision_agent(str(item["path"]))
                for element in element_list:
                    if self.crop_image_if_position_in_coordinates(item["image"], item["path"], item["position"], element.coordinates):
                        break
            # Stop listener
            return False

        

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

if __name__ == "__main__":
    auto_control = AutoControl()
    auto_control.start_listen()

