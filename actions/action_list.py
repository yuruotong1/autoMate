from actions.llm_action import LLMAction
from actions.loop_action import LoopAction
from actions.open_application_action import OpenApplicationAction
from actions.open_browser_url_action import OpenBrowserUrlAction
from actions.search_engine_action import SearchEngineAction


class ActionList:
    actions = [OpenApplicationAction,
               OpenBrowserUrlAction,
               SearchEngineAction,
               LLMAction,
               LoopAction]

    @classmethod
    def get_funcs(cls):
        return cls.actions

    @classmethod
    def get_action_by_name(cls, name):
        for i in cls.actions:
            if i.name == name:
                return i
        return None
