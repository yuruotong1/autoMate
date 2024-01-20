from agent.agent_base import AgentBase

class WokerAgent(AgentBase):
    def __init__(self):
        super().__init__("你是一名工作者，负责执行OKR中的KR，向总计划制定者汇报")
