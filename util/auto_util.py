import os
import platform
import pyautogui
from enum import Enum

import pyperclip
class AppName(Enum):
    WECHAT = "wechat"
   

class AutoUtil:
    def __init__(self, app_name: AppName):
        self.img_dir = os.path.join(os.path.dirname(__file__),"..", "imgs", app_name.value)

    def click_multi_img(self, img_names, offset_x=0, offset_y=0, minSearchTime=0):
        for img_name in img_names:
            self.find_click_img(img_name, offset_x, offset_y, minSearchTime)
    
    def find_click_img(self, img_name, offset_x=0, offset_y=0, minSearchTime=0):
        img_path = os.path.join(self.img_dir, img_name + ".png")
        img = pyautogui.locateOnScreen(img_path, minSearchTime=minSearchTime)
        x,y = pyautogui.center(img)
        # Add offset to click position
        pyautogui.click(x + offset_x, y + offset_y)

    def send_text(self, text):
        clipboard_data = pyperclip.paste()
        pyperclip.copy(text)
        if platform.system() == 'Darwin':
            pyautogui.hotkey('command', 'v', interval=0.1)
        else:
            pyautogui.hotkey('ctrl', 'v')
        # Copy old data back to clipboard
        pyperclip.copy(clipboard_data)
