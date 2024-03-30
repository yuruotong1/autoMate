from pydantic import BaseModel, Field

from actions.action_base import ActionBase
from utils.selenium_util import SeleniumUtil


class SearchInput(BaseModel):
    key: str = Field(description="要查询的关键词", default="")


# 利用搜索引擎搜索关键词
class SearchEngineAction(ActionBase):
    name = "百度搜索内容"
    description = "利用搜索引擎搜索关键词，得到结果列表"
    args: SearchInput

    def run(self, key):
        """Use the tool."""
        selenium = SeleniumUtil()
        selenium.get_url(f"https://www.baidu.com/s?wd={key}")
        # result_elements = selenium.get_xpath_elements("//*[@class='result c-container xpath-log new-pmd']")
        # search_result = []
        # for result_element in result_elements:
        #     title = result_element.find_element(By.XPATH, ".//h3").text
        #     url = result_element.find_element(By.XPATH, ".//h3/a").get_attribute("href")
        #     short_description = result_element.find_element(By.XPATH, ".//*/span[@class='content-right_8Zs40']").text
        #     search_data = SearchData(title=title, url=url, short_description=short_description)
        #     search_result.append(search_data)
        # return search_result
