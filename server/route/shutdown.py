import os
from flask import Blueprint
home_bp = Blueprint('shutdown', __name__)
# 关闭服务器
@home_bp.route('/shutdown', methods=["GET"])
def home():
    os._exit(0)