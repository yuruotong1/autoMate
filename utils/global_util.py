import os
import pickle
from utils.qt_util import QtUtil


class GlobalUtil:
    edit_page_global = []
    current_page = None
    all_widget = []
    path = os.path.join(QtUtil.get_root_path(), "cache")


    @classmethod
    def get_widget_by_uuid(cls, uuid: str):
        for widget in cls.all_widget:
            if widget.uuid == uuid:
                return widget
        return None

    # @classmethod
    # def delete_widget_by_uuid(cls, uuid: str):
    #     for widget in cls.all_widget:
    #         if widget.uuid == uuid:
    #             cls.all_widget.remove(widget)
    #             break
    
    @classmethod
    def delete_widget(cls, widget):
        cls.all_widget.remove(widget)

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