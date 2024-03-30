from pages.bse_page import BasePage
from pages.edit_action_list_view import ActionList
from pages.edit_function_page import FunctionListView
from pages.global_util import GlobalUtil
from utils.qt_util import QtUtil


class EditPage(BasePage):
    def __init__(self, func_status, func_list_pos_row, func_list_pos_column, action_list: ActionList = None):
        self.func_list_pos_column = func_list_pos_column
        self.func_list_pos_row = func_list_pos_row
        # 属于通用还是专属
        self.func_status = func_status
        self.func_description = ""
        # 在func上的名称
        self.func_name = "默认名称"
        if not action_list:
            action_list = ActionList()
        self.action_list = action_list
        super().__init__()

    def dump(self):
        return {"func_list_pos_column": self.func_list_pos_column,
                "func_list_pos_row": self.func_list_pos_row,
                "func_name": self.func_name,
                "func_status": self.func_status,
                "func_description": self.func_description,
                "action_list": self.action_list.dump()
                }

    def setup_up(self):
        self.ui = QtUtil.load_ui("edit_page.ui")
        self.ui.func_name_edit.setText(self.func_name)
        self.ui.func_description_edit.setText(self.func_description)
        function_list_view = FunctionListView()
        self.ui.function_list_layout.addWidget(function_list_view)
        self.ui.action_list_view_layout.addWidget(self.action_list)
        self.ui.run_button.clicked.connect(self.__run_button_click)
        self.ui.save_button.clicked.connect(self.__save_button_click)
        self.ui.cancel_button.clicked.connect(self.__cancel_button_click)
        # 设置间距
        self.ui.action_list_view_layout.setStretch(0, 1)
        self.ui.action_list_view_layout.setStretch(1, 2)
        self.ui.action_list_view_layout.setStretch(2, 10)

    def __save_button_click(self):
        self.func_name = self.ui.func_name_edit.text()
        self.func_description = self.ui.func_description_edit.text()
        GlobalUtil.save_to_local()
        self.ui.hide()
        from pages.func_list_page import FuncListPage
        self.func = FuncListPage()
        self.func.show()

    def __cancel_button_click(self):
        GlobalUtil.delete_edit_page(GlobalUtil.current_page)
        self.ui.hide()
        from pages.func_list_page import FuncListPage
        self.func = FuncListPage()
        self.func.show()

    def __run_button_click(self):
        for index in range(self.action_list.count()):
            func = self.action_list.item(index)
            res = func.__getattribute__("get_action")().run_with_out_arg()
            print("执行结果：", res)
