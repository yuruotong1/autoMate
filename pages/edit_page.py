from pages.edit_action_list_view import ActionList
from pages.edit_function_page import FunctionListView
from pages.global_util import GlobalUtil
from utils.qt_util import QtUtil
from PyQt6.QtWidgets import QMainWindow



interface_ui = QtUtil.load_ui_type("edit_page.ui")
   

class EditPage(QMainWindow, interface_ui):
    def __init__(self, parent_page, func_status, func_list_pos_row, func_list_pos_column, action_list: ActionList = None):
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
        self.parent_page = parent_page
        super().__init__()
        self.setupUi(self)
        self.setup_up()

    def closeEvent(self, event):
        self.parent_page.show()

    def dump(self):
        return {"func_list_pos_column": self.func_list_pos_column,
                "func_list_pos_row": self.func_list_pos_row,
                "func_name": self.func_name,
                "func_status": self.func_status,
                "func_description": self.func_description,
                "action_list": self.action_list.dump()
                }

    def setup_up(self):
        self.func_name_edit.setText(self.func_name)
        self.func_description_edit.setText(self.func_description)
        function_list_view = FunctionListView()
        self.function_list_layout.addWidget(function_list_view)
        self.action_list_view_layout.addWidget(self.action_list)
        self.run_button.clicked.connect(self.__run_button_click)
        self.save_button.clicked.connect(self.__save_button_click)
        self.cancel_button.clicked.connect(self.__cancel_button_click)
        # 设置间距
        self.action_list_view_layout.setStretch(0, 1)
        self.action_list_view_layout.setStretch(1, 2)
        self.action_list_view_layout.setStretch(2, 10)

    def __save_button_click(self):
        self.func_name = self.func_name_edit.text()
        self.func_description = self.func_description_edit.text()
        GlobalUtil.edit_page_global.append(self)
        GlobalUtil.save_to_local()
        self.close()


    def __cancel_button_click(self):
        # GlobalUtil.delete_edit_page(GlobalUtil.current_page)
        self.close()


    def __run_button_click(self):
        for index in range(self.action_list.count()):
            func = self.action_list.item(index)
            res = func.__getattribute__("get_action")().run_with_out_arg()
            print("执行结果：", res)



    @staticmethod
    def global_load( parent):
        # 根据配置文件的配置，从本地文件中或者网上读取
        edit_pages_json = GlobalUtil.read_from_local()
        for edit_page_json in edit_pages_json:
            from pages.edit_page import EditPage
            from pages.edit_action_list_view import ActionList
            edit_page = EditPage(
                func_status=edit_page_json["func_status"],
                func_list_pos_row=edit_page_json["func_list_pos_row"],
                func_list_pos_column=edit_page_json["func_list_pos_column"],
                # TODO待优化加载问题
                action_list=ActionList.load(edit_page_json["action_list"]),
                parent_page=parent
                )
            edit_page.func_name = edit_page_json["func_name"]
            edit_page.func_description = edit_page_json["func_description"]
            GlobalUtil.edit_page_global.append(edit_page)


    @staticmethod
    def get_edit_page_by_position(func_status, row, column):
        for i in GlobalUtil.edit_page_global:
            if i.func_list_pos_row == row and i.func_list_pos_column == column \
                    and i.func_status == func_status:
                return i
        return None