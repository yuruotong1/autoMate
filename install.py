import subprocess
import os
import sys

from util import download_weights

def check_cuda_version():
    try:
        # try to get cuda version from nvidia-smi
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if 'CUDA Version:' in line:
                cuda_version = line.split('CUDA Version:')[1].strip()
                return cuda_version
        
        # try to get cuda version from nvcc
        result = subprocess.run(['nvcc', '--version'], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if 'release' in line:
                version = line.split('V')[-1].split('.')[0:2]
                return '.'.join(version)
        
        return None
    except:
        return None

def install_pytorch():
    cuda_version = check_cuda_version()
    if cuda_version is None:
        print("CUDA not found. Installing CPU version of PyTorch")
        cmd = "pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu --timeout 3000"
    elif cuda_version.startswith("11."):
        print(f"CUDA {cuda_version} found. Installing PyTorch for CUDA 11.8")
        cmd = "pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118 --timeout 3000"
    elif cuda_version.startswith("12.4"):
        print(f"CUDA {cuda_version} found. Installing PyTorch for CUDA 12.4")
        cmd = "pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124 --timeout 3000"
    elif cuda_version.startswith("12.6"):
        print(f"CUDA {cuda_version} found. Installing PyTorch for CUDA 12.6")
        cmd = "pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126 --timeout 3000"
    else:
        print(f"CUDA {cuda_version} found, but not in 11.8, 12.4, 12.6, please reinstall cuda and try again")
        exit(1)
    
    print(f"Running: {cmd}")
    subprocess.run(cmd, shell=True)

def install_requirements():
    # create a temporary requirements file, excluding torch and torchvision
    with open('requirements.txt', 'r') as f:
        requirements = f.readlines()
    
    # filter out torch and torchvision
    filtered_requirements = [req for req in requirements 
                           if not req.strip().startswith('torch') 
                           and not req.strip().startswith('torchvision')]
    
    with open('temp_requirements.txt', 'w') as f:
        f.writelines(filtered_requirements)
    
    # install other dependencies
    print("Installing other dependencies...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'temp_requirements.txt'])
    
    # delete temporary file
    os.remove('temp_requirements.txt')

def adjust_python_env():
    # check if python is 3.12
    if sys.version_info.major != 3 or sys.version_info.minor != 12:
        print("Python version is not 3.12, please install python 3.12")
        exit(1)


def install():
    adjust_python_env()
    install_pytorch()
    install_requirements()
    # download the weight files
    download_weights.download() 
    print("Installation complete!") 

if __name__ == "__main__":
    install()
    print("Installation complete!") 