
from agent.manager_agent import ManagerAgent
from work_principle.okr_principle import OKR


class AutoMate:
    def __init__(self):
        pass
    
    
    def rule_define(self):
        o_kr = OKR()
        o_kr.set_objective(input("请输入任务: "))
        ManagerAgent().call_gpt(o_kr)




if __name__ == "__main__":
    automator = AutoMate()
    automator.rule_define()
    # print(automator.call_chatgpt_api("Hello"))
