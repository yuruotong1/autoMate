from typing import Type, Any, ClassVar
import uuid

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton
from pydantic import BaseModel
from utils.global_util import GlobalUtil
from utils.qt_util import QtUtil


class ActionBase(BaseModel):
    name: ClassVar[str]
    description: ClassVar[str]
    args: Type[BaseModel]
    output_save_name: str = ""
    action_pos: int = -1
    action_level: int = -1
    uuid: str = ""
    
    def __init__(self, output_save_name_from_drag: str = None, **data: Any):
        super().__init__(**data)
        # 为每个实例生成唯一的 UUID
        if self.uuid == "":
            self.uuid = str(uuid.uuid4())  
        self._ui_name_and_line_edit = {}
        self._output_edit = None
        self._config_ui = QtUtil.load_ui("action_config_page.ui")
        self._parent = None
        self._is_config_page_init = False
        # 如果拖动过 action，则使用传进来的 output_save_name
        self._output_save_name_from_drag = output_save_name_from_drag
        self._data = {}

    def set_data(self, key, value):
        self._data[key] = value
    
    def get_data(self, key):
        return self._data.get(key, None)

    def set_output_save_name_from_drag(self, output_save_name_from_drag: str):
        self._output_save_name_from_drag = output_save_name_from_drag

    def set_parent(self, parent):
        self._parent = parent
    
    def get_parent(self):
        return self._parent

    def run(self, *args, **kwargs):
        raise TypeError("Not realize run function")

    def run_with_out_arg(self):
        res = self.run(**self.args.model_dump())
        # 保存输出结果
        if self.output_save_name:
            self._get_edit_page().output_save_dict[self.uuid][self._output_edit.text()] = res
        return res

    # 设置配置界面的布局
    def config_page_ui(self):
        model_fields = self.model_fields["args"].annotation.model_fields
        # 配置输入
        for field in model_fields:
            # 如果是 after_config 类型，则需要在editPage页面手动配置后填充值
            if hasattr(model_fields[field], "json_schema_extra") and model_fields[field].json_schema_extra and model_fields[field].json_schema_extra.get("_type") == "after_config":
                continue
            h_box_layout = QHBoxLayout()
            label = QLabel(self._config_ui)
            label.setText(model_fields[field].title)
            line_edit = QLineEdit(self._config_ui)
            line_edit.setText(str(self.args.model_dump().get(field, "")))
            h_box_layout.addWidget(label)
            h_box_layout.addWidget(line_edit)
            self._config_ui.config_list.addLayout(h_box_layout)
            self._ui_name_and_line_edit[field] = line_edit
        


    def save_out_put_ui(self):
        # 判断是否需要保存输出
        if self.output_save_name != "":
            output_label = QLabel(self._config_ui)
            output_label.setText("保存结果至")
            output_line_edit = QLineEdit("output_save_name")
            self._output_edit = output_line_edit
            # 使用外部传进来的 output_save_name
            if self._output_save_name_from_drag:
                self.output_save_name = self._output_save_name_from_drag
                # 设置编辑框的默认名称
                output_line_edit.setText(self.output_save_name)
            else:
                output_save_name = self.output_save_name
                # 为输出结果自动取名
                i = 1
                 # 获取 editPage 页面的 output_save_dict
                output_save_dict = self._get_edit_page().output_save_dict
                # 找到一个不存在的名称
                while True:
                    if output_save_name in [list(i.keys())[0] for i in output_save_dict.values()]:
                        output_save_name = self.output_save_name + "_" + str(i)
                        i += 1
                        continue
                    else:
                        self.output_save_name = output_save_name
                        # 设置编辑框的默认名称
                        output_line_edit.setText(output_save_name)
                        break
            self._config_ui.output_config.addWidget(output_label)
            self._config_ui.output_config.addWidget(output_line_edit)
        else:
            self._config_ui.output_config.addWidget(QLabel("当前行为不包含输出项"))

    def __cancel_button_clicked(self):
        self._config_ui.hide()

    def _get_edit_page(self):
        parent = self.get_parent()
        from pages.edit_page import EditPage
        while not isinstance(parent, EditPage):
            parent = parent.get_parent()
        return parent

    def get_action_list(self):
        return self.get_parent().get_parent()
    
    def get_action_list_item(self):
        return self.get_parent()

    def _save_button_clicked(self):
        arg = {}
        for arg_name in self._ui_name_and_line_edit:
            arg[arg_name] = self._ui_name_and_line_edit[arg_name].text()
        self.args = self.args.model_validate(arg)
        self.action_level = 0
        # 如果设置了output_save_name，向全局中插入该变量
        if self.output_save_name != "":
            self.output_save_name = self._output_edit.text()
            self._get_edit_page().output_save_dict[self.uuid] = {}
            self._get_edit_page().output_save_dict[self.uuid][self.output_save_name] = ""
            self._get_edit_page().update_send_to_ai_selection()
        # 插入新的 action
        if self.get_action_list_item() not in self.get_action_list().action_list_items:
            from pages.edit_action_list_view import ActionList
            ActionList.insert_item(self.get_action_list(), self.action_pos, self.get_action_list_item())
        
        self._config_ui.hide()
            

    def config_page_show(self):
        save_button: QPushButton = self._config_ui.saveButton
        save_button.clicked.__getattribute__("connect")(self._save_button_clicked)
        cancel_button: QPushButton = self._config_ui.cancelButton
        cancel_button.clicked.__getattribute__("connect")(self.__cancel_button_clicked)
        if self._config_ui is None:
            raise TypeError("config_ui not config")
        # 居上对齐
        self._config_ui.config_list.layout().setAlignment(Qt.AlignmentFlag.AlignTop)
        # 如果配置页面未加载过，就进行加载
        if not self._is_config_page_init:
            self.save_out_put_ui()
            self.config_page_ui()
        # 如果已经加载过，就直接显示
        self._is_config_page_init = True
        self._config_ui.show()
