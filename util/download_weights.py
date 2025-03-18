import os
from pathlib import Path
from modelscope import snapshot_download
__WEIGHTS_DIR = Path("weights")
OMNI_PARSER_MODEL_DIR = os.path.join(__WEIGHTS_DIR, "AI-ModelScope", "OmniParser-v2___0")

def __download_omni_parser():
    # Create weights directory
   
    __WEIGHTS_DIR.mkdir(exist_ok=True)
    
    snapshot_download(
        'AI-ModelScope/OmniParser-v2.0',
        cache_dir='weights'
        )
    
    
def download_models():
    __download_omni_parser()


if __name__ == "__main__":
    download_models()