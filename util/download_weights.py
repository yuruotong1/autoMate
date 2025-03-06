import subprocess
from pathlib import Path

def download():
    # 创建权重目录
    weights_dir = Path("weights")
    weights_dir.mkdir(exist_ok=True)
    
    # 需要下载的文件列表
    files = [
        "icon_detect/train_args.yaml",
        "icon_detect/model.pt",
        "icon_detect/model.yaml",
        "icon_caption/config.json",
        "icon_caption/generation_config.json",
        "icon_caption/model.safetensors"
    ]
    
    # 检查并下载缺失的文件
    missing_files = []
    for file in files:
        file_path = weights_dir / file
        if not file_path.exists():
            missing_files.append(file)
    
    if not missing_files:
        print("已经检测到模型文件！")
        return
    
    print(f"未检测到模型文件，需要下载 {len(missing_files)} 个文件")
    # 下载缺失的文件
    max_retries = 3  # 最大重试次数
    for file in missing_files:
        for attempt in range(max_retries):
            try:
                print(f"正在下载: {file} (尝试 {attempt + 1}/{max_retries})")
                cmd = [
                    "huggingface-cli",
                    "download",
                    "microsoft/OmniParser-v2.0",
                    file,
                    "--local-dir",
                    "weights"
                ]
                subprocess.run(cmd, check=True)
                break  # 下载成功，跳出重试循环
            except subprocess.CalledProcessError as e:
                if attempt == max_retries - 1:  # 最后一次尝试
                    print(f"下载失败: {file}，已达到最大重试次数")
                    raise  # 重新抛出异常
                print(f"下载失败: {file}，正在重试...")
                continue
    
    print("下载完成")

if __name__ == "__main__":
    download()