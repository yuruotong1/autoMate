from pydantic import BaseModel, Field

from actions.action_base import ActionBase
from utils.selenium_util import SeleniumUtil


class OpenBrowserUrlInput(BaseModel):
    url: str = Field(description="要访问的网址", title="网址", default="")


class OpenBrowserUrlAction(ActionBase):
    name = "打开网页"
    description = "打开指定网址的页面"
    args: OpenBrowserUrlInput

    # 打开指定目录的应用
    def run(self, url):
        selenium = SeleniumUtil()
        selenium.get_url(url)

