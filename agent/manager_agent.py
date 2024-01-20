from agent.agent import Agent
from work_principle.okr_principle import OKR_Object

class ManagerAgent(Agent):
    def __init__(self):
        super().__init__("你是一名总经理，负责对任务进行可量化的评估")

    
    def optimization_Object(self, object:OKR_Object):
        object.content
        # todo 待加入 PDCA循环规则
        # 利用 smart 原则对目标进行评估

        for i in object.five_w_two_h.content:
            r = self.call_gpt(f"你觉得'{object.content}'，说清楚了{i['descriptions']}吗？如果说清楚，返回{i}否则返回'no'")
            if r == "no":
                input(f"请说清楚'{object.content}'的{i}，按回车键继续")
            else:
                i['content'] = r
        
        

        for k, v in object.smart.items():
            self.call_gpt(f"你觉得'{object.content}'这个目标，就{k}来说满分是3分可以打几分，只返回给1或2或3，比如2")
