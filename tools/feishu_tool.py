import os
from langchain.tools import BaseTool

class FindDesktopPath(BaseTool):
    name = "上传文档到飞书"
    description = "上传文档到飞书"

    # args_schema = None

    def _run(self):
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        return desktop_path