from openai import OpenAI
from .models import session, LLMApi
from datetime import datetime, timezone
from agents.Agent import Agent


def chat(llm_config: LLMApi, agent: Agent, starter=None):

    client = OpenAI(api_key=llm_config._api_key, 
                    base_url=llm_config.base_url)

    completion = client.chat.completions.create(
        model="gpt-4-turbo",
        stream=False,
        messages=[
            {"role": "system", "content": f"{agent.prompt}"},
            {"role": "user", "content": f"{starter if starter else 'Hello!, please tell me what you can do.'}"}
        ]
    )
    llm_config.last_used_at = datetime.now(timezone.utc)
    session.commit()

    return completion.choices[0].message.content
