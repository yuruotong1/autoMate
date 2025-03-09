class BaseAgent:
    def __init__(self, config, *args, **kwargs):
        self.config = config
        self.SYSTEM_PROMPT = ""

    
    def chat(self, messages):
        pass

