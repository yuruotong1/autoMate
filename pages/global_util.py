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
        cache_path = os.path.join(Config.get_app_settings_path(), 'cache')
        # 判断文件是否存在
        if not os.path.exists(cache_path):
            return []

        with open(cache_path, "rb") as file:
            data = pickle.load(file).get("action_list_global")
            if not data:
                data = []
            return data

    @classmethod
    def save_to_local(cls):
        cache_path = os.path.join(Config.get_app_settings_path(), 'cache')
        with open(cache_path, "wb") as file:
            edit_page_dump = [i.dump() for i in cls.edit_page_global]
            pickle.dump({"action_list_global": edit_page_dump}, file)

    @classmethod
    def load_data(cls):
        # 根据配置文件的配置，从本地文件中或者网上读取
        config = Config()
        cls.edit_page_global = []
        if config.DATA_POSITION == "local":
            edit_pages_json = cls.read_from_local()
        elif config.DATA_POSITION == "remote":
            edit_pages_json = []
        else:
            edit_pages_json = []
        return edit_pages_json
