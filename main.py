from gradio_ui import app
import os
from util import download_weights
os.environ["GRADIO_ANALYTICS_ENABLED"] = "False"
def run():
    download_weights.download() 
    app.run()


if __name__ == '__main__':
    run()