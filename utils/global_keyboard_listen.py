from pynput import mouse
from PyQt6.QtCore import pyqtSignal, QThread

from utils.window_util import WindowUtil

class GlobalKeyboardListen(QThread):
    mouse_middle_signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()

    def run(self):
        def on_click(x, y, button, pressed):
            if button == mouse.Button.middle:
                if pressed:
                    window_title = WindowUtil.get_window_title()
                    self.mouse_middle_signal.emit(window_title)
        # 创建鼠标监听器
        with mouse.Listener(on_click=on_click) as mouse_listener:
            mouse_listener.join() 