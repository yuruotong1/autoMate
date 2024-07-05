from flask import Blueprint, Response
from flask import request
from litellm import completion
from utils.sql_util import get_config
import json
home_bp = Blueprint('llm', __name__)

@home_bp.route('/llm', methods=["POST"])
def llm():
    
    messages = request.get_json()["messages"]
    isStream = request.get_json().get("isStream", False)
    llm_config = request.get_json().get("llm_config", None)
    if llm_config:
        config = json.loads(llm_config)
    else:
        config = json.loads(get_config())["llm"]
    if isStream:
        def generate():
            response = completion(
                messages=messages,
                stream=True,
                **config
            )
            for part in response:
                yield part.choices[0].delta.content or ""
        return Response(generate(), mimetype='text/event-stream')
    else:
        res =  completion(
            messages=messages,
            **config
        )
        return {
            "content": res.choices[0].message.content
        }
   