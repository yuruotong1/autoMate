import unittest

from agent.plan_agent import PlanAgent
from work_principle.okr_principle import OKR_Object
class TestPlanAgent(unittest.TestCase):
    def test_aligning(self):
        # Create an instance of the PlanAgent class
        plan_agent = PlanAgent()
        # Create a mock OKR_Object with a raw_user_task
        okr_object = OKR_Object("因为想要增加编程效率，对比一下copilot和curson谁更好用，比较提示词数量、安装易用性，给出不少于100字的文")
        # Call the aligning method
        plan_agent.aligning(okr_object)

if __name__ == '__main__':
    unittest.main()