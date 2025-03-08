from openai import OpenAI

class BaseAgent:
    def __init__(self, config, *args, **kwargs):
        self.config = config
        self.SYSTEM_PROMPT = ""

    def chat(self, messages):
        client = OpenAI(base_url=self.config.OPENAI_BASE_URL, api_key=self.config.OPENAI_API_KEY)
        messages = [{"role": "system", "content": self.SYSTEM_PROMPT}] + messages
        response = client.chat.completions.create(
            model=self.config.OPENAI_MODEL,
            messages=messages
        )
        return response.choices[0].message.content
    
