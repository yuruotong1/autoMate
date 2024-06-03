import os
import sys

from PyQt6 import uic
from PyQt6.uic import loadUiType


class QtUtil:
    @classmethod
    def get_root_path(cls):
        # project_root_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        project_root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
        return project_root_path
        

    @classmethod
    def load_ui(cls, *path):
        # 项目根目录
        path = os.path.join(cls.get_root_path(), "pages", *path)
        return uic.loadUi(path)

    @classmethod
    def load_ui_type(cls, *path):
        path = os.path.join(cls.get_root_path(), "pages", *path)
        interface_ui, _ = loadUiType(path)
        return interface_ui

    @classmethod
    def get_icon(cls, *path):
        path = os.path.join(cls.get_root_path(), "source", *path)
        return path
