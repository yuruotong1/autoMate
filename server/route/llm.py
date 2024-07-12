from flask import Blueprint, Response, request
from litellm import completion
from utils.sql_util import get_config
from agent.prompt import code_prompt
import json
import re



home_bp = Blueprint('llm', __name__)

@home_bp.route('/llm', methods=["POST"])
def llm():
    data = request.get_json()
    messages = data["messages"]
    if data.get("llm_config"):
        config = json.loads(data.get("llm_config"))
    else:
        config = json.loads(get_config())["llm"]
    messages = [{"role": "system", "content": code_prompt.substitute()}] + messages
    try:
        res = completion(messages=messages, **config).choices[0].message.content
        return {"content": res, "code": extract_code_blocks(res), "status": 0}
    except Exception as e:
        return {"content": str(e), "status": 1}



def extract_code_blocks(text):
    pattern_match = [
        r'.*?```python([\s\S]*?)```.*',
        r'.*?```([\s\S]*?)```.*'
    ]
    for pattern in pattern_match:
        pattern = re.compile(pattern, re.MULTILINE).findall(text)
        if pattern:
            return pattern[0]
        else:
            continue
    return ""