import base64
import time
from typing import Literal, TypedDict
from PIL import Image
from anthropic.types.beta import BetaToolComputerUse20241022Param
from .base import BaseAnthropicTool, ToolError, ToolResult
from .screen_capture import get_screenshot
import pyautogui
import pyperclip
import platform

OUTPUT_DIR = "./tmp/outputs"
TYPING_DELAY_MS = 12
TYPING_GROUP_SIZE = 50


Action = Literal[
    "key",
    "type",
    "mouse_move",
    "left_click",
    "left_click_drag",
    "right_click",
    "middle_click",
    "double_click",
    "screenshot",
    "cursor_position",
    "hover",
    "wait",
    "scroll_up",
    "scroll_down",
    "None"
]

class Resolution(TypedDict):
    width: int
    height: int

MAX_SCALING_TARGETS: dict[str, Resolution] = {
    "XGA": Resolution(width=1024, height=768),  # 4:3
    "WXGA": Resolution(width=1280, height=800),  # 16:10
    "FWXGA": Resolution(width=1366, height=768),  # ~16:9
}

class ComputerToolOptions(TypedDict):
    display_height_px: int
    display_width_px: int
    display_number: int | None

def chunks(s: str, chunk_size: int) -> list[str]:
    return [s[i : i + chunk_size] for i in range(0, len(s), chunk_size)]

class ComputerTool(BaseAnthropicTool):
    """
    A tool that allows the agent to interact with the screen, keyboard, and mouse of the current computer.

    Adapted for Windows using 'pyautogui'.
    """
    name: Literal["computer"] = "computer"
    api_type: Literal["computer_20241022"] = "computer_20241022"
    width: int
    height: int
    display_num: int | None
    _screenshot_delay = 2.0

    @property
    def options(self) -> ComputerToolOptions:
        return {
            "display_width_px": self.width,
            "display_height_px": self.height,
            "display_number": self.display_num,
        }

    def to_params(self) -> BetaToolComputerUse20241022Param:
        return {"name": self.name, "type": self.api_type, **self.options}


    def __init__(self):
        super().__init__()
        self.display_num = None
        self.offset_x = 0
        self.offset_y = 0
        self.width, self.height = pyautogui.size()
        self.key_conversion = {"Page_Down": "pagedown",
                               "Page_Up": "pageup",
                               "Super_L": "win",
                               "Escape": "esc"}
    async def __call__(
        self,
        *,
        action: Action,
        text: str | None = None,
        coordinate: tuple[int, int] | None = None,
        **kwargs,
    ):
        print(f"action: {action}, text: {text}, coordinate: {coordinate},")
        if action in ("mouse_move", "left_click_drag"):
            if coordinate is None:
                raise ToolError(f"coordinate is required for {action}")
            if text is not None:
                raise ToolError(f"text is not accepted for {action}")
            if not isinstance(coordinate, (list, tuple)) or len(coordinate) != 2:
                raise ToolError(f"{coordinate} must be a tuple of length 2")
            # if not all(isinstance(i, int) and i >= 0 for i in coordinate):
            if not all(isinstance(i, int) for i in coordinate):
                raise ToolError(f"{coordinate} must be a tuple of non-negative ints")
           
            x, y = coordinate
            print(f"mouse move to {x}, {y}")
            if action == "mouse_move":
                pyautogui.moveTo(x, y)
                return ToolResult(output=f"Moved mouse to ({x}, {y})")
            elif action == "left_click_drag":
                current_x, current_y = pyautogui.position()
                pyautogui.dragTo(x, y, duration=0.5)
                return ToolResult(output=f"Dragged mouse from ({current_x}, {current_y}) to ({x}, {y})")
        if action in ("key", "type"):
            if text is None:
                raise ToolError(f"text is required for {action}")
            if coordinate is not None:
                raise ToolError(f"coordinate is not accepted for {action}")
            if not isinstance(text, str):
                raise ToolError(output=f"{text} must be a string")
            if action == "key":
                # Handle key combinations
                keys = text.split('+')
                for key in keys:
                    key = self.key_conversion.get(key.strip(), key.strip())
                    key = key.lower()
                    pyautogui.keyDown(key)
                for key in reversed(keys):
                    key = self.key_conversion.get(key.strip(), key.strip())
                    key = key.lower()
                    pyautogui.keyUp(key)
                return ToolResult(output=f"Pressed keys: {text}")
            elif action == "type":
                # default click before type TODO: check if this is needed
                # Save user's old clipboard
                clipboard_data = pyperclip.paste()
                pyperclip.copy(text)
                pyautogui.click()
                if platform.system() == 'Darwin':
                    pyautogui.hotkey('command', 'v', interval=0.1)
                else: # TODO: double check what works on windows
                    pyautogui.hotkey('ctrl', 'v')
                # Copy old data back to clipboard
                pyperclip.copy(clipboard_data)
                screenshot_base64 = (await self.screenshot()).base64_image
                return ToolResult(output=text, base64_image=screenshot_base64)
        if action in (
            "left_click",
            "right_click",
            "double_click",
            "middle_click",
            "screenshot",
            "cursor_position",
            "left_press",
        ):
            if text is not None:
                raise ToolError(f"text is not accepted for {action}")
            if coordinate is not None:
                raise ToolError(f"coordinate is not accepted for {action}")
            if action == "screenshot":
                return await self.screenshot()
            elif action == "cursor_position":
                x, y = pyautogui.position()
                # 直接返回原始坐标，不进行缩放
                return ToolResult(output=f"X={x},Y={y}")
            else:
                if action == "left_click":
                    pyautogui.click()
                elif action == "right_click":
                    pyautogui.rightClick()
                    # 等待5秒，等待菜单弹出
                    time.sleep(5)
                elif action == "middle_click":
                    pyautogui.middleClick()
                elif action == "double_click":
                    pyautogui.doubleClick()
                elif action == "left_press":
                    pyautogui.mouseDown()
                    time.sleep(1)
                    pyautogui.mouseUp()
                return ToolResult(output=f"Performed {action}")
        if action in ("scroll_up", "scroll_down"):
            if action == "scroll_up":
                pyautogui.scroll(100)
            elif action == "scroll_down":
                pyautogui.scroll(-100)
            return ToolResult(output=f"Performed {action}")
        if action == "hover":
            return ToolResult(output=f"Performed {action}")
        if action == "wait":
            time.sleep(1)
            return ToolResult(output=f"Performed {action}")
        raise ToolError(f"Invalid action: {action}")
    
    async def screenshot(self):
        if not hasattr(self, 'target_dimension'):
            screenshot = self.padding_image(screenshot)
            self.target_dimension = MAX_SCALING_TARGETS["WXGA"]
        width, height = self.target_dimension["width"], self.target_dimension["height"]
        screenshot, path = get_screenshot(resize=True, target_width=width, target_height=height)
        time.sleep(0.7) # avoid async error as actions take time to complete
        return ToolResult(base64_image=base64.b64encode(path.read_bytes()).decode())

    def padding_image(self, screenshot):
        """Pad the screenshot to 16:10 aspect ratio, when the aspect ratio is not 16:10."""
        _, height = screenshot.size
        new_width = height * 16 // 10

        padding_image = Image.new("RGB", (new_width, height), (255, 255, 255))
        # padding to top left
        padding_image.paste(screenshot, (0, 0))
        return padding_image
