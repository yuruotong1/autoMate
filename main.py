import logging
import sys
import traceback
from PyQt6.QtWidgets import QApplication
from pages.chat_page import ChatPage
from self_utils.config import Config


# 设置日志
logging.basicConfig(level=logging.INFO)


class AutoMate:
    def main(self):
        Config()
        self.page = ChatPage()
        self.page.show_window()
       


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("catch exception:", tb)

if __name__ == "__main__":
    try:
        sys.excepthook = excepthook
        app = QApplication(sys.argv)
        automate = AutoMate()
        automate.main()
        sys.exit(app.exec())
    except Exception as e:
        traceback.print_exc(e)
    
