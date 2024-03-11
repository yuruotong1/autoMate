import os

import yaml


class Config:
    def __init__(self):
        # 项目根目录
        project_root_path = os.path.abspath(os.path.dirname(__file__))
        # 上一层目录
        self.config = self._load_config(os.path.join(project_root_path, "..", "config.yaml"))
        self.OPEN_AI = self.config["openai"]
        self.BROWSER = self.config["browser"]
        self.DATA_POSITION = self.config["data_position"]
        self.LEAN_CLOUD = None
        if self.DATA_POSITION == "local":
            self.LEAN_CLOUD = self.config["leancloud"]

    @staticmethod
    # Load content from a yaml file and return as variables
    def _load_config(file_path):
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
        return config
