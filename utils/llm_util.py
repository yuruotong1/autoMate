
from utils.config import Config


class LLM_Util:
    def __init__(self):
        super().__init__()
        self.config = Config()
        self.api_key = self.config.get_config_from_component("openai", "api_key")
        self.base_url = self.config.get_config_from_component("openai", "api_url")
        self.open_ai_model = self.config.get_config_from_component("openai", "model")

    def llm(self):
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(temperature=0, model_name=self.open_ai_model, openai_api_key=self.api_key,
                          openai_api_base=self.base_url)
