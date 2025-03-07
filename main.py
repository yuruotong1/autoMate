import subprocess
from threading import Thread
import time
import requests
from gradio_ui import app
from util import download_weights
import torch
import socket

def run():
    try:
        print("cuda is_available: ", torch.cuda.is_available())  # 应该返回True
        print("MPS is_available: ", torch.backends.mps.is_available())
        print("cuda device_count", torch.cuda.device_count())  # 应该至少返回1
        print("cuda device_name", torch.cuda.get_device_name(0))  # 应该显示您的GPU名称
    except Exception:
        print("显卡驱动不适配，请根据readme安装合适版本的 torch！")


    server_process = subprocess.Popen(
        ["python", "./omniserver.py"],
        stdout=subprocess.PIPE,  # 捕获标准输出
        stderr=subprocess.PIPE,
        text=True
    )


    try:
        # 下载权重文件
        download_weights.download()
        print("启动Omniserver服务中，约5分钟左右，因为加载模型真的超级慢，请耐心等待！")
        # 等待 server_process 打印出 "Started server process"
        while True:
            res = requests.get("http://127.0.0.1:8000/probe/")
            if res.status_code == 200 and res.json().get("message", None):
                print("Omniparser服务启动成功...")
                break
            if server_process.poll() is not None:
                raise RuntimeError("Server process terminated unexpectedly")
            time.sleep(5)
        
        stdout_thread = Thread(
            target=stream_reader,
            args=(server_process.stdout, "SERVER-OUT")
        )

        stderr_thread = Thread(
            target=stream_reader,
            args=(server_process.stderr, "SERVER-ERR")
        )
        stdout_thread.daemon = True
        stderr_thread.daemon = True
        stdout_thread.start()
        stderr_thread.start()
        app.run()
    finally:
        if server_process.poll() is None:  # 如果进程还在运行
            server_process.terminate()  # 发送终止信号
            server_process.wait(timeout=8)  # 等待进程结束

def stream_reader(pipe, prefix):
    for line in pipe:
        print(f"[{prefix}]", line, end="", flush=True)

def is_port_occupied(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0
    
if __name__ == '__main__':
    # 检测8000端口是否被占用
    if is_port_occupied(8000):
        print("8000端口被占用，请先关闭占用该端口的进程")
        exit()
    run()