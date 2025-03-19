from gradio_ui import app
from util import download_weights

import torch

def run():
    if not torch.cuda.is_available():
        print("Warning: GPU is not available, we will use CPU, the application may run slower!\nyou computer will very likely heat up!")
    app.run()


if __name__ == '__main__':
    run()