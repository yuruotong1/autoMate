from abc import ABC
from typing import Any

from langchain_core.tools import BaseTool

from utils.config import Config


class ToolBase(BaseTool, ABC):
    def get_info(self):
        return {"name": self.name, "description": self.description, "param": self.request_param, "return_content": self.return_content}


