from agent.agent import Agent

class WokerAgent(Agent):
    def __init__(self):
        super().__init__("你是一名计划拆解者，负责对OKR中的O进行拆解并制定KR，向总经理汇报")