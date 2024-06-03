import os
import shutil

import yaml

from self_utils.qt_util import QtUtil


class Config:
    def __init__(self):
        # 项目根目录
        self.config_path = os.path.join(QtUtil.get_root_path(), "config.yaml")
        # 上一层目录
        self.config = self.load_config()
        
    def get_config_from_base(self, title, key):
        return self.config["base"][title]["config"][key]

    def get_config_from_component(self, title, key):
        return self.config["components"][title]["config"][key]

    def load_config(self):
        # 如果文件不存在，则生成一个yaml文件
        if not os.path.exists(self.config_path):
            # 将 config_tmp.yaml 复制并改名为 config.yaml
            shutil.copyfile(os.path.join(QtUtil.get_root_path(), "config_tmp.yaml"), self.config_path)

        with open(self.config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        return config

    def update_config(self):
        # 将 self.config 写入 yaml 文件，并允许 Unicode 字符
        with open(self.config_path, 'w', encoding='utf-8') as file:
            yaml.dump(self.config, file, allow_unicode=True, sort_keys=False)
