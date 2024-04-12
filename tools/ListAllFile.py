import os
from pydantic import BaseModel, Field
from langchain.tools import BaseTool


class ListAllFileInput(BaseModel):
    path: str = Field(description="路径", title="路径")


class ListAllFile(BaseTool):
    name = "返回路径下的所有文件"
    description = "返回指定路径下的所有文件"
    args_schema = ListAllFileInput

    def _run(self, path):
        # 如果路径不存在则报错
        if not os.path.exists(path):
            raise ValueError(f"路径 {path} 不存在")
        file_list = []
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                file_list.append(os.path.join(dirpath, filename))
        print(file_list)
        return file_list
