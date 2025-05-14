# 导入主界面模块
from ui.main import main
# 导入权重下载工具
from util import download_weights

def run():
    # 下载必要的模型权重文件
    download_weights.download() 
    # 启动主界面
    main()
    
# 当脚本直接运行时执行run函数
if __name__ == "__main__":
    run()

