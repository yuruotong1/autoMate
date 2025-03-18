# import os
# os.environ["HF_ENDPOINT"] = "https://hf-mirror.com/"

from gradio_ui import app
from util import download_weights

import torch

def run():
    if not torch.cuda.is_available():
        print("Warning: GPU is not available, we will use CPU, the application may run slower!\nyou computer will very likely heat up!")
    print("Downloading the weight files...")
    # download the weight files
    # download_weights.download_models()  
    # 配置 HuggingFace 镜像
    # print("HuggingFace mirror configured to use ModelScope registry")
    app.run()


if __name__ == '__main__':
    run()