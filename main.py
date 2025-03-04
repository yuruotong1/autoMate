import argparse
import subprocess
import signal
import sys
from gradio_ui import app
from util import download_weights
import time
def run():
    # 启动 server.py 子进程
    server_process = subprocess.Popen(
        ["python", "./server.py"],
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
    )
    try:
        # 下载权重文件
        download_weights.download()
        # 启动 Gradio UI
        app.run()
    finally:
        # 确保在主进程退出时终止子进程
        if server_process.poll() is None:  # 如果进程还在运行
            server_process.terminate()  # 发送终止信号
            server_process.wait(timeout=5)  # 等待进程结束

if __name__ == '__main__':
    run()