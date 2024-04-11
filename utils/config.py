import os
import platform
import yaml


class Config:
    APP_NAME = "autoMate"
    OPENAI_KEY = "openai_key"
    OPENAI_URL = "openai_url"
    OPENAI_MODEL = "openai_model"
    OPENAI = "openai"
    BROWSER = "browser"

    def __init__(self):
        # 全局配置文件根目录
        self.global_config_path = Config.get_app_settings_path()
        self.path = os.path.join(self.global_config_path, "config.yaml")
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
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
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

    @staticmethod
    def get_user_home():
        if platform.system() == "Windows":
            return os.environ["USERPROFILE"]
        else:
            return os.path.expanduser("~")

    @staticmethod
    def get_app_settings_path(app_name=APP_NAME):
        user_home = Config.get_user_home()
        if platform.system() == "Windows":
            return os.path.join(os.environ["APPDATA"], app_name)
        else:
            return os.path.join(user_home, ".config", app_name)
