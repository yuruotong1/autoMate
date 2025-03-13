import os
from pathlib import Path
from modelscope import snapshot_download
__WEIGHTS_DIR = Path("weights")
MODEL_DIR = os.path.join(__WEIGHTS_DIR, "AI-ModelScope", "OmniParser-v2___0")
def download():
    # Create weights directory
   
    __WEIGHTS_DIR.mkdir(exist_ok=True)
    
    # List of files to download
    files = [
        "icon_detect/train_args.yaml",
        "icon_detect/model.pt",
        "icon_detect/model.yaml",
        "icon_caption/config.json",
        "icon_caption/generation_config.json",
        "icon_caption/model.safetensors"
    ]
    
    # Check and download missing files
    missing_files = []
    for file in files:
        file_path = os.path.join(MODEL_DIR, file)
        if not os.path.exists(file_path):
            missing_files.append(file)
            break
    
    if not missing_files:
        print("Model files already detected!")
        return
    
    snapshot_download(
        'AI-ModelScope/OmniParser-v2.0',
        cache_dir='weights'
        )

    print("Download complete")

if __name__ == "__main__":
    download()