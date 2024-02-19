import logging
from agent.agent_base import AgentBase
from tools.tool_base import ToolBase
from tools.tools_factory import ToolsFactory
from work_principle.okr_principle import OKR_Object

class PlanAgent(AgentBase):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        super().__init__('#Goals:\n你是一名计划拆解者，将object拆解成key_result，\n#Workflow:1.')
        '''
        '''
    # '多个key_result完成这一个目标，返回格式如下：{"tools_name":"web_browser","request_param":"请求参数"}'
    # 根据object和已有的工具能力拆解成key result，key
    def aligning(self, okr_object: OKR_Object):
        raw = okr_object.raw_user_task
        r = self.call_gpt(f"object为'{raw}'， 工具列表为{list(ToolsFactory().get_tools())}")
        self.logger.info(f"prompt：object为'{raw}'， 工具列表为{list(ToolsFactory().get_tools())}")
        self.logger.info(f"Alignment result: {r}")
        # return r

    def get_subclasses(self, cls):
        subclasses = []
        for subclass in cls.__subclasses__():
            subclasses.append(subclass)
        return subclasses
