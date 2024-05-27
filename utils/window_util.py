import ctypes
class WindowUtil:
    def __init__(self):
        self.title = None

    @staticmethod
    def get_window_title():
        # 获取当前活动窗口的句柄
        hWnd = ctypes.windll.user32.GetForegroundWindow()
        # 获取窗口标题
        length = ctypes.c_int(256)
        buffer = ctypes.create_unicode_buffer(length.value)
        ctypes.windll.user32.GetWindowTextW(hWnd, buffer, length)
        title = buffer.value.split("-")[-1].strip()
        return title