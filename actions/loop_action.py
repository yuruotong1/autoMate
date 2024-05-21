import time

from pydantic import BaseModel, Field
from actions.action_base import ActionBase
from utils.global_util import GlobalUtil

class LoopInput(BaseModel):
    # loop_number: int = Field(description="循环次数", title="循环次数", default=0)
    stop_condition: str = Field(description="循环退出条件，python表达式", title="循环退出条件", default="False")
    loop_interval_time: int = Field(description="循环间隔时间，单位是秒", title="循环间隔时间(秒)", default=0)
    # action_li st 代表内置参数，会被映射成ActionList对象，_type=after_config 
    # 如果是 after_config 类型，则需要在editPage页面手动配置后填充值
    action_list: list[ActionBase] = Field(description="循环执行的内容", title="循环执行的内容", default=[], _type="after_config")


class LoopAction(ActionBase):
    name: str = "循环执行"
    description: str = "根据循环条件循环执行"
    action_type: str = "include"
    args: LoopInput

    def run(self, stop_condition, loop_interval_time, action_list):
        while True:
            if eval(stop_condition, {}, GlobalUtil.current_page.get_output_dict()):
                break
            for action_dict in action_list:
                from actions.action_util import ActionUtil
                action = ActionUtil.get_action_by_name(action_dict["name"]).model_validate(action_dict)
                action.run_with_out_arg()
            print(GlobalUtil.current_page.get_output_dict())
            time.sleep(loop_interval_time)
