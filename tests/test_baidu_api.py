from interpreter import interpreter

class OpenInterpreter:
    def test_api(self):
        interpreter.chat("电脑桌面有什么文件？")
        
if __name__ == "__main__":
    interpreter.llm.api_key = "sk-i6ClcJAogigoWxI9271b80E978374e8dAbC1167d3b6d8eA3" # LiteLLM, which we use to talk to LM Studio, requires this
    interpreter.llm.api_base = "https://api.fast-tunnel.one/v1" # Point this at any OpenAI compatible server
    OpenInterpreter().test_api()


