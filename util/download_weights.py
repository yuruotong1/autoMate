import os
from pathlib import Path
from modelscope import snapshot_download
import subprocess
import shutil
__WEIGHTS_DIR = Path("weights")
MODEL_DIR = os.path.join(__WEIGHTS_DIR, "AI-ModelScope", "OmniParser-v2___0") 
PROCESSOR_DIR = os.path.join(__WEIGHTS_DIR, "AI-ModelScope", "Florence-2-base")
def download():
    # Create weights directory
   
    __WEIGHTS_DIR.mkdir(exist_ok=True)
    
    # List of files to download
    files = [
        "icon_detect/train_args.yaml",
        "icon_detect/model.pt",
        "icon_detect/model.yaml",
        "icon_caption/generation_config.json",
        "icon_caption/model.safetensors",
    ]

    # Extra config files downloaded from Florence2 repo
    config_files = [
        "configuration_florence2.py",
        "modeling_florence2.py"
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
        cache_dir='weights',
        ignore_file_pattern=['config.json']
        )
    
    snapshot_download(
        'AI-ModelScope/Florence-2-base',
        cache_dir='weights',
        allow_file_pattern=['*.py', '*.json']
    )

    # Move downloaded Florence config files into icon_caption
    for file_path in config_files:
        source_dir = os.path.join(PROCESSOR_DIR, file_path)
        dest_dir = os.path.join(MODEL_DIR, "icon_caption", file_path)
        shutil.copy(source_dir, dest_dir)

    # Move customized config.json into icon_caption to load the model from local path
    shutil.copy(os.path.join("util", "config.json"), os.path.join(MODEL_DIR, "icon_caption", "config.json"))
    
    print("Download complete")

if __name__ == "__main__":
    download()