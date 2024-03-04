from functions.open_application_func import OpenApplicationFunc


class FunctionList:
    funcs = [OpenApplicationFunc()]

    @classmethod
    def get_funcs(cls):
        return cls.funcs

    @classmethod
    def get_fuc_by_uni_tag(cls, uni_tag):
        for i in cls.funcs:
            if i.uni_tag == uni_tag:
                return i
        return None
