from functions.open_application_func import OpenApplicationFunc
from functions.open_browser_url_func import OpenBrowserUrlFunc


class FunctionList:
    funcs = [OpenApplicationFunc(), OpenBrowserUrlFunc()]

    @classmethod
    def get_funcs(cls):
        return cls.funcs

    @classmethod
    def get_fuc_by_name(cls, name):
        for i in cls.funcs:
            if i.name == name:
                return i
        return None
