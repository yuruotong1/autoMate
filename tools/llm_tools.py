import openai
import yaml
from tools.tools_base import ToolsBase


class LLMTools(ToolsBase):
    def __init__(self):
        self.name = "llm_tools"
        self.description = "利用大模型进行回答，入参格式为字典：{role:大模型的角色, content:问题}"
    
    def run(self, param=None):
        """
        Make a call to the OpenAI chat API.

        Args:
            param: The input text for the chat API.

        Returns:
            str: The generated text from the chat API.
        """
        with open("config.yaml", "r") as file:
            config = yaml.safe_load(file).get("openai")

        openai.api_key = config.get("api_key")
        openai.base_url = config.get("api_url")
        messages = []
        if "role" in param:
            messages.append({"role": "system", "content": param["role"]})
        messages.append({"role": "user", "content": param["content"]})

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # GPT-3.5 model
            messages=messages,
            temperature=0.2
        )

        generated_text = response.choices[0].message.content

        return generated_text
