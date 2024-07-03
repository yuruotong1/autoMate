from flask import Blueprint, Response
from flask import request
from litellm import completion
from utils.sql_util import get_config
import json
home_bp = Blueprint('llm', __name__)

@home_bp.route('/llm', methods=["POST"])
def llm():
    config = get_config()
    messages = request.get_json()["messages"]
    isStream = request.get_json().get("isStream", False)
    if isStream:
        def generate():
            response = completion(
                messages=messages,
                stream=True,
                **json.loads(config)["llm"]
            )
            for part in response:
                yield part.choices[0].delta.content or ""
        return Response(generate(), mimetype='text/event-stream')
    else:
        res =  completion(
            messages=messages,
            **json.loads(config)["llm"]
        )
        return {
            "content": res.choices[0].message.content
        }
   