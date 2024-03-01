import logging
import os
import sys

import leancloud
from PyQt6.QtWidgets import QApplication
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder, PromptTemplate, \
    HumanMessagePromptTemplate

from pages.edit_page import EditPage
from pages.login_page import LoginPage
from tools.search_engine_tool import SearchEngineTool
from utils.config import Config
from utils.llm_util import LLMUtil

# 设置日志
logging.basicConfig(level=logging.INFO)


def run():
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate(
                prompt=PromptTemplate(input_variables=[], template='你是一个工作助手')),
            MessagesPlaceholder(variable_name='chat_history', optional=True),
            HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['input'], template='{input}')),
            MessagesPlaceholder(variable_name='agent_scratchpad')
        ]
    )
    model = LLMUtil().llm()
    tools = [SearchEngineTool()]
    agent = create_openai_functions_agent(model, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, return_intermediate_steps=True)
    r = input("请输入你的问题：\n")
    agent_executor.invoke({"input": r})


class AutoMate:
    def __init__(self):
        self.page = None

    def run_ui(self):
        config = Config()
        leancloud.init(config.LEAN_CLOUD["id"], config.LEAN_CLOUD["key"])
        # 从文件中判断是否有session
        tmp_file = "./session"
        if os.path.exists(tmp_file):
            with open(tmp_file, 'rb') as file:
                session_token = file.read()
                leancloud.User.become(session_token)
                authenticated = leancloud.User.get_current().is_authenticated()
                if not authenticated:
                    self.page = LoginPage()
                    self.page.show()
                else:
                    self.page = EditPage()
        else:
            self.page = LoginPage()
            self.page.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # page = AutoMate()
    # page.run_ui()
    page = EditPage()
    page.show()
    sys.exit(app.exec())
