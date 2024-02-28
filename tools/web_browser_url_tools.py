import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.service import Service as ChromeService

from tools.tool_base import ToolBase


class WebBrowserUrl():
    def __init__(self):
        super().__init__()

    def run(self, url):
        # Load browser configuration from YAML file
        driver = None
        # Download webdriver based on browser type
        browser_type = self.config.BROWSER.get("browser_type")
        if browser_type == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")  # Enable headless mode
            webdriver_manager = ChromeDriverManager()
            driver = webdriver.Chrome(service=ChromeService(webdriver_manager.install()), options=options)
        elif browser_type == "edge":
            options = webdriver.EdgeOptions()
            # options.add_argument("--headless")  # Enable headless mode
            webdriver_manager = EdgeChromiumDriverManager()
            driver = webdriver.Edge(service=EdgeService(webdriver_manager.install()), options=options)
        else:
            return
        driver.implicitly_wait(10)
        driver.quit()
        return driver
