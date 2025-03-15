from gradio_ui import app
from util import download_weights
import torch
import signal
import sys

def signal_handler(*args):
    print("Ctrl+C detected, exiting gracefully...")
    sys.exit(0)

def run():
    try:
        print("cuda is_available: ", torch.cuda.is_available())
        print("MPS is_available: ", torch.backends.mps.is_available())
        print("cuda device_count", torch.cuda.device_count()) 
        print("cuda device_name", torch.cuda.get_device_name(0)) 
    except Exception:
        print("GPU driver is not compatible, please install the appropriate version of torch according to the readme!")

    # download the weight files
    download_weights.download()   
    
    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    app.run()


if __name__ == '__main__':
    run()