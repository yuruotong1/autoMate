import subprocess
from langchain.tools import BaseTool, ToolException  # Updated import statement
from pydantic import BaseModel, Field


class OpenApplicationInput(BaseModel):
    path: str = Field(description="应用路径", title="应用路径")


class OpenApplicationAction(BaseTool):
    name = "打开应用"
    description = "打开指定目录的应用"
    args_schema = OpenApplicationInput

    def _run(self, path):
        subprocess.Popen(path)
