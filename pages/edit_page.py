import json
import os
import pickle
from dataclasses import dataclass, asdict

from pages.bse_page import BasePage
from pages.edit_action_list_view import ActionList
from pages.edit_function_page import FunctionListView
from utils.qt_util import QtUtil


class EditPage(BasePage):
    @dataclass
    class EditPageData:
        func_list_pos_column: int
        func_list_pos_row: int
        func_name: str
        func_status: str
        func_description: str
        action_list: ActionList.ActionListData

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
        return self.EditPageData(func_list_pos_column=self.func_list_pos_column,
                                 func_list_pos_row=self.func_list_pos_row,
                                 func_name=self.func_name,
                                 func_status=self.func_status,
                                 func_description=self.func_description,
                                 action_list=self.action_list.dump()
                                 )

    @classmethod
    def load(cls, edit_page_data):
        edit_page = EditPage(
            func_status=edit_page_data.func_status,
            func_list_pos_row=edit_page_data.func_list_pos_row,
            func_list_pos_column=edit_page_data.func_list_pos_column,
            action_list=ActionList.load(edit_page_data.action_list))
        edit_page.func_name = edit_page_data.func_name
        edit_page.func_description = edit_page_data.func_description
        return edit_page

    def setup_up(self):
        self.ui = QtUtil.load_ui("edit_page.ui")
        self.ui.func_name_edit.setText(self.func_name)
        self.ui.func_description_edit.setText(self.func_description)
        function_list_view = FunctionListView()
        self.ui.function_list_layout.addWidget(function_list_view)
        self.ui.ListViewLayout.addWidget(self.action_list)
        self.ui.run_button.clicked.connect(self.__run_button_click)
        self.ui.save_button.clicked.connect(self.__save_button_click)
        self.ui.cancel_button.clicked.connect(self.__cancel_button_click)
        # 设置间距
        self.ui.ListViewLayout.setStretch(0, 1)
        self.ui.ListViewLayout.setStretch(1, 2)
        self.ui.ListViewLayout.setStretch(2, 10)

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
            func.__getattribute__("func").run_with_out_arg()


class GlobalUtil:
    edit_page_global: list[EditPage] = []
    current_page: EditPage = None

    @classmethod
    def get_edit_page_by_position(cls, func_status, row, column):
        for i in cls.edit_page_global:
            if i.func_list_pos_row == row and i.func_list_pos_column == column \
                    and i.func_status == func_status:
                return i
        return None

    @classmethod
    def delete_edit_page(cls, edit_page):
        cls.edit_page_global.remove(edit_page)

    @classmethod
    def read_from_local(cls):
        # 判断文件是否存在
        if not os.path.exists("./cache"):
            return []

        with open("./cache", "rb") as file:
            data = pickle.load(file).get("action_list_global")
            if not data:
                data = []
            return data

    @classmethod
    def save_to_local(cls):
        with open("./cache", "wb") as file:
            edit_page_dump = [asdict(i.dump()) for i in cls.edit_page_global]
            pickle.dump({"action_list_global": edit_page_dump}, file)

    @classmethod
    def init(cls):
        # 根据配置文件的配置，从本地文件中或者网上读取
        from utils.config import Config
        config = Config()
        cls.edit_page_global = []
        if config.DATA_POSITION == "local":
            edit_pages_json = cls.read_from_local()
        elif config.DATA_POSITION == "remote":
            edit_pages_json = []
        else:
            edit_pages_json = []
        for edit_page_json in edit_pages_json:
            edit_pages_data = EditPage.EditPageData(**edit_page_json)
            cls.edit_page_global.append(EditPage.load(edit_pages_data))
