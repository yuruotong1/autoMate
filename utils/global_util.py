import os
import pickle
from utils.qt_util import QtUtil


class GlobalUtil:
    edit_page_global = []
    current_page = None
    path = os.path.join(QtUtil.get_root_path(), "cache")


    @classmethod
    def read_from_local(cls):
       
        # 判断文件是否存在
        if not os.path.exists(cls.path):
            return []

        with open(cls.path, "rb") as file:
            data = pickle.load(file).get("action_list_global")
            if not data:
                data = []
            return data

    @classmethod
    def save_to_local(cls):
        with open(cls.path, "wb") as file:
            edit_page_dump = [i.dump() for i in cls.edit_page_global]
            pickle.dump({"action_list_global": edit_page_dump}, file)