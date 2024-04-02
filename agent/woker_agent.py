from langchain.agents import create_react_agent, OpenAIFunctionsAgent
from langchain_core.prompts import MessagesPlaceholder, HumanMessagePromptTemplate, PromptTemplate

from tools.tools_util import ToolsUtil
from utils.llm_util import LLM_Util


class WorkerAgent:
    def run(self, input):
        llm = LLM_Util().llm()
        tools = ToolsUtil.get_tools()
        tool_names = [tool.name for tool in tools]
        prompt = OpenAIFunctionsAgent.create_prompt(
            system_message="",
            extra_prompt_messages=[
                HumanMessagePromptTemplate(
                    prompt=PromptTemplate(input_variables=['input'], template='请输入以下内容：{input}')),
                MessagesPlaceholder(variable_name="chat_history"),
                MessagesPlaceholder(variable_name="tool_names", variable_value=tool_names),
                MessagesPlaceholder(variable_name="tools", variable_value=tools)

            ],
        )
        # agent_executor = initialize_agent(llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        #                                   tools=tools, memory=memory, verbose=True)
        agent_executor = create_react_agent(llm=llm, tools=tools, prompt=prompt)
        return agent_executor.invoke({"input": input})
