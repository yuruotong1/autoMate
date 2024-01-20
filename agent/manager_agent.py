import json
from agent.agent_base import AgentBase
from work_principle.okr_principle import OKR_Object
import logging
logging.basicConfig(level=logging.INFO)
class ManagerAgent(AgentBase):
    def __init__(self):
        super().__init__("你是一名总经理，负责对任务进行可量化的评估")
        self.logger = logging.getLogger(__name__)

    def optimization_Object(self, object:OKR_Object):
        # todo 待加入 PDCA循环规则
        # 利用 smart 原则对目标进行评估

        for i in object.five_w_two_h.content:
            content = object.content
            call_openai_res = {'isOk': 'no', 'content': ''}
            while call_openai_res["isOk"]=="no" :
                prompt = f"这是一个任务描述:'{content}'。你觉得这个任务描述具备{i['descriptions']}吗？如果具备返回格式如下：{{\"isOk\":\"yes\", \"content\":\"提炼出任务的{i['descriptions']}\"}}，如果不具备返回格式如下：{{\"isOk\":\"no\",\"content\":\"返回不具备的原因并给出完善建议\"}}"
                self.logger.info(prompt)
                call_openai_res = json.loads(self.call_gpt(prompt))
                self.logger.info(call_openai_res)
                if call_openai_res["isOk"]=="no":
                    content  = content + f"，{i['target']}：" +input(f"【警告】{call_openai_res['content']}\n请您补充信息：")
            i['content'] = call_openai_res["content"]
        self.logger.info(str(object.five_w_two_h.content))
