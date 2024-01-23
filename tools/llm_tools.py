import openai
import yaml
from tools.tools_base import ToolsBase


class LLMTools(ToolsBase):
    def __init__(self):
        super().__init__()
        self.name = "llm_tools"
        self.description = "利用大模型进行回答"
        self.request_param='字典，如{"content": "天气怎么样"}'
        self.return_content = "大模型结果"
    
    def run(self, param=None):
        """
        Make a call to the OpenAI chat API.

        Args:
            param: The input text for the chat API.

        Returns:
            str: The generated text from the chat API.
        """
        openai.api_key = self.config.OPEN_AI.get("api_key")
        openai.base_url = self.config.OPEN_AI.get("api_url")
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
