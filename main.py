import os
import sys

import leancloud
from PyQt6.QtWidgets import QApplication, QWidget
from langchain.agents import create_openai_functions_agent, AgentExecutor, AgentType, create_react_agent
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder, PromptTemplate, \
    HumanMessagePromptTemplate

from ui.login_page import LoginPage
from agent.manager_agent import ManagerAgent
from agent.plan_agent import PlanAgent
from tools.search_engine_tool import SearchEngineTool
from utils.config import Config
from utils.llm_util import LLMUtil
from work_principle.okr_principle import OKR_Object
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)


class AutoMate:
    def __init__(self):
        pass

    # def rule_define(self):
    #     # 与用户对齐任务
    #     while True:
    #         o_kr = OKR_Object(
    #             "因为想要增加编程效率，对比一下copilot和curson谁更好用，比较提示词数量、安装易用性，给出不少于100字的文章")
    #         ManagerAgent().optimization_Object(o_kr)
    #         r = input(f"最终对齐的任务是：{o_kr.raw_user_task}，一切都OK对吧？y/n\n")
    #         if r == "y":
    #             break
    #
    #     # 让计划拆解者拆解任务
    #     PlanAgent().aligning(o_kr)

    def run(self):
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
                    self.goto_login_page()
                else:
                    print("登陆成功")
        else:
            self.goto_login_page()

    def goto_login_page(self):
        app = QApplication(sys.argv)
        w = LoginPage()
        w.show()
        sys.exit(app.exec())


if __name__ == "__main__":
    automator = AutoMate()
    automator.run_ui()
    # print(automator.call_chatgpt_api("Hello"))
