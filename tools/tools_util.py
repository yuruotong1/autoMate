from tools.FindDesktopPath import FindDesktopPath
from tools.ListAllFile import ListAllFile
from tools.ListDesktopFiles import ListDesktopFiles
from tools.OpenApplication import OpenApplicationAction
from langchain.tools import StructuredTool
from utils.global_util import GlobalUtil


class ToolsUtil:
    @staticmethod
    def get_tools():
        print("get_tools")
        action_tools = []
        # 从 function_list 中生成工具
        for edit_page in GlobalUtil.edit_page_global:
            # 动态生成 langchain 工具
            langchain_tools = StructuredTool.from_function(
            func=edit_page.run_action,
            name=edit_page.func_name,
            description=edit_page.func_description,
                return_direct=True)
            action_tools.append(langchain_tools)
        print(action_tools)
        return [OpenApplicationAction(), FindDesktopPath(), ListAllFile(), ListDesktopFiles()] + action_tools
