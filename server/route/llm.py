from fastapi import APIRouter,Request
from fastapi.responses import StreamingResponse
from litellm import completion
from utils.sql_util import get_config
from agent.prompt import code_prompt
import json
llm_route = APIRouter()

@llm_route.post("/llm")
async def llm_post(req:Request):
    data = await req.body()
    data = json.loads(data)
    messages = data["messages"]
    isStream = data.get("isStream", False)
    if data.get("llm_config"):
        config = json.loads(data.get("llm_config"))
    else:
        config = json.loads(get_config())["llm"]
    messages = [{"role": "system", "content": code_prompt.substitute()}] + messages
    # 暂时没有strem
    if isStream:
        def generate():
            response = completion(messages=messages, stream=True, **config)
            for part in response:
                yield part.choices[0].delta.content or ""
        return StreamingResponse(generate(),media_type='text/event-stream')
    else:
        try:
            res = completion(messages=messages, **config)
            return {"content": res.choices[0].message.content, "status": 0}
        except Exception as e:
            return {"content": str(e), "status": 1}
