from utils.config import Config
from utils.qt_util import QtUtil
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget



interface_ui = QtUtil.load_ui_type("config_page.ui")
   

class ConfigPage(QMainWindow, interface_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup_up()
        self.save_button.clicked.connect(self.save_setting)
        self.cancel_button.clicked.connect(self.cancel_btn)
    
    def setup_up(self):
        self.config = Config()
        config_list_widget = self.config_list
        for type_key, type_value  in self.config.config.items():
            widget = QWidget()
            config_list_widget.addWidget(widget)
            for sub_title, sub_value in type_value.items():
                '''
                components:
                    feishu:
                        description: 配置飞书相关信息，用于与飞书进行交互
                        config:
                            app_id: 请输入api_id
                            app_secret: 请输入app_secret
                '''
                sub_title_label = QLabel()
                # feishu:配置飞书相关信息，用于与飞书进行交互
                sub_title_label.setText(sub_title + ":"+ sub_value["description"])
                v_box_layout = QVBoxLayout()
                widget.setLayout(v_box_layout)
                v_box_layout.addWidget(sub_title_label)
                # app_id, 请输入api_id
                # app_secret, 请输入app_secret
                for config_key, config_value in sub_value["config"].items():
                    h_box_layout = QHBoxLayout()
                    config_key_label = QLabel()
                    # app_id
                    config_key_label.setText(config_key)
                    line_edit = QLineEdit()
                    # 请输入api_id
                    line_edit.setText(config_value)
                    h_box_layout.addWidget(config_key_label)
                    h_box_layout.addWidget(line_edit)
                    v_box_layout.addLayout(h_box_layout)
                
            

    
    def save_setting(self):
        self.config.update_config()
        self.setting_page.close()

    def cancel_btn(self):
        self.setting_page.close()