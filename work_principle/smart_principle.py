class SMARTPrincipleBase:
    def __init__(self):
        pass

    def get_principle(self):
        pass


class Specific(SMARTPrincipleBase):
    def __init__(self):
        self.what={"content":"", "description":""}
        self.why=""
        self.where=""
        
        
    def get_principle(self):
        """
        具体原则列表

        Returns:
            list: 具体原则的列表
        """
        return ["是什么", "为什么要做", "哪里做"]


class Measurable(SMARTPrincipleBase):
    """
    可衡量原则类
    """
    def get_principle(self):
        return ["做到什么程度"]


class Achievable(SMARTPrincipleBase):
    """
    可实现原则类
    """
    def get_principle(self):
        return ["怎么做"]


class Relevant(SMARTPrincipleBase):
    """
    相关性原则类
    """
    pass


class TimeBound(SMARTPrincipleBase):
    """
    时间限制原则类
    """
    def get_principle(self):
        return ["什么时候做"]
