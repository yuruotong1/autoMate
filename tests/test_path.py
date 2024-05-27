import os
import time


def test_path():
    desktop_path = r"C:\Users\yuruo\Desktop"
    file_list = []
    for dirpath, dirnames, filenames in os.walk(desktop_path):
        for filename in filenames:
            file_list.append(os.path.join(dirpath, filename))
    print(file_list)

def test_window():
    import ctypes
    # 获取当前活动窗口的句柄
    hWnd = ctypes.windll.user32.GetForegroundWindow()
    
    # 获取窗口标题
    length = ctypes.c_int(256)
    buffer = ctypes.create_unicode_buffer(length.value)
    ctypes.windll.user32.GetWindowTextW(hWnd, buffer, length)
    title = buffer.value.split("-")[-1]
    
    print(title)
    
if __name__ == "__main__":
    while True:
        test_window()
        time.sleep(2)

