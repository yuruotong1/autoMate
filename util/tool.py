import os
import shlex
import subprocess
import threading
import traceback
import pyautogui
from PIL import Image
from io import BytesIO


computer_control_lock = threading.Lock()
def execute_command(command, shell=False):
    """Local function to execute a command."""
    with computer_control_lock:
        if isinstance(command, str) and not shell:
            command = shlex.split(command)

        # Expand user directory
        for i, arg in enumerate(command):
            if arg.startswith("~/"):
                command[i] = os.path.expanduser(arg)

        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell, text=True, timeout=120)
            return {
                'status': 'success',
                'output': result.stdout,
                'error': result.stderr,
                'returncode': result.returncode
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

def capture_screen_with_cursor():
    """Local function to capture the screen with cursor."""
    cursor_path = os.path.join(os.path.dirname(__file__),"..","resources", "cursor.png")
    screenshot = pyautogui.screenshot()
    cursor_x, cursor_y = pyautogui.position()
    cursor = Image.open(cursor_path)
    cursor = cursor.resize((int(cursor.width / 1.5), int(cursor.height / 1.5)))
    screenshot.paste(cursor, (cursor_x, cursor_y), cursor)
    img_io = BytesIO()
    screenshot.save(img_io, 'PNG')
    img_io.seek(0)
    return img_io


