import os
import pyautogui
from PIL import Image
from io import BytesIO


def capture_screen_with_cursor():
    """Local function to capture the screen with cursor."""
    cursor_path = os.path.join(os.path.dirname(__file__),"..","imgs", "cursor.png")
    screenshot = pyautogui.screenshot()
    cursor_x, cursor_y = pyautogui.position()
    cursor = Image.open(cursor_path)
    cursor = cursor.resize((int(cursor.width / 1.5), int(cursor.height / 1.5)))
    screenshot.paste(cursor, (cursor_x, cursor_y), cursor)
    img_io = BytesIO()
    screenshot.save(img_io, 'PNG')
    img_io.seek(0)
    return img_io


