import requests

class FeiShuUtil:
    def get_token(self):
        app_id = ""
        app_secret = ""
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        res = requests.post(url)
        print(res)