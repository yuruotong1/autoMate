import os


def test_path():
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    print(desktop_path)
    file_list = []
    for dirpath, dirnames, filenames in os.walk(desktop_path):
        for filename in filenames:
            file_list.append(os.path.join(dirpath, filename))
    print(file_list)
