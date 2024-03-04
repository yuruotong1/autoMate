import subprocess

from functions.function_base import FunctionBase


class OpenBrowserUrlFunc(FunctionBase):
    name = "打开网页"
    description = "打开指定网址的页面"
    uni_tag = "open_web_url"

    # 打开指定目录的应用
    def run(self, path):
        subprocess.Popen(path)
