from typing import Type

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QWidget
from langchain_core.tools import StructuredTool
from pydantic import BaseModel

from functions.open_application_tool import OpenApplicationInput
from utils.qt_util import QtUtil


class FunctionBase:
    name = ""
    description = ""
    args_schema: Type[BaseModel]

    def __init__(self):
        self.config_ui = None
        self.tool = None

    def run(self, *args, **kwargs):
        raise TypeError("Not realize run function")

    def convert_langchain_tool(self):
        return StructuredTool.from_function(
            func=self.run,
            name=self.name,
            description=self.description,
            args_schema=self.args_schema
        )

    # 设置配置界面的布局
    def config_page_ui(self):
        self.config_ui = QtUtil.load_ui("config_page.ui")
        # 水平布局
        h_box_layout = QHBoxLayout()
        label = QLabel(self.config_ui)
        model_fields = self.args_schema.model_fields
        for field in model_fields:
            label.setText(model_fields[field].title)
            line_edit = QLineEdit(self.config_ui)
            h_box_layout.addWidget(label)
            h_box_layout.addWidget(line_edit)
            container_widget = QWidget(self.config_ui)
            container_widget.setLayout(h_box_layout)
            self.config_ui.config_list.addWidget(container_widget)

    def config_page_show(self):
        self.config_page_ui()
        if self.config_ui is None:
            raise TypeError("config_ui not config")
        # 居上对齐
        self.config_ui.config_list.layout().setAlignment(Qt.AlignmentFlag.AlignTop)
        self.config_ui.show()
