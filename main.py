import logging
import os
import sys
import traceback

import leancloud
from PyQt6.QtWidgets import QApplication
from actions import open_application_action

from pages.chat_page import ChatPage
from pages.edit_page import GlobalUtil, EditPage
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
                    self.page = FuncListPage()
        else:
            self.page = LoginPage()
            self.page.show()


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("catch exception:", tb)

# 加载全局数据
def load():
    
    # 生成 config.yaml 文件 
    Config()
    EditPage.global_load()




if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    sys.excepthook = excepthook
    app = QApplication(sys.argv)
    load()
    page = ChatPage()
    page.show()
    logging.error(sys.exit(app.exec()))
    
