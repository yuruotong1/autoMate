from utils.config import Config


class LLMUtil:
    def __init__(self):
        super().__init__()
        self.config = Config()
        self.api_key = self.config.OPEN_AI.get("api_key")
        self.base_url = self.config.OPEN_AI.get("api_url")
        self.model_name = self.config.OPEN_AI.get("model_name", "gpt-3.5-turbo")

    def llm(self):
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(temperature=0, model_name=self.model_name, openai_api_key=self.api_key,
                          openai_api_base=self.base_url)
