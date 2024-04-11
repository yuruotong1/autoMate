import os


def test_path():
    desktop_path = r"C:\Users\yuruo\Desktop"
    file_list = []
    for dirpath, dirnames, filenames in os.walk(desktop_path):
        for filename in filenames:
            file_list.append(os.path.join(dirpath, filename))
    print(file_list)
