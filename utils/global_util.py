import os
import pickle
from utils.qt_util import QtUtil


class GlobalUtil:
    current_page = None
    all_widget = {"edit_page": {}, "action_list": {}, "action_list_item": {}}
    path = os.path.join(QtUtil.get_root_path(), "cache")

    @classmethod
    def init(cls):
        cls.all_widget = {"edit_page": {}, "action_list": {}, "action_list_item": {}}
        cls.current_page = None

    # type 分为 edit_page, action_list, action_list_item
    @classmethod
    def get_widget_by_uuid(cls, uuid: str, type: str):
        return cls.all_widget[type][uuid]
    
    @classmethod
    def delete_local_by_position(cls, func_status: str, func_list_pos_row: int, func_list_pos_column: int):
        edit_pages_jsons = cls.read_from_local()
        for edit_page_json in edit_pages_jsons:
            if edit_page_json["func_status"] == func_status and\
                edit_page_json["func_list_pos_row"] == func_list_pos_row and\
                edit_page_json["func_list_pos_column"] == func_list_pos_column:
                edit_pages_jsons.remove(edit_page_json)
                break
        with open(cls.path, "wb") as file:
            pickle.dump({"edit_pages": edit_pages_jsons}, file)

    @classmethod
    def delete_widget(cls, widget):
        cls.all_widget.remove(widget)

    @classmethod
    def read_from_local(cls):
        # 判断文件是否存在
        if not os.path.exists(cls.path):
            return []

        with open(cls.path, "rb") as file:
            data = pickle.load(file).get("edit_pages")
            if not data:
                data = []
            return data

    @classmethod
    def save_to_local(cls):
        edit_pages = cls.read_from_local()
        found = False
        for edit_page in edit_pages:
            if edit_page["uuid"] == cls.current_page.uuid:
                edit_page.update(cls.current_page.dump())
                found = True
                break
        if not found:
            edit_pages.append(cls.current_page.dump())
        with open(cls.path, "wb") as file:
            pickle.dump({"edit_pages": edit_pages}, file)

