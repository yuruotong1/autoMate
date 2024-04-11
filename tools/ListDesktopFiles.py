import os

from langchain_core.tools import BaseTool

from tools.FindDesktopPath import FindDesktopPath
from tools.ListAllFile import ListAllFile


class ListDesktopFiles(BaseTool):
    name = "桌面的所有文件"
    description = "返回桌面的所有文件"

    def _run(self, *tool_args, **tool_kwargs):
        desk_top_path = FindDesktopPath().invoke(input={})
        all_files = ListAllFile().invoke(input={"path": desk_top_path})
        return all_files
