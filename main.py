import argparse
from gradio_ui import app
from util import download_weights

def run():
    download_weights.download()
    app.run()


if __name__ == '__main__':
    download_weights.download()
    run()