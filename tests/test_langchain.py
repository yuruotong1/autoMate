from functions.open_application_tool import OpenApplicationInput, OpenApplicationTool
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from tools.search_engine_tool import SearchEngineTool

from utils.llm_util import LLM_Util


class TestLangChain:
    def test_chain(self):
        template = """根据用户输入，提取出搜索引擎的关键字，返回该关键字:

        {input}"""
        model = LLM_Util().llm()
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | model | StrOutputParser() | SearchEngineTool()

        search_datas = chain.invoke({"input": "谁是李一舟"})
        info = "\n".join(f"{i + 1}. {data.title}" for i, data in enumerate(search_datas))
        choice = input(f"下面是百度搜索结果，请选择你觉得有用的信息以逗号分割，如1,3,4，直接回车代表all in：\n{info}")
        choice = list(map(int, choice.split(",")))

    def test_chain(self):
        a = OpenApplicationTool()
        # a.invoke(r"C:\Users\yuruo\Desktop\HBuilder X.lnk")
        b = OpenApplicationInput.model_fields
        for c in b.keys():
            print(c)
            print(b[c].title)
