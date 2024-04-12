from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate, ChatMessagePromptTemplate

from tools.tools_util import ToolsUtil
from utils.llm_util import LLM_Util


class WorkerAgent:
    def get_executor(self):
        llm = LLM_Util().llm()
        tools = ToolsUtil.get_tools()
        # prompt = PromptTemplate(
        #     template="{instructions}\n\nTOOLS:\n------\n\n你可以使用以下工具:\n\n{tools}\n\n使用工具时，请使用以下格式：\n\n"
        #              "```\nThought: 我需要使用工具吗? 需要\nAction: {tool_names}\n"
        #              "Action Input: Action的输入'\n'Observation: 运行Action的结果\n```"
        #              "\n\n当输出内容时，或者不需要使用工具，必须使用以下格式: "
        #              "\n\n```\nThought: 我需要使用工具吗? 不需要\nFinal Answer: [你的回复]\n```\n\n开始!\n\n"
        #              "Previous conversation history:\n{chat_history}\n\nNew input: {input}\n{agent_scratchpad}",
        #     input_variables=['agent_scratchpad', 'input', 'tool_names', 'tools'],
        #     partial_variables={'chat_history': '', 'instructions': ""}
        # )
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
        example = """例子如下：案例1：```Thought: 我需要使用工具吗? 需要\nAction: 桌面路径\nAction Input: 无\nObservation: c:/path/develop```\n
案例2：```Thought: 我需要使用工具吗? 需要\nAction: 打开应用\nAction Input: xxx\nObservation: 打开成功```\n
案例3：```Thought: 我需要使用工具吗? 不需要\nFinal Answer: 您的桌面上有以下文件```\n
"""
        prompt = PromptTemplate(
            template="TOOLS:\n------\n\n你可以使用以下工具:\n\n{tools}\n\n使用工具时，请使用以下格式：\n\n"
                     "```\n'Thought: 我需要使用工具吗? 需要\nAction: {tool_names}'\n"
                     "'Action Input: Action的输入'\n'Observation: 运行Action的结果'\n```"
                     "\n\n当输出内容时，或者不需要使用工具，必须使用以下格式: "
                     "\n\n```\nThought: 我需要使用工具吗? 不需要\nFinal Answer: [你的回复]\n```\n\n{example}\n\n"
                     "Previous conversation history:\n{chat_history}\n\nNew input: {input}\n{agent_scratchpad}",
            input_variables=['agent_scratchpad', 'input', 'tool_names', 'tools'],
            partial_variables={'chat_history': '', 'instructions': ""}
        )
        prompt = prompt.partial(example=example)
        agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
        return agent_executor.iter({"input": question})
