from typing import Type, Any, ClassVar

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QWidget, QPushButton, QVBoxLayout
from langchain_core.tools import StructuredTool
from pydantic import BaseModel
from utils.global_util import GlobalUtil

from utils.qt_util import QtUtil


class ActionBase(BaseModel):
    name: ClassVar[str]
    description: ClassVar[str]
    args: Type[BaseModel]
    output_save_name: ClassVar[str]
    action_pos: int = -1
    action_level: int = -1

    def __init__(self, **data: Any):
        super().__init__(**data)
        self._ui_name_and_line_edit = {}
        self._output_edit = None
        self._config_ui = QtUtil.load_ui("action_config_page.ui")
        self.save_out_put_ui()
        self.config_page_ui()


    def run(self, *args, **kwargs):
        raise TypeError("Not realize run function")

    def run_with_out_arg(self):
        res = self.run(**self.args.model_dump())
        # 保存输出结果
        if self.output_save_name:
            GlobalUtil.current_page.output_save_dict[self._output_edit.text()] = res
        return res

    # 设置配置界面的布局
    def config_page_ui(self):
        model_fields = self.model_fields["args"].annotation.model_fields
        # 配置输入
        for field in model_fields:
            h_box_layout = QHBoxLayout()
            label = QLabel(self._config_ui)
            label.setText(model_fields[field].title)
            line_edit = QLineEdit(self._config_ui)
            h_box_layout.addWidget(label)
            h_box_layout.addWidget(line_edit)
            self._config_ui.config_list.addLayout(h_box_layout)
            self._ui_name_and_line_edit[field] = line_edit
        


    def save_out_put_ui(self):
        # 判断是否需要保存输出
        if hasattr(self, "output_save_name"):
            output_label = QLabel(self._config_ui)
            output_label.setText("保存结果至")
            
            output_line_edit = QLineEdit("output_save_name")
            self._output_edit = output_line_edit
            # output_line_edit.setObjectName("output_save_name")
            output_save_dict = GlobalUtil.current_page.output_save_dict
            output_save_name = self.output_save_name
            # 为输出结果自动取名
            i = 1
            while True:
                if output_save_name in output_save_dict:
                    output_save_name = self.output_save_name + "_" + str(i)
                    i += 1
                    continue
                else:
                    output_line_edit.setText(output_save_name)
                    break
            self._config_ui.output_config.addWidget(output_label)
            self._config_ui.output_config.addWidget(output_line_edit)
        else:
            self._config_ui.output_config.addWidget(QLabel("当前行为不包含输出项"))

    def __cancel_button_clicked(self):
        self._config_ui.hide()

    def __save_button_clicked(self, the_insert_row):
        from pages.edit_page import GlobalUtil
        arg = {}
        for arg_name in self._ui_name_and_line_edit:
            arg[arg_name] = self._ui_name_and_line_edit[arg_name].text()
        self.args= self.args.model_validate(arg)
        self.action_pos = the_insert_row
        self.action_level = 0
        # 如果设置了output_save_name
        if hasattr(self, "output_save_name"):
            output_save_name = self._output_edit.text()
            GlobalUtil.current_page.output_save_dict[output_save_name] = ""
        #  向新位置增加元素
        from pages.edit_action_list_view import ActionList
        from pages.edit_action_list_view import ActionListItem
        action_item = ActionListItem(self)
        ActionList.insert_item(GlobalUtil.current_page.action_list, self.action_pos, action_item)
        self._config_ui.hide()

    def config_page_show(self, the_insert_row):
        save_button: QPushButton = self._config_ui.saveButton
        save_button.clicked.__getattribute__("connect")(lambda: self.__save_button_clicked(the_insert_row))
        cancel_button: QPushButton = self._config_ui.cancelButton
        cancel_button.clicked.__getattribute__("connect")(self.__cancel_button_clicked)
        if self._config_ui is None:
            raise TypeError("config_ui not config")
        # 居上对齐
        self._config_ui.config_list.layout().setAlignment(Qt.AlignmentFlag.AlignTop)
        self._config_ui.show()
