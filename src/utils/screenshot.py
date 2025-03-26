"""
Screenshot utility module for capturing screen content
"""
from io import BytesIO
import os
from pathlib import Path
from uuid import uuid4
from PIL import Image
import pyautogui

# Output directory for screenshots
OUTPUT_DIR = "./tmp/outputs"


def get_screenshot(screen_region=None, is_cursor=True):
    """
    Capture a screenshot with or without cursor
    
    Args:
        screen_region: Optional tuple (x1, y1, x2, y2) to capture a specific region
        is_cursor: Whether to include the cursor in the screenshot
    
    Returns:
        tuple: (screenshot_image, screenshot_path)
    """
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"screenshot_{uuid4().hex}.png"
    
    if is_cursor:
        img_io = capture_screen_with_cursor()
    else:
        pyautogui_screenshot = pyautogui.screenshot()
        img_io = BytesIO()
        pyautogui_screenshot.save(img_io, 'PNG')
    
    screenshot = Image.open(img_io)
    
    # Apply region mask if specified
    if screen_region and len(screen_region) == 4:
        black_mask = Image.new("RGBA", screenshot.size, (0, 0, 0, 255))
        x1, y1, x2, y2 = screen_region
        region = screenshot.crop((x1, y1, x2, y2))
        # Paste the region onto the black mask
        black_mask.paste(region, (x1, y1, x2, y2))
        # Use the modified image as screenshot
        screenshot = black_mask
    
    screenshot.save(path)
    return screenshot, path


def capture_screen_with_cursor():
    """
    Capture the screen with cursor overlay
    
    Returns:
        BytesIO: Image buffer containing the screenshot with cursor
    """
    cursor_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                              "imgs", "cursor.png")
    screenshot = pyautogui.screenshot()
    cursor_x, cursor_y = pyautogui.position()
    
    cursor = Image.open(cursor_path)
    cursor = cursor.resize((int(cursor.width / 1.5), int(cursor.height / 1.5)))
    screenshot.paste(cursor, (cursor_x, cursor_y), cursor)
    
    img_io = BytesIO()
    screenshot.save(img_io, 'PNG')
    img_io.seek(0)
    return img_io 