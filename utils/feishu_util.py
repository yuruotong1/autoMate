import requests

from utils.config import Config

class FeiShuUtil:
    def get_token(self):
        config = Config()
        app_id = config.get_config_from_component("feishu", "app_id")
        app_secret = config.get_config_from_component("feishu", "app_secret")
        body = {
            "app_id": app_id,
            "app_secret": app_secret
        }
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        res = requests.post(url, json=body)
        print(res)

