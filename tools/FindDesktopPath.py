import os
from langchain.tools import BaseTool

class FindDesktopPath(BaseTool):
    name = "桌面路径"
    description = "返回桌面路径"

    # args_schema = None

    def _run(self):
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        return desktop_path