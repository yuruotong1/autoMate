import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.service import Service as ChromeService

from tools.tools_base import ToolsBase


class WebBrowserUrl(ToolsBase):
    def __init__(self):
        super().__init__()
        self.name = "web_browser"
        self.description = "利用selenium对指定URL进行访问"
        self.request_param = '字典，如{"usrl": ""}'
        self.return_content = ('{"driver": "selenium的webdriver，driver用于继续在此见面上进行操作，可作为web_element工具的入参", "content": '
                               '"网页xml结构"')

    def run(self, param=None):
        # Load browser configuration from YAML file
        driver = None
        # Check if webdriver is available
        if not os.path.exists("webdriver.exe"):
            # Download webdriver based on browser type
            browser_type = self.config.BROWSER.get("browser_type")
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
                return
        driver.implicitly_wait(10)
        driver.get(param["url"])
        driver.quit()
        return driver.page_source
