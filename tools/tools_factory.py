from tools.llm_tools import LLMTools
from tools.web_browser_element_tools import WebBrowserElement
from tools.web_browser_url_tools import WebBrowserUrl


class ToolsFactory:
    def __init__(self):
        self.tools = [
            WebBrowserElement(),
            WebBrowserUrl(),
            LLMTools()
        ]

    def get_tools(self):
        for tool in self.tools:
            yield tool.get_info()
