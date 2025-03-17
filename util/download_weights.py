import os
from pathlib import Path
from modelscope import snapshot_download
__WEIGHTS_DIR = Path("weights")
OMNI_PARSER_MODEL_DIR = os.path.join(__WEIGHTS_DIR, "AI-ModelScope", "OmniParser-v2___0")
FLORENCE_MODEL_DIR = os.path.join(__WEIGHTS_DIR, "AI-ModelScope", "Florence-2-base-ft")

def __download_omni_parser():
    # Create weights directory
   
    __WEIGHTS_DIR.mkdir(exist_ok=True)
    
    snapshot_download(
        'AI-ModelScope/OmniParser-v2.0',
        cache_dir='weights'
        )

def __download_florence_model():
    snapshot_download('AI-ModelScope/Florence-2-base-ft',
                      cache_dir='weights'
                      )

def download_models():
    __download_omni_parser()
    __download_florence_model()

if __name__ == "__main__":
    download_models()