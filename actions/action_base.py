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
    __config_ui: ClassVar

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

    @classmethod
    # 设置配置界面的布局
    def config_page_ui(cls):
        cls.__config_ui = QtUtil.load_ui("config_page.ui")
        v_box_layout = QVBoxLayout()
        model_fields = cls.model_fields["args"].model_fields
        for field in model_fields:
            # 水平布局
            h_box_layout = QHBoxLayout()
            label = QLabel(cls.__config_ui)
            label.setText(model_fields[field].title)
            line_edit = QLineEdit(cls.__config_ui)
            h_box_layout.addWidget(label)
            h_box_layout.addWidget(line_edit)
            # 将输入内容填入参数列表
            cls.__ui_name_and_line_edit[field] = line_edit
            v_box_layout.addLayout(h_box_layout)
        save_button: QPushButton = cls.__config_ui.saveButton
        save_button.clicked.connect(cls.__save_button_clicked)

        cancel_button: QPushButton = cls.__config_ui.cancelButton
        cancel_button.clicked.connect(cls.__cancel_button_clicked)
        container_widget = QWidget(cls.__config_ui)
        container_widget.setLayout(v_box_layout)
        cls.__config_ui.config_list.addWidget(container_widget)

    @classmethod
    def __cancel_button_clicked(cls):
        cls.__config_ui.hide()

    @classmethod
    def __save_button_clicked(cls):
        from pages.edit_page import GlobalUtil
        for arg_name in cls.__ui_name_and_line_edit:
            cls.action_arg[arg_name] = cls.__ui_name_and_line_edit[arg_name].text()
        # 如果双击应用列表打开的配置页面，保存后向应用列表最后插入
        if cls.action_pos is None:
            cls.action_pos = GlobalUtil.current_page.action_list.count()
            cls.action_level = 0
        #  向新位置增加元素
        from pages.edit_action_list_view import ActionList
        ActionList.insert_item(GlobalUtil.current_page.action_list, cls.action_pos, cls)
        cls.__config_ui.hide()

    @classmethod
    def config_page_show(cls):
        cls.config_page_ui()
        if cls.__config_ui is None:
            raise TypeError("config_ui not config")
        # 居上对齐
        cls.__config_ui.config_list.layout().setAlignment(Qt.AlignmentFlag.AlignTop)
        cls.__config_ui.show()
