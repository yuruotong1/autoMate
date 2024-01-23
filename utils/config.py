import yaml


class Config:
    def __init__(self):
        self.config = self._load_config('../config.yaml')
        self.OPEN_AI = self.config["openai"]
        self.BROWSER = self.config["browser"]

    # Load content from a yaml file and return as variables
    def _load_config(self, file_path):
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
        return config
