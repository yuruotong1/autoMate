import json
from agent.agent_base import AgentBase
from agent.plan_agent import PlanAgent
from work_principle.okr_principle import OKR_Object
import logging

class ManagerAgent(AgentBase):
    def __init__(self):
        super().__init__("你是一名总经理，负责与客户对齐目标，与计划拆解者对齐关键结果")
        self.logger = logging.getLogger(__name__)

    # 与用户对齐目标，填充缺失的信息
    def optimization_Object(self, okr_object: OKR_Object):
        # todo 待加入 PDCA循环规则
        for i in okr_object.task.content:
            call_openai_res = {'isOk': 'no', 'content': ''}
            while call_openai_res["isOk"] == "no":
                prompt = f"这是一个任务描述:'{okr_object.raw_user_task}'。你觉得这个任务描述具备{i['descriptions']}吗？如果具备返回格式如下：{{\"isOk\":\"yes\", \"content\":\"提炼出任务的{i['descriptions']}\"}}，如果不具备返回格式如下：{{\"isOk\":\"no\",\"content\":\"返回不具备的原因并给出完善建议\"}}"
                call_openai_res = json.loads(self.call_gpt(prompt))
                if call_openai_res["isOk"] == "no":
                    okr_object.raw_user_task = okr_object.raw_user_task + f"，{i['target']}：" + input(
                        f"【警告】{call_openai_res['content']}\n请您补充信息：")
            i['content'] = call_openai_res["content"]


    # 与计划拆解者对齐关键结果，填充缺失的信息
    def assign_task_to_plan_agent(self, okr_object: OKR_Object):
        okr_object.task.raw_user_task
        PlanAgent()
