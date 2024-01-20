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

        for k,i in object.five_w_two_h.content.items():
            r = {'是否具备': 'no'}
            content = object.content
            while r["是否具备"]=="no" :
                prompt = f"这是一个任务描述:'{content}'。你觉得这个任务描述具备{i['descriptions']}吗？如果具备返回格式如下：{{'是否具备': 'yes'}}，如果不具备返回格式如下：{{'是否具备': 'no', '原因': '返回具体原因即可'}}"
                self.logger.info(prompt)
                call_openai = self.call_gpt(prompt)
                self.logger.info(call_openai)
                r = json.loads(call_openai)
                if r["是否具备"]=="no":
                    content  = input(f"您的任务描述不清楚，{r['原因']}：")            
            i['content'] = content
        self.logger.info(str(object.five_w_two_h.content))
