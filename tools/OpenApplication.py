import subprocess
from langchain.tools import BaseTool  # Added ToolException impor
from pydantic import BaseModel, Field
from langchain_core.tools import ToolException

class OpenApplicationInput(BaseModel):
    path: str = Field(description="应用路径", title="应用路径")

class OpenApplicationAction(BaseTool):
    name = "打开应用"
    description = "打开指定目录的应用"
    args_schema = OpenApplicationInput

    def _run(self, path):
        try:
            subprocess.Popen(path)
        except Exception as e:
            raise ToolException(f"请好好检查一下路径，是不是有不合理的字符，比如`\nObservation: `、`非路径内容`")  # Using ToolException here
