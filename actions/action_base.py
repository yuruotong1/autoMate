from typing import Type

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QWidget, QPushButton
from langchain_core.tools import StructuredTool
from pydantic import BaseModel

from pages.edit_action_list_view import GlobalUtil, ActionListViewItem
from utils.qt_util import QtUtil


class ActionBase:
    name = ""
    description = ""
    args_schema: Type[BaseModel]

    def __init__(self):
        self.__config_ui = None
        self.tool = None
        self.__ui_name_and_link_edit = {}
        self.action_arg = {}
        self.action_pos = None

    def run(self, *args, **kwargs):
        raise TypeError("Not realize run function")

    def run_with_out_arg(self):
        return self.run(**self.action_arg)

    def convert_langchain_tool(self):
        return StructuredTool.from_function(
            func=self.run,
            name=self.name,
            description=self.description,
            args_schema=self.args_schema
        )

    # 设置配置界面的布局
    def config_page_ui(self):
        self.__config_ui = QtUtil.load_ui("config_page.ui")
        # 水平布局
        h_box_layout = QHBoxLayout()
        label = QLabel(self.__config_ui)
        model_fields = self.args_schema.model_fields
        for field in model_fields:
            label.setText(model_fields[field].title)
            line_edit = QLineEdit(self.__config_ui)
            h_box_layout.addWidget(label)
            h_box_layout.addWidget(line_edit)
            self.__ui_name_and_link_edit[field] = line_edit
        save_button: QPushButton = self.__config_ui.saveButton
        save_button.clicked.connect(self.__save_button_clicked)

        cancel_button: QPushButton = self.__config_ui.cancelButton
        cancel_button.clicked.connect(self.__cancel_button_clicked)
        container_widget = QWidget(self.__config_ui)
        container_widget.setLayout(h_box_layout)
        self.__config_ui.config_list.addWidget(container_widget)

    def __cancel_button_clicked(self):
        self.__config_ui.hide()

    def __save_button_clicked(self):
        for arg_name in self.__ui_name_and_link_edit:
            self.action_arg[arg_name] = self.__ui_name_and_link_edit[arg_name].text()
        # 如果双击应用列表打开的配置页面，保存后向应用列表最后插入
        if self.action_pos is None:
            self.action_pos = GlobalUtil.current_action.count()

        GlobalUtil.current_action.insertItem(self.action_pos, ActionListViewItem(self))
        self.__config_ui.hide()

    def config_page_show(self):
        self.config_page_ui()
        if self.__config_ui is None:
            raise TypeError("config_ui not config")
        # 居上对齐
        self.__config_ui.config_list.layout().setAlignment(Qt.AlignmentFlag.AlignTop)
        self.__config_ui.show()
