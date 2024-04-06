import os

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class ListAllFileInput(BaseModel):
    path: str = Field(description="目录路径", title="目录路径")


class ListAllFile(BaseTool):
    name = "list all file"
    description = "返回指定路径下的所有文件"
    args_schema = ListAllFileInput

    def _run(self, path):
        file_list = []
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                file_list.append(os.path.join(dirpath, filename))
        return file_list
