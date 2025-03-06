import argparse
import subprocess
import signal
import sys
import platform
from gradio_ui import app
from util import download_weights
import time
import torch

def run():
    try:
        print("cuda is_available: ", torch.cuda.is_available())  # 应该返回True
        print("MPS is_available: ", torch.backends.mps.is_available())
        print("cuda device_count", torch.cuda.device_count())  # 应该至少返回1
        print("cuda device_name", torch.cuda.get_device_name(0))  # 应该显示您的GPU名称
    except Exception:
        print("显卡驱动不适配，请根据readme安装合适版本的 torch！")

    # 启动 server.py 子进程，并捕获其输出
    # Windows: 
    if platform.system() == 'Windows':
        server_process = subprocess.Popen(
            ["python", "./server.py"],
            stdout=subprocess.PIPE,  # 捕获标准输出
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
            text=True
        )
    else:
        server_process = subprocess.Popen(
            ["python", "./server.py"],
            stdout=subprocess.PIPE,  # 捕获标准输出
            stderr=subprocess.PIPE,
            start_new_session=True,
            text=True
        )


    try:
        # 下载权重文件
        download_weights.download()
        print("启动Omniserver服务中，约40s左右，请耐心等待！")
        # 启动 Gradio UI
         # 等待 server_process 打印出 "Started server process"
        while True:
            output = server_process.stdout.readline()
            if "Omniparser initialized" in output:
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