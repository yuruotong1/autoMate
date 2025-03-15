from pathlib import Path
from uuid import uuid4
from PIL import Image
from .base import ToolError
from util import tool

OUTPUT_DIR = "./tmp/outputs"

def get_screenshot(screen_region):
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"screenshot_{uuid4().hex}.png"
    try:
        img_io = tool.capture_screen_with_cursor()
        screenshot = Image.open(img_io)
        # Create a black mask of the same size
        black_mask = Image.new("RGBA", screenshot.size, (0, 0, 0, 255))
        # If screen_region is provided and valid, copy only that region
        if screen_region and len(screen_region) == 4:
            x1, y1, x2, y2 = screen_region
            region = screenshot.crop((x1, y1, x2, y2))
            # Paste the region onto the black mask
            black_mask.paste(region, (x1, y1, x2, y2))
            # Use the modified image as screenshot
            screenshot = black_mask
        
        screenshot.save(path)
        return screenshot, path
    except Exception as e:
        raise ToolError(f"Failed to capture screenshot: {str(e)}")