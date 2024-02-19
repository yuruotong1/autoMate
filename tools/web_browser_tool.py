from typing import Optional, Type

from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.callbacks import CallbackManagerForToolRun, AsyncCallbackManagerForToolRun
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from tools.tool_base import ToolBase
from utils.config import Config


class SearchInput(BaseModel):
    url: str = Field(description="要查询的网址")


class WebBrowserTool(ToolBase):
    name = "web_browser"
    description = "利用浏览器访问url，得到网页源码"
    args_schema: Type[BaseModel] = SearchInput

    def _run(self, url: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        """Use the tool."""
        config = Config()
        # Download webdriver based on browser type
        browser_type = config.BROWSER.get("browser_type")
        if browser_type == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")  # Enable headless mode
            webdriver_manager = ChromeDriverManager()
            driver = webdriver.Chrome(service=ChromeService(webdriver_manager.install()), options=options)
        elif browser_type == "edge":
            options = webdriver.EdgeOptions()
            options.add_argument("--headless")  # Enable headless mode
            webdriver_manager = EdgeChromiumDriverManager()
            driver = webdriver.Edge(service=EdgeService(webdriver_manager.install()), options=options)
        else:
            return ""
        driver.implicitly_wait(10)
        driver.get(url)
        s = driver.page_source
        driver.quit()
        # print(f"res {driver.page_source}")

        return s

    async def _arun(
            self, url: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")
