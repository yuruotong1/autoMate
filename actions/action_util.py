from typing import Union, List
from actions.action_base import ActionBase
from actions.llm_action import LLMAction
from actions.loop_action import LoopAction
from actions.open_application_action import OpenApplicationAction
from actions.open_browser_url_action import OpenBrowserUrlAction
from actions.search_engine_action import SearchEngineAction


class ActionUtil:
    actions = [OpenApplicationAction,
               OpenBrowserUrlAction,
               SearchEngineAction,
               LLMAction,
               LoopAction]

    @classmethod
    def get_funcs(cls) -> List[ActionBase.__class__]:
        return cls.actions

    @classmethod
    def get_action_by_name(cls, name) -> ActionBase.__class__:
        for i in cls.actions:
            if i.name == name:
                return i
        raise ValueError(f"未找到名为{name}的Action")
