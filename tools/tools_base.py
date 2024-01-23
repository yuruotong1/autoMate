from utils.config import Config


class ToolsBase:
    def __init__(self):
        self.name = ""
        self.description = ""
        self.request_param = ""
        self.return_content = ""
        self.config = Config()
        
    def get_info(self):
        return {"name": self.name, "description": self.description, "param": self.request_param, "return_content": self.return_content}

    def run(self, param=None):
        pass
