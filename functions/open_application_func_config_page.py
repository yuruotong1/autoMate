from pages.bse_page import BasePage
from utils.qt_util import QtUtil


class NewFuncPage(BasePage):
    def setup_up(self):
        self.ui = QtUtil.load_ui("config_page.ui")

