from agent.agent_base import AgentBase
from work_principle.okr_principle import OKR_Object

class PlanAgent(AgentBase):
    def __init__(self):
        super().__init__("你是一名计划拆解者，负责对OKR中的O进行拆解并制定KR，向总经理汇报")


     # 与用户对齐目标，填充缺失的信息
    def aligning(self, okr_object:OKR_Object):
        pass



    