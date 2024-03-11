from pydantic import BaseModel, Field
from actions.action_base import ActionBase


class LoopInput(BaseModel):
    loop_number: int = Field(description="循环次数", title="循环次数")
    stop_condition: int = Field(description="循环退出条件，python表达式", title="循环退出条件")
    loop_interval_time: int = Field(description="循环间隔时间，单位是秒", title="循环间隔时间(秒)")


class LoopAction(ActionBase):
    name = "循环执行"
    description = "根据循环次数，执行输入内容"
    args_schema = LoopInput

    def run(self, loop_number, stop_condition, loop_interval_time):
        pass
