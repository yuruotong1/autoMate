import os
import sys

from PyQt6 import uic


class QtUtil:
    @staticmethod
    def load_ui(*path):
        # 项目根目录
        # project_root_path = os.path.abspath(os.path.dirname(__file__))
        project_root_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        path = os.path.join(project_root_path, "pages", *path)
        return uic.loadUi(path)

    @staticmethod
    def get_icon(*path):
        project_root_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        # project_root_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(project_root_path, "source", *path)
        return path
