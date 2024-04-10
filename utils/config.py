import os

import yaml


class Config:
    OPENAI_KEY = "openai_key"
    OPENAI_URL = "openai_url"
    OPENAI_MODEL = "openai_model"
    OPENAI = "openai"
    BROWSER = "browser"

    def __init__(self):
        # 项目根目录
        project_root_path = os.path.abspath(os.path.dirname(__file__))
        self.path = os.path.join(project_root_path, "..", "config.yaml")
        # 上一层目录
        self.config = self._load_config(self.path)
        self.OPEN_AI = self.config[self.OPENAI]
        self.BROWSER_CONFIG = self.config[self.BROWSER]
        self.DATA_POSITION = self.config["data_position"]
        self.LEAN_CLOUD = None
        if self.DATA_POSITION == "remote":
            self.LEAN_CLOUD = self.config["leancloud"]

    @staticmethod
    # Load content from a yaml file and return as variables
    def _load_config(file_path):
        # 如果文件不存在，则生成一个yaml文件
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                data = {Config.OPENAI: {Config.OPENAI_KEY: "your_api_key",
                                        Config.OPENAI_URL: "https://api.openai.com/v1/",
                                        Config.OPENAI_MODEL: "gpt-4-1106-preview"},
                        "data_position": "local",
                        Config.BROWSER: "edge"}
                yaml.dump(data, file)

        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
        return config

    def update_config(self, loc, key, value):
        self.config[loc][key] = value
        with open(self.path, 'w') as file:
            yaml.dump(self.config, file)
