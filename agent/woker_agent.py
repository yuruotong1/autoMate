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
        instructions = ""
        prompt = PromptTemplate(
            template="{instructions}\n\nTOOLS:\n------\n\n你可以使用以下工具:\n\n{tools}\n\n使用工具时，请使用以下格式：\n\n"
                     "```\n'Thought: 我需要使用工具吗? 需要\nAction: {tool_names}'\n"
                     "'Action Input: Action的输入'\n'Observation: 运行Action的结果'\n```"
                     "\n\n当输出内容时，或者不需要使用工具，必须使用以下格式: "
                     "\n\n```\nThought: 我需要使用工具吗? 不需要\nFinal Answer: [你的回复]\n```\n\n开始!\n\n"
                     "Previous conversation history:\n{chat_history}\n\nNew input: {input}\n{agent_scratchpad}",
            input_variables=['agent_scratchpad', 'input', 'tool_names', 'tools'],
            partial_variables={'chat_history': '', 'instructions': ""}
        )
        base_prompt = hub.pull("langchain-ai/react-agent-template")
        # prompt = base_prompt.partial(instructions=instructions)
        agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
        return agent_executor.iter({"input": question})
