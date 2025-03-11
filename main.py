from gradio_ui import app
from util import download_weights
import torch

def run():
    try:
        print("cuda is_available: ", torch.cuda.is_available())  # 应该返回True
        print("MPS is_available: ", torch.backends.mps.is_available())
        print("cuda device_count", torch.cuda.device_count())  # 应该至少返回1
        print("cuda device_name", torch.cuda.get_device_name(0))  # 应该显示您的GPU名称
    except Exception:
        print("显卡驱动不适配，请根据readme安装合适版本的 torch！")

    # 下载权重文件
    download_weights.download()   
    app.run()


if __name__ == '__main__':
    run()