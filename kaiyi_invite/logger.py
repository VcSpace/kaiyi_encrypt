import logging
import os
import time

logger = logging.getLogger()

def setlog():
    path = "./logs/"
    isExists = os.path.exists(path)
    if not isExists:
        os.mkdir(path)
    logger.setLevel(logging.INFO)
    log_time = time.strftime("%Y_%m_%d", time.localtime())  # 刷新
    logfile = path + log_time + ".log"
    if os.path.exists(logfile):
        log_time = time.strftime("%Y_%m_%d_%H_%M", time.localtime())  # 刷新
        logfile = path + log_time + "分.log"
    fh = logging.FileHandler(logfile, mode='w')
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

setlog()