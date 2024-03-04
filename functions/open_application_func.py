import subprocess

from functions.function_base import FunctionBase


class OpenApplicationFunc(FunctionBase):
    name = "打开应用"
    description = "打开指定目录的应用"
    uni_tag = "open_application"

    # 打开指定目录的应用
    def run(self, path):
        subprocess.Popen(path)
