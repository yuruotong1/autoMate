import subprocess

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class OpenApplicationInput(BaseModel):
    path: str = Field(description="应用路径", title="应用路径")


class OpenApplicationAction(BaseTool):
    name = "open_application"
    description = "打开指定目录的应用"
    args_schema = OpenApplicationInput

    def _run(self, path):
        subprocess.Popen(path)
