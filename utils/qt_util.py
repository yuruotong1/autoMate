import os

from PyQt6 import uic


class QtUtil:
    @staticmethod
    def load_ui(*path):
        # 项目根目录
        project_root_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(project_root_path, "..", "pages", *path)
        return uic.loadUi(path)