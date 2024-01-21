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

class WebBrowser(ToolsBase):
    def __init__(self):
        self.name = "web_browser"
        self.description = "利用浏览器进行搜索，入参格式为字符串"

    def run(self, param=None):
        # Load browser configuration from YAML file
        with open("config.yaml", "r") as file:
            config = yaml.safe_load(file)

        # Check if webdriver is available
        if not os.path.exists("webdriver.exe"):
            # Download webdriver based on browser type
            browser_type = config.get("browser_type")
            driver = None
            if browser_type == "chrome":
                options = webdriver.ChromeOptions()
                options.add_argument("--headless")  # Enable headless mode
                webdriver_manager = ChromeDriverManager()
                driver = webdriver.Chrome(webdriver_manager.install(), options=options)
            elif browser_type == "firefox":
                options = webdriver.FirefoxOptions()
                options.add_argument("--headless")  # Enable headless mode
                webdriver_manager = GeckoDriverManager()
                driver = webdriver.Firefox(webdriver_manager.install(), options=options)
            elif browser_type == "edge":
                options = webdriver.EdgeOptions()
                options.add_argument("--headless")  # Enable headless mode
                webdriver_manager = EdgeChromiumDriverManager()
                driver = webdriver.Edge(service=EdgeService(webdriver_manager.install()), options=options)
            elif browser_type == "opera":
                options = webdriver.ChromeOptions()
                options.add_argument("--headless")  # Enable headless mode
                webdriver_manager = OperaDriverManager()
                driver = webdriver.Opera(webdriver_manager.install(), options=options)
        driver.implicitly_wait(10)
        browser_url = config.get("browser_url")
        driver.get(browser_url)
        driver.find_element(by=By.XPATH, value='//*[@id="kw"]').send_keys("陈")
        driver.find_element(by=By.XPATH, value='//*[@id="su"]').click()
        print(driver.page_source)
        driver.quit()
