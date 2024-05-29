from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate, ChatMessagePromptTemplate

from tools.tools_util import ToolsUtil
from utils.llm_util import LLM_Util


class WorkerAgent:
    def get_executor(self):
        llm = LLM_Util().llm()
        tools = ToolsUtil.get_tools()
        prompt = hub.pull("langchain-ai/react-agent-template")
        prompt.partial(instructions="")
        agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
        return agent_executor

    def run(self, question):
        return self.get_executor().invoke({"input": question})["output"]

    @staticmethod
    def get_iter(question):
        llm = LLM_Util().llm()
        tools = ToolsUtil.get_tools()
        example = """Thought: 我需要使用工具吗? 需要\nAction: 桌面路径\nAction Input: ""\nObservation: c:/path/develop\n\n
Thought: 我需要使用工具吗? 需要\nAction: 打开应用\nAction Input: ""\nObservation: 打开成功\n\n
Thought: 我需要使用工具吗? 不需要\nFinal Answer: 您的桌面上有以下文件\n
"""
        prompt = PromptTemplate(
            template="### TOOLS ###\n{tools}#######\n"
                     "### THOUGHT ###Thought:我需要使用工具吗? 需要\n"
                     "Action:{tool_names}\n"
                     "Action Input:Action的输入，如果没有参数请设置为""\n"
                     "Observation:运行[ACTION]得到的结果\n\n"
                     "当输出内容或者不需要使用工具，必须使用以下格式: Thought: 我需要使用工具吗? 不需要\nFinal Answer: [你的回复]######\n"
                     "### EXAMPLE ###\n{example}######\n"
                     "### PREVIOUS CONVERSATION HISTORY ###\n{chat_history}######\n"
                     "### NEW INPUT ###\n{input}######\n{agent_scratchpad}",
            input_variables=['agent_scratchpad', 'input', 'tool_names', 'tools'],
            partial_variables={'chat_history': '', 'instructions': ""}
        )
        prompt = prompt.partial(example=example)
        agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
        return agent_executor.iter({"input": question})

    def run(self, question):
        