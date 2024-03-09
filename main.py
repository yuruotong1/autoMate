import logging
import os
import sys

import leancloud
from PyQt6.QtWidgets import QApplication

from pages.edit_action_list_view import GlobalUtil
from pages.edit_page import EditPage
from pages.func_list_page import FuncListPage
from pages.login_page import LoginPage
from utils.config import Config

# 设置日志
logging.basicConfig(level=logging.INFO)

class AutoMate:
    def __init__(self):
        self.page = None

    def run_ui(self):
        config = Config()
        leancloud.init(config.LEAN_CLOUD["id"], config.LEAN_CLOUD["key"])
        # 从文件中判断是否有session
        tmp_file = "./session"
        if os.path.exists(tmp_file):
            with open(tmp_file, 'rb') as file:
                session_token = file.read()
                leancloud.User.become(session_token)
                authenticated = leancloud.User.get_current().is_authenticated()
                if not authenticated:
                    self.page = LoginPage()
                    self.page.show()
                else:
                    self.page = EditPage()
        else:
            self.page = LoginPage()
            self.page.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    GlobalUtil.init()
    page = FuncListPage()
    page.show()
    sys.exit(app.exec())
