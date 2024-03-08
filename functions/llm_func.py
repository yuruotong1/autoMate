from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from functions.function_base import FunctionBase
from utils.llm_util import LLMUtil


class LLMInput(BaseModel):
    question: str = Field(description="需要问的问题", title="问题内容")


class LLMFunc(FunctionBase):
    name = "大模型问答"
    description = "利用大模型进行回答"
    args_schema = LLMInput

    def run(self, question):
        llm = LLMUtil().llm()
        return llm.invoke(question).content
