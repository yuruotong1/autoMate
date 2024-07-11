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
            res = completion(messages=messages, **config).choices[0].message.content
            return {"content": res, "isExistCode": contains_code(res), "status": 0}
        except Exception as e:
            return {"content": str(e), "status": 1}


def contains_code(text):
    markdown_patterns = [
        r'```.*?```',
        r'```[\s\S]*?```'
    ]
    for pattern in markdown_patterns:
        if re.search(pattern, text, re.MULTILINE):
            return 0
    return 1


if __name__ == "__main__":
    print(contains_code("为了帮助你打开并读取位于桌面上的 `a.txt` 文件，以下是相应的Python代码。请确保根据你的系统环境（如Windows或Mac OS），调整文件路径。\\n\\n```python\\n# 打开并读取桌面上的 a.txt 文件\\ntry:\\n    with open('/Users/your_username/Desktop/a.txt', 'r') as file:  # 请根据你的系统路径修改文件路径\\n        content = file.read()  # 读取文件\\n    print(content)  # 显示文件内容\\nexcept FileNotFoundError:\\n    print(\\\"文件没有找到，请确保文件路径正确。\\\")\\nexcept Exception as e:\\n    print(\\\"读取文件时发生错误:\\\", e)\\n```\\n\\n请将 `/Users/your_username/Desktop/a.txt` 中的 `your_username` 替换为你的用户名称。如果你是Windows用户，路径可能类似于 `C:\\\\\\\\Users\\\\\\\\your_username\\\\\\\\Desktop\\\\\\\\a.txt`。"))