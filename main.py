from ui.main import main
from util import download_weights
def run():
    download_weights.download() 
    main()
    
if __name__ == "__main__":
    run()

