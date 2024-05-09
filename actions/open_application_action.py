import subprocess

from pydantic import BaseModel, Field

from actions.action_base import ActionBase


class OpenApplicationInput(BaseModel):
    path: str = Field(description="要查询的关键词", title="应用路径", default="")


class OpenApplicationAction(ActionBase):
    name: str = "打开应用"
    description: str = "打开指定目录的应用"
    args: OpenApplicationInput

    def run(self, path):
        print("运行了这里", path)
        subprocess.Popen(path)
