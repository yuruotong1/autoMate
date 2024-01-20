from agent.manager_agent import ManagerAgent
from work_principle.okr_principle import OKR_Object


class AutoMate:
    def __init__(self):
        pass
    
    
    def rule_define(self):
        # o_kr = OKR_Object(input("请输入任务: "))
        o_kr = OKR_Object("对比一下copilot和curson谁更好用，比较提示词数量、安装易用性，给出不少于100字的文章")
        ManagerAgent().optimization_Object(o_kr)



if __name__ == "__main__":
    automator = AutoMate()
    automator.rule_define()
    # print(automator.call_chatgpt_api("Hello"))
