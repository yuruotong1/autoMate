import os
import requests
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.opera import OperaDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
import openai
from selenium.webdriver.common.by import By


class AutoMate:
    def __init__(self):
        pass
    def main(self):
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

    def call_chatgpt_api(self, input_text):
        # Load API configuration from YAML file
        with open("config.yaml", "r") as file:
            config = yaml.safe_load(file).get("openai")

        openai.api_key = config.get("api_key")
        openai.base_url = config.get("api_url")

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # GPT-3.5 model
            messages=[
                {"role": "user", "content": input_text}
            ],
            temperature=0.7
        )

        generated_text = response.choices[0].message.content

        return generated_text



if __name__ == "__main__":
    automator = AutoMate()
    automator.main()
    # print(automator.call_chatgpt_api("Hello"))
