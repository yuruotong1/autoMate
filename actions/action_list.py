from actions.llm_func import LLMAction
from actions.open_application_func import OpenApplicationFunc
from actions.open_browser_url_func import OpenBrowserUrlAction
from actions.search_engine_func import SearchEngineFunc


class ActionList:
    funcs = [OpenApplicationFunc(), OpenBrowserUrlAction(), SearchEngineFunc(), LLMAction()]

    @classmethod
    def get_funcs(cls):
        return cls.funcs

    @classmethod
    def get_fuc_by_name(cls, name):
        for i in cls.funcs:
            if i.name == name:
                return i
        return None
