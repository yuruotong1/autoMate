import logging
import os
import sys
import traceback

import leancloud
from PyQt6.QtWidgets import QApplication

from pages.edit_action_list_view import ActionList
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


def load():
    edit_pages_json = GlobalUtil.load_data()
    for edit_page_json in edit_pages_json:
        edit_page = EditPage(
            func_status=edit_page_json["func_status"],
            func_list_pos_row=edit_page_json["func_list_pos_row"],
            func_list_pos_column=edit_page_json["func_list_pos_column"],
            action_list=ActionList.load(edit_page_json["action_list"]))
        edit_page.func_name = edit_page_json["func_name"]
        edit_page.func_description = edit_page_json["func_description"]
        GlobalUtil.edit_page_global.append(edit_page)


if __name__ == "__main__":
    sys.excepthook = excepthook
    app = QApplication(sys.argv)
    load()
    page = FuncListPage()
    page.show()
    sys.exit(app.exec())
