import subprocess

from pydantic import BaseModel, Field

from actions.action_base import ActionBase


class OpenApplicationInput(BaseModel):
    path: str = Field(description="要查询的关键词", title="应用路径", default="")


class OpenApplicationAction(ActionBase):
    name = "打开应用"
    description = "打开指定目录的应用"
    args: OpenApplicationInput

    def run(self, path):
        subprocess.Popen(path)


if __name__ == '__main__':
    action = OpenApplicationAction(args={})
    action.args.path = "ccc"
    print(action)
