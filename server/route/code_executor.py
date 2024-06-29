from flask import Blueprint
from flask import request
home_bp = Blueprint('home', __name__)

@home_bp.route('/execute', methods=["POST"])
def home():
    code = request.get_json()
    exec(code)
    return {"message": "你好"}