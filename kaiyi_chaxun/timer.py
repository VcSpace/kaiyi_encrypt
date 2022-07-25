# -*- coding:utf-8 -*-
import time
import sys

from datetime import datetime
from logger import logger
# from config import global_config



class Timer(object):
    def __init__(self, sleep_interval=0.2):
        # '2018-09-28 22:45:50.000'
        # self.start_time = datetime.strptime(global_config.getRaw('config','buy_time'), "%Y-%m-%d %H:%M:%S.%f")
        # self.ready_time = datetime.strptime(global_config.getRaw('config','ready_time'), "%Y-%m-%d %H:%M:%S.%f")
        # self.end_time = datetime.strptime(global_config.getRaw('config','end_time'), "%Y-%m-%d %H:%M:%S.%f")
        self.ready_time = datetime.strptime('2022-06-23 19:29:50.500', "%Y-%m-%d %H:%M:%S.%f")
        self.use_time = datetime.strptime('2022-09-27 20:05:00.000', "%Y-%m-%d %H:%M:%S.%f")
        self.start_time = datetime.strptime('2022-06-23 19:29:59.100', "%Y-%m-%d %H:%M:%S.%f")
        self.sleep_interval = sleep_interval

    def ready(self):
        logger.info('正在等待到达设定时间:%s' % self.ready_time)
        now_time = datetime.now
        while True:
            if now_time() >= self.ready_time:
                logger.info('准备开始执行……')
                break
            else:
                time.sleep(self.sleep_interval)

    def start(self):
        now_time = datetime.now
        while True:
            if now_time() >= self.start_time:
                logger.info('时间到达，开始执行……')
                break
            else:
                time.sleep(self.sleep_interval)

    # def end(self):
    #     now_time = datetime.now
    #     while True:
    #         if now_time() < self.end_time:
    #             return True
    #         else:
    #             break
    #     return False

    def use(self):
        now_time = datetime.now
        while True:
            if now_time() < self.use_time:
                return True
            else:
                print('测试期限已过')
                time.sleep(3)
                sys.exit()



