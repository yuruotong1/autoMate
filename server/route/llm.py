from flask import Blueprint, Response, request
from litellm import completion
from utils.sql_util import get_config
from agent.prompt import code_prompt
import json

home_bp = Blueprint('llm', __name__)

@home_bp.route('/llm', methods=["POST"])
def llm():
    data = request.get_json()
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
        return Response(generate(), mimetype='text/event-stream')
    else:
        try:
            res = completion(messages=messages, **config)
            return {"content": res.choices[0].message.content, "status": 0}
        except Exception as e:
            return {"content": str(e), "status": 1}
