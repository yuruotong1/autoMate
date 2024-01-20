from agent.agent import Agent

class ManagerAgent(Agent):
    def __init__(self):
        super().__init__("你是一名总经理，负责与用户沟通需求，制定OKR中的O，并对下属的工作成果进行评估")
