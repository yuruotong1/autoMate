import os
import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.opera import OperaDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By

from tools.tools_base import ToolsBase

class WebBrowserElement(ToolsBase):
    def __init__(self):
        super().__init__()
        self.name = "web_element"
        self.description = "利用selenium对指定xpath进行点击或者输入内容"
        self.request_param = '字典，如{"driver": "driver", "xpath": "", "action":"click或send_text"}'
        self.return_content = "True"

    def run(self, param=None):
        driver = param["driver"]
        xpath = param["xpath"]
        action = param["action"]
        if action == "click":
            driver.find_element(By.XPATH, xpath).click()
        elif action == "send_text":
            driver.find_element(By.XPATH, xpath).send_keys(param["text"])
        return True

       
