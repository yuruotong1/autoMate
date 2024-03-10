from pages.bse_page import BasePage
from pages.edit_action_list_view import GlobalUtil
from pages.edit_function_page import FunctionListView
from utils.qt_util import QtUtil


class EditPage(BasePage):
    def setup_up(self):
        self.ui = QtUtil.load_ui("edit_page.ui")
        function_list_view = FunctionListView()
        self.ui.function_list_layout.addWidget(function_list_view)
        self.ui.ListViewLayout.addWidget(GlobalUtil.current_action)
        self.ui.run_button.clicked.connect(self.__run_button_click)
        self.ui.save_button.clicked.connect(self.__save_button_click)
        self.ui.cancel_button.clicked.connect(self.__cancel_button_click)
        # 设置间距
        self.ui.ListViewLayout.setStretch(0, 1)
        self.ui.ListViewLayout.setStretch(1, 2)
        self.ui.ListViewLayout.setStretch(2, 10)

    def __save_button_click(self):
        GlobalUtil.save_to_local()
        self.ui.hide()
        from pages.func_list_page import FuncListPage
        self.func = FuncListPage()
        self.func.show()

    def __cancel_button_click(self):
        GlobalUtil.delete_action_view(GlobalUtil.current_action)
        self.ui.hide()
        self.func = FunctionListView()
        self.func.show()

    @staticmethod
    def __run_button_click():
        GlobalUtil.current_action.model()
        for index in range(GlobalUtil.current_action.count()):
            func = GlobalUtil.current_action.item(index)
            r = func.__getattribute__("func").run_with_out_arg()
