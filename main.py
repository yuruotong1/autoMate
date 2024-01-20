
from o_kr import OKR


class AutoMate:
    def __init__(self):
        pass
    
    
    def rule_define(self):
        o_kr = OKR()
        o_kr.set_objective(input("请输入任务: "))



if __name__ == "__main__":
    automator = AutoMate()
    automator.main()
    # print(automator.call_chatgpt_api("Hello"))
