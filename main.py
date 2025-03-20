from gradio_ui import app
import torch
import os
from util import download_weights
os.environ["GRADIO_ANALYTICS_ENABLED"] = "False"
def run():
    if not torch.cuda.is_available():
        print("Warning: GPU is not available, we will use CPU, the application may run slower!\nyou computer will very likely heat up!")
    download_weights.download() 
    app.run()


if __name__ == '__main__':
    run()