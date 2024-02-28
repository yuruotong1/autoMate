from typing import Optional, Type, Any, List
from langchain_core.callbacks import CallbackManagerForToolRun, AsyncCallbackManagerForToolRun
from langchain.pydantic_v1 import BaseModel, Field
from selenium.webdriver.common.by import By

from data_class.search_data import SearchData
from tools.tool_base import ToolBase
from utils.selenium_util import SeleniumUtil


class SearchInput(BaseModel):
    key: str = Field(description="要查询的关键词")


# 利用搜索引擎搜索关键词
class SearchEngineTool(ToolBase):
    name = "web_browser"
    description = "利用搜索引擎搜索关键词，得到结果列表"
    args_schema: Type[BaseModel] = SearchInput


    def _run(self, key: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> list[SearchData]:
        """Use the tool."""
        selenium = SeleniumUtil()
        selenium.get_url(f"https://www.baidu.com/s?wd={key}")
        result_elements = selenium.get_xpath_elements("//*[@class='result c-container xpath-log new-pmd']")
        search_result = []
        for result_element in result_elements:
            title = result_element.find_element(By.XPATH, ".//h3").text
            url = result_element.find_element(By.XPATH, ".//h3/a").get_attribute("href")
            short_description = result_element.find_element(By.XPATH, ".//*/span[@class='content-right_8Zs40']").text
            search_data = SearchData(title=title, url=url, short_description=short_description)
            search_result.append(search_data)
        return search_result

    async def _arun(
            self, key: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")
