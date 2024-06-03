
import httpx
from self_utils.config import Config
from openai import DefaultHttpxClient, OpenAI
class LLM_Util:

    def __init__(self):
        super().__init__()
        self.config = Config()
        self.api_key = self.config.get_config_from_component("llm", "api_key")
        self.base_url = self.config.get_config_from_component("llm", "api_url")
        self.model = self.config.get_config_from_component("llm", "model")
        self.proxy = self.config.get_config_from_component("llm", "proxy")
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url, 
                             http_client=DefaultHttpxClient(
                            proxies=self.proxy,
                            transport=httpx.HTTPTransport(local_address="0.0.0.0"),
                            ),
                            )
        self.res = ""

    # messages = [{ "content": message, "role": "user"}]
    def invoke(self, messages):
        r =  self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True  # 流式请求参数值设置为True
        )
        for i in r:
            stream_res = i.choices[0].delta.content or ""
            self.res += stream_res
            yield stream_res
        messages.append({"content": self.res, "role": "assistant"})


        # response = completion(model=self.model, base_url=self.base_url, api_key=self.api_key,
        #                        messages=messages)

        # return response.json()["choices"][0]["message"]


