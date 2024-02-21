from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from tools.search_engine_tool import SearchEngineTool
from utils.llm_util import LLMUtil


class TestLangChain:
    def test_chain(self):
        template = """根据用户输入，提取出搜索引擎的关键字，返回该关键字:

        {input}"""
        model = LLMUtil().llm()
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | model | StrOutputParser() | SearchEngineTool()
        search_datas = chain.invoke({"input": "谁是李一舟"})
        info = "\n".join(f"{i+1}. {data.title}" for i, data in enumerate(search_datas))
        choice = input(f"下面是百度搜索结果，请选择你觉得有用的信息以逗号分割，如1,3,4：\n{info}")

