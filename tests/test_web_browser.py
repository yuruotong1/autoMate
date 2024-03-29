import logging
import unittest
from idlelib.searchengine import SearchEngine

from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_core.messages import HumanMessage
from langchain_core.prompts import SystemMessagePromptTemplate, PromptTemplate, MessagesPlaceholder, \
    HumanMessagePromptTemplate, ChatPromptTemplate
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_openai import ChatOpenAI

from tools.search_engine_tool import SearchEngineTool
from utils.llm_util import LLMUtil


class TestWebBrowser:
    def test_agent(self):
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
        agent_executor.invoke({"input": "李一舟为什么能成功"})
