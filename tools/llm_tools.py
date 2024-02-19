from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI

from tools.tool_base import ToolBase


class LLMTools(ToolBase):
    def __init__(self):
        super().__init__()
        self.name = "llm_tools"
        self.description = "利用大模型进行回答"
        self.request_param = '字典，如{"content": "天气怎么样"}'
        self.return_content = "大模型结果"
        self.api_key = self.config.OPEN_AI.get("api_key")
        self.base_url = self.config.OPEN_AI.get("api_url")

    def run(self, param=None):
        chat = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo", openai_api_key=self.api_key,
                          openai_api_base=self.base_url)
        return chat([SystemMessage("你是一个点菜机器人"),
                     HumanMessage("我想要一份牛排")]).content
