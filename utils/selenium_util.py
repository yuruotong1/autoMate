import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.service import Service as ChromeService

from utils.config import Config


class SeleniumUtil:
    def __init__(self):
        config = Config()
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
            return
        driver.implicitly_wait(10)
        self.driver = driver

    def get_url(self, url):
        self.driver.get(url)

    def click(self, xpath):
        self.driver.find_element(By.XPATH, xpath).click()

    def send(self, xpath, text):
        self.driver.find_element(By.XPATH, xpath).send_keys(text)

    def quit(self):
        self.driver.quit()

    def get_text(self, xpath):
        return self.driver.find_element(xpath).text

    def get_attribute(self, xpath, name):
        return self.driver.find_element(xpath).get_attribute(name)

    def get_xpath_elements(self, xpath):
        return self.driver.find_elements(By.XPATH, xpath)