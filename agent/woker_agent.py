from langchain import hub
from langchain.agents import create_react_agent, OpenAIFunctionsAgent, AgentExecutor
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
                MessagesPlaceholder(variable_name="tools", variable_value=tools),

            ],
        )
        instructions = """请你回复中文"""
        base_prompt = hub.pull("langchain-ai/react-agent-template")
        prompt = base_prompt.partial(instructions=instructions)
        print(prompt)
        # agent_executor = initialize_agent(llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        #                                   tools=tools, memory=memory, verbose=True)
        agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        return agent_executor.invoke({"input": input})["output"]
