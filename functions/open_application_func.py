import subprocess
from typing import Type

from pydantic import BaseModel, Field

from functions.function_base import FunctionBase


class OpenApplicationInput(BaseModel):
    path: str = Field(description="要查询的关键词", title="应用路径")


class OpenApplicationFunc(FunctionBase):
    name = "打开应用"
    description = "打开指定目录的应用"
    args_schema: Type[BaseModel] = OpenApplicationInput

    def run(self, path):
        subprocess.Popen(path)
