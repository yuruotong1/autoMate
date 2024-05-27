from typing import Type, Any
from PyQt6.QtCore import Qt, pyqtSignal, QObject
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton
from pydantic import BaseModel
from utils.qt_util import QtUtil
from PyQt6.QtCore import QThread

class ActionSignal(QObject):
    finish_run_signal = pyqtSignal(object)
    start_run_signal = pyqtSignal()    

    def finish_run_signal_emit(self, res):
        self.finish_run_signal.emit(res)

    def start_run_signal_emit(self):
        self.start_run_signal.emit()

class RunActionThread(QThread):
    def __init__(self, action):
        super().__init__()
        self.action = action

    def run(self):
        res = self.action.run_with_out_arg()
        self.action.get_signal().finish_run_signal_emit(res)

class ActionBase(BaseModel):
    name: str = ""
    description: str = ""
    args: Type[BaseModel]
   
    def __init__(self, **data: Any):
        super().__init__(**data)
        self._ui_name_and_line_edit = {}
        self._config_ui = QtUtil.load_ui("action_config_page.ui")
        self._action_signal = ActionSignal()

    def get_signal(self):
        return self._action_signal
    

    def run(self, *args, **kwargs):
        raise TypeError("Not realize run function")

    def run_with_out_arg(self):
        print("运行中...")
        res = self.run(**self.args.model_dump())
        # # 保存输出结果
        # if self.output_save_name:
        #     GlobalUtil.current_page.output_save_dict[self.uuid][self.output_save_name] = res
        #     GlobalUtil.current_page.update_runing_terminal()
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
        

    def __cancel_button_clicked(self):
        self._config_ui.hide()

    def _save_button_clicked(self):
        arg = {}
        for arg_name in self._ui_name_and_line_edit:
            arg[arg_name] = self._ui_name_and_line_edit[arg_name].text()
        self.args = self.args.model_validate(arg)
        thread = RunActionThread(self)
        thread.start()
        self._action_signal.start_run_signal_emit()
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
        self.config_page_ui()
        # 如果已经加载过，就直接显示
        self._config_ui.show()
