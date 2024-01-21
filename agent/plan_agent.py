import logging
from agent.agent_base import AgentBase
from tools.tools_base import ToolsBase
from work_principle.okr_principle import OKR_Object

class PlanAgent(AgentBase):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        super().__init__('你是一名计划拆解者，利用工具将object拆解成key_result，请你返回json格式的内容，比如["使用工具a进行xx操作", "使用工具b进行xx操作"]')

    # 根据object和已有的工具能力拆解成key result，key
    def aligning(self, okr_object: OKR_Object):
        raw = okr_object.raw_user_task
        tools_list = [i().get_info() for i in self.get_subclasses(ToolsBase)]
        r = self.call_gpt(f"object为'{raw}'， 工具列表为{tools_list}")
        print(r)
        self.logger.info(f"Alignment result: {r}")

    def get_subclasses(self, cls):
        subclasses = []
        for subclass in cls.__subclasses__():
            subclasses.append(subclass)
        return subclasses
