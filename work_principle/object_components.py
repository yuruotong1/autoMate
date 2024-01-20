class ObjectComponents:
    def __init__(self) -> None:
        self.content = [
            {"target": "任务主体", "content": "", "descriptions": "任务主体"},
            {"target": "执行动作", "content": "", "descriptions": "执行动作"},
            {"target": "任务背景", "content": "", "descriptions": "任务背景或原因"},
            # "how": {"content": "", "descriptions": "这个任务如何做", "example": ["通过线上直播发布会，合作伙伴渠道和社交媒体宣传", "通过增加人员、改善流程和引入新的服务软件"]},
            {"target": "任务完成程度", "content": "", "descriptions": "任务要做到什么程度，给出具体的几个要求"}
        ]
