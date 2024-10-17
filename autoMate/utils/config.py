import os
import yaml


class Config:
    def __init__(self):
        self.user_home_path = os.path.expanduser("~")  # 获取用户主目录路径
        self.config_path = os.path.join(self.user_home_path, ".xbrain.yaml")  # 使用用户目录下的配置文件
        self.config = self.load_config()
        self.OPENAI_BASE_URL = self.config["openai"]["base_url"]
        self.OPENAI_API_KEY = self.config["openai"]["api_key"]
        self.OPENAI_MODEL = self.config["openai"]["model"]


    def load_config(self):
        
        if not os.path.exists(self.config_path):
            # 如果文件不存在，创建文件并写入默认配置
            default_config = {
                'openai': {
                    'base_url': 'https://api.openai.com/v1',
                    'api_key': '',
                    'model': 'gpt-4o-2024-08-06'
                }
            }
            with open(self.config_path, 'w') as f:
                yaml.dump(default_config, f, default_flow_style=False)
            return default_config
        else:
            # 如果文件存在，正常加载配置
            with open(self.config_path, "r") as f:
                return yaml.load(f, Loader=yaml.FullLoader)