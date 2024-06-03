from self_utils.config import Config
from self_utils.qt_util import QtUtil
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QLineEdit, QWidget, QGridLayout, QSpacerItem, QSizePolicy

interface_ui = QtUtil.load_ui_type("config_page.ui")
   

class ConfigPage(QMainWindow, interface_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.config = Config()
        self.tmp_config = self.config.config
        self.setup_up()
        self.save_button.clicked.connect(self.save_setting)
        self.cancel_button.clicked.connect(self.cancel_btn)
    
    def setup_up(self):
        for type_key, type_value  in self.tmp_config.items():
            widget = QWidget()
            widget.setObjectName(type_key)
            self.config_list.addTab(widget, type_key)
            all_settings = QVBoxLayout()
            widget.setLayout(all_settings)
            for sub_title, sub_value in type_value.items():
                '''
                components:
                    feishu:
                        description: 配置飞书相关信息，用于与飞书进行交互
                        config:
                            app_id: 请输入api_id
                            app_secret: 请输入app_secret
                '''
                 # feishu
                sub_title_label = QLabel(text=sub_title)
                # 配置飞书相关信息，用于与飞书进行交互
                sub_description_label = QLabel(text=sub_value["description"])
                grid_layout = QGridLayout()
                grid_layout.addWidget(sub_title_label, 0, 0)
                grid_layout.addWidget(sub_description_label, 1, 0)
                all_settings.addLayout(grid_layout)
                row = 2
                # app_id, 请输入api_id
                # app_secret, 请输入app_secret
                for config_key, config_value in sub_value["config"].items():
                    config_key_label = QLabel()
                    # app_id
                    config_key_label.setText(config_key)
                    line_edit = QLineEdit()
                    # 请输入api_id
                    line_edit.setText(config_value)
                    line_edit.textChanged.connect(lambda x, k=config_key, c=sub_value["config"]: self.text_changed(k, x, c))
                    grid_layout.addWidget(config_key_label, row, 0)
                    grid_layout.addWidget(line_edit, row, 1)
                    row += 1
                spacer = QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
                grid_layout.addItem(spacer, row, 0)
            
            spacer = QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
            all_settings.addItem(spacer)

    def text_changed(self, key, value, config):
        config[key] = value

    
    def save_setting(self):
        self.config.config = self.tmp_config
        self.config.update_config()
        self.close()

    def cancel_btn(self):
        self.hide()