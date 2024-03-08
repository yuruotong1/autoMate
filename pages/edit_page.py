from pages.bse_page import BasePage
from pages.edit_function_page import FunctionListView
from pages.action_list_view import GlobalUtil
from utils.qt_util import QtUtil


class EditPage(BasePage):
    def setup_up(self):
        self.ui = QtUtil.load_ui("edit_page.ui")
        function_list_view = FunctionListView()
        self.ui.function_list_layout.addWidget(function_list_view)
        self.ui.ListViewLayout.addWidget(GlobalUtil.action_list_global)
        # 设置间距
        self.ui.ListViewLayout.setStretch(0, 1)
        self.ui.ListViewLayout.setStretch(1, 2)
        self.ui.ListViewLayout.setStretch(2, 10)
        self.ui.show()

    def __run_button_click(self, function_list_view):
        function_list_view.model()
