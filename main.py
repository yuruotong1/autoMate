import argparse
import subprocess
import signal
import sys
from gradio_ui import app
from util import download_weights
import time
def run():
    # 启动 server.py 子进程，并捕获其输出
    server_process = subprocess.Popen(
        ["python", "./server.py"],
        stdout=subprocess.PIPE,  # 捕获标准输出
        stderr=subprocess.PIPE,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
        text=True
    )

    try:
        # 下载权重文件
        download_weights.download()
        # 启动 Gradio UI
         # 等待 server_process 打印出 "Started server process"
        while True:
            output = server_process.stdout.readline()
            if "Started server process" in output:
                print("Omniparseer服务启动成功...")
                break
            if server_process.poll() is not None:
                raise RuntimeError("Server process terminated unexpectedly")
        app.run()
    finally:
        # 确保在主进程退出时终止子进程
        if server_process.poll() is None:  # 如果进程还在运行
            server_process.terminate()  # 发送终止信号
            server_process.wait(timeout=5)  # 等待进程结束

if __name__ == '__main__':
    run()