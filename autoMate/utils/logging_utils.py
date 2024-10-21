import logging
from logging.handlers import RotatingFileHandler

# 创建logger，如果参数为空则返回root logger
logger = logging.getLogger("root")
logger.setLevel(logging.INFO)  # 设置logger日志等级

# 创建handler
# backupCount=2 表示保留2个备份文件。
fh = RotatingFileHandler("server.log", maxBytes=10*1024*1024, backupCount=2, encoding="utf-8")
ch = logging.StreamHandler()

# 创建单独的错误日志处理器
error_fh = RotatingFileHandler("error.log", maxBytes=10*1024*1024, backupCount=2, encoding="utf-8")
error_fh.setLevel(logging.ERROR)  # 仅记录错误及以上级别的日志

# 设置输出日志格式
formatter = logging.Formatter(
    fmt="%(asctime)s %(name)s %(filename)s %(message)s",
    datefmt="%Y/%m/%d %X"
)

# 为handler指定输出格式，注意大小写
fh.setFormatter(formatter)
ch.setFormatter(formatter)
error_fh.setFormatter(formatter)  # 为错误日志处理器指定格式

# 为logger添加的日志处理器
logger.addHandler(fh)
logger.addHandler(ch)
logger.addHandler(error_fh)  # 添加错误日志处理器

