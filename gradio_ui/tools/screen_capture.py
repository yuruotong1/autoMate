from pathlib import Path
from uuid import uuid4
from PIL import Image
from .base import ToolError
from util import tool

OUTPUT_DIR = "./tmp/outputs"

def get_screenshot():
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"screenshot_{uuid4().hex}.png"
    try:
        img_io = tool.capture_screen_with_cursor()
        screenshot = Image.open(img_io)        
        screenshot.save(path)
        return screenshot, path
    except Exception as e:
        raise ToolError(f"Failed to capture screenshot: {str(e)}")