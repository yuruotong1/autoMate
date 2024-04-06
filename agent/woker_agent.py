from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor

from tools.tools_util import ToolsUtil
from utils.llm_util import LLM_Util


class WorkerAgent:
    def run(self, input):
        llm = LLM_Util().llm()
        tools = ToolsUtil.get_tools()
        instructions = """请你回复中文"""
        base_prompt = hub.pull("langchain-ai/react-agent-template")
        prompt = base_prompt.partial(instructions=instructions)
        agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        return agent_executor.invoke({"input": input})["output"]
