import subprocess
from pydantic import BaseModel, Field

from data_class.search_data import SearchData
from functions.function_base import FunctionBase
from utils.selenium_util import SeleniumUtil


class OpenBrowserUrlInput(BaseModel):
    url: str = Field(description="要访问的网址", title="网址")


class OpenBrowserUrlFunc(FunctionBase):
    name = "打开网页"
    description = "打开指定网址的页面"
    args_schema = OpenBrowserUrlInput

    # 打开指定目录的应用
    def run(self, url):
        selenium = SeleniumUtil()
        selenium.get_url(url)

