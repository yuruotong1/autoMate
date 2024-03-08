import subprocess
from abc import ABC
from typing import Type

from PyQt6.QtWidgets import QHBoxLayout, QLineEdit, QLabel, QWidget
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing_extensions import Optional
from utils.qt_util import QtUtil


class OpenApplicationInput(BaseModel):
    path: str = Field(description="要查询的关键词", title="hello")


class OpenApplicationTool(BaseTool, ABC):
    name = "打开应用"
    description = "打开指定目录的应用"
    args_schema: Type[BaseModel] = OpenApplicationInput

    def __init__(self):
        super().__init__()

    # 打开指定目录的应用
    def _run(self, path, run_manager: Optional[CallbackManagerForToolRun] = None):
        subprocess.Popen(path)

    def config_page_ui(self):
        self.config_ui = QtUtil.load_ui("config_page.ui")
        # 水平布局
        h_box_layout = QHBoxLayout()
        label = QLabel(self.config_ui)
        label.setText("路径")
        line_edit = QLineEdit(self.config_ui)
        h_box_layout.addWidget(label)
        h_box_layout.addWidget(line_edit)
        container_widget = QWidget(self.config_ui)
        container_widget.setLayout(h_box_layout)
        self.config_ui.config_list.addWidget(container_widget)
