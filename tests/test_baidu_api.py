from selenium.webdriver.common.by import By

from utils.selenium_util import SeleniumUtil


class TestBaiduApi:
    def test_api(self):
        selenium = SeleniumUtil()
        selenium.get_url("https://www.baidu.com/s?wd=搜索引擎 api 汇总")
        result_elements = selenium.get_xpath_elements("//*[@class='result c-container xpath-log new-pmd']")
        for result_element in result_elements:
            title = result_element.find_element(By.XPATH, ".//h3").text
            url = result_element.find_element(By.XPATH, ".//h3/a").get_attribute("href")
            short_description = result_element.find_element(By.XPATH, ".//*/span[@class='content-right_8Zs40']").text
            print(result_element)

