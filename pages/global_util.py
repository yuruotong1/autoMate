import os
import pickle

from utils.config import Config


class GlobalUtil:
    edit_page_global = []
    current_page = None

    @classmethod
    def get_edit_page_by_position(cls, func_status, row, column):
        for i in cls.edit_page_global:
            if i.func_list_pos_row == row and i.func_list_pos_column == column \
                    and i.func_status == func_status:
                return i
        return None

    @classmethod
    def delete_edit_page(cls, edit_page):
        cls.edit_page_global.remove(edit_page)

    @classmethod
    def read_from_local(cls):
        # 判断文件是否存在
        if not os.path.exists("./cache"):
            return []

        with open("./cache", "rb") as file:
            data = pickle.load(file).get("action_list_global")
            if not data:
                data = []
            return data

    @classmethod
    def save_to_local(cls):
        with open("./cache", "wb") as file:
            edit_page_dump = [i.dump() for i in cls.edit_page_global]
            pickle.dump({"action_list_global": edit_page_dump}, file)

    @classmethod
    def load_data(cls):
        # 根据配置文件的配置，从本地文件中或者网上读取
        edit_pages_json = cls.read_from_local()
        for edit_page_json in edit_pages_json:
            from pages.edit_page import EditPage
            from pages.edit_action_list_view import ActionList
            edit_page = EditPage(
                func_status=edit_page_json["func_status"],
                func_list_pos_row=edit_page_json["func_list_pos_row"],
                func_list_pos_column=edit_page_json["func_list_pos_column"],
                # TODO待优化加载问题
                action_list=ActionList.load(edit_page_json["action_list"]))
            edit_page.func_name = edit_page_json["func_name"]
            edit_page.func_description = edit_page_json["func_description"]
            GlobalUtil.edit_page_global.append(edit_page)
