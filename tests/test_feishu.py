from utils.feishu_util import FeiShuUtil


class TestFeiShu:
    def test_get_token(self):
        feishu_util = FeiShuUtil()
        feishu_util.get_token()

