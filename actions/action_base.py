from typing import Type, Any, ClassVar

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QWidget, QPushButton, QVBoxLayout
from langchain_core.tools import StructuredTool
from pydantic import BaseModel

from utils.qt_util import QtUtil


class ActionBase(BaseModel):
    name: ClassVar[str]
    description: ClassVar[str]
    args: Type[BaseModel]
    action_pos: int = -1
    action_level: int = -1
    config_ui: ClassVar = QtUtil.load_ui("config_page.ui")

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.__ui_name_and_line_edit = {}

    def run(self, *args, **kwargs):
        raise TypeError("Not realize run function")

    def run_with_out_arg(self):
        return self.run(**self.action_arg)

    def convert_langchain_tool(self):
        return StructuredTool.from_function(
            func=self.run,
            name=self.name,
            description=self.description,
            args_schema=self.args
        )

    # 设置配置界面的布局
    def config_page_ui(self, the_insert_row):
        v_box_layout = QVBoxLayout()
        model_fields = self.model_fields["args"].annotation.model_fields
        for field in model_fields:
            # 水平布局
            h_box_layout = QHBoxLayout()
            label = QLabel(self.config_ui)
            label.setText(model_fields[field].title)
            line_edit = QLineEdit(self.config_ui)
            h_box_layout.addWidget(label)
            h_box_layout.addWidget(line_edit)
            # 将输入内容填入参数列表
            self.__ui_name_and_line_edit[field] = line_edit
            v_box_layout.addLayout(h_box_layout)
        save_button: QPushButton = self.config_ui.saveButton
        save_button.clicked.__getattribute__("connect")(self.__save_button_clicked, the_insert_row)
        cancel_button: QPushButton = self.config_ui.cancelButton
        cancel_button.clicked.__getattribute__("connect")(self.__cancel_button_clicked
                                                          )
        container_widget = QWidget(self.config_ui)
        container_widget.setLayout(v_box_layout)
        self.config_ui.config_list.addWidget(container_widget)

    def __cancel_button_clicked(self):
        self.config_ui.hide()

    def __save_button_clicked(self, the_insert_row):
        args = {}
        from pages.edit_page import GlobalUtil
        for arg_name in self.__ui_name_and_line_edit:
            args[arg_name] = self.__ui_name_and_line_edit[arg_name].text()
        self.action_pos = the_insert_row
        self.action_level = 0
        #  向新位置增加元素
        from pages.edit_action_list_view import ActionList
        ActionList.insert_item(GlobalUtil.current_page.action_list, self.action_pos, self)
        self.config_ui.hide()

    def config_page_show(self, the_insert_row):
        self.config_page_ui(the_insert_row)
        if self.config_ui is None:
            raise TypeError("config_ui not config")
        # 居上对齐
        self.config_ui.config_list.layout().setAlignment(Qt.AlignmentFlag.AlignTop)
        self.config_ui.show()
