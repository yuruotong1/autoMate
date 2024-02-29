import os

from PyQt6 import uic


class QtUtil:
    @staticmethod
    def load_ui(ui_name):
        # 项目根目录
        project_root_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(project_root_path, "..", "pages", ui_name)
        return uic.loadUi(path)