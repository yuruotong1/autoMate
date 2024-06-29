import io
import sys
import traceback
from flask import Blueprint
from flask import request
home_bp = Blueprint('home', __name__)

@home_bp.route('/execute', methods=["POST"])
def home():
    code = request.get_json()["code"]
    # 创建一个 StringIO 对象来捕获输出
    output = io.StringIO()
    # 保存当前的 stdout
    old_stdout = sys.stdout
    sys.stdout = output
    result = ""
    try:
        exec(code)
        result = {"status": "success", "result": output.getvalue()}
    except Exception as e:
        sys.stdout = old_stdout
        result = {"status": "error", "result": traceback.format_exc()}
    finally:
        sys.stdout = old_stdout
    return result