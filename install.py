import subprocess
import sys
from util import download_weights

def install_requirements():
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])

def adjust_python_env():
    # check if python is 3.12
    if sys.version_info.major != 3 or sys.version_info.minor != 12:
        print("Python version is not 3.12, please install python 3.12")
        exit(1)

def install():
    adjust_python_env()
    install_requirements()
    # download the weight files
    download_weights.download() 
    print("Installation complete!") 

if __name__ == "__main__":
    install()
    print("Installation complete!") 