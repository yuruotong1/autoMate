
from utils.config import Config
from litellm import completion
from agent.prompt import tools

class LLM_Util:

    def __init__(self):
        super().__init__()
        self.config = Config()
        self.api_key = self.config.get_config_from_component("llm", "api_key")
        self.base_url = self.config.get_config_from_component("llm", "api_url")
        self.model = self.config.get_config_from_component("llm", "model")

    # messages = [{ "content": message, "role": "user"}]
    def invoke(self, messages):
        response = completion(model=self.model, base_url=self.base_url, api_key=self.api_key,
                               messages=messages, tools=tools, tool_choice={"type": "function", "function": {"name": "execute"}})

        return response.json()["choices"][0]["message"]