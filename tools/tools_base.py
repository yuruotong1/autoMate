class ToolsBase:
    def __init__(self):
        self.name = ""
        self.description = ""
        
    def get_info(self):
        return {"name": self.name, "description": self.description}

    def run(self, param=None):
        pass
