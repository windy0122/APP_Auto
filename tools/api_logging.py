import logging
from tools.project_path import *
from logging.handlers import RotatingFileHandler


# 根据指定log文件，每次追加在后方
fmt = "%(asctime)s %(filename)s %(funcName)s [line:%(lineno)d] %(message)s"
datefmt = "%a, %d %b %Y %H:%M:%S"
handler_1 = logging.StreamHandler()

handler_2 = RotatingFileHandler(test_log_path, backupCount=20, encoding='utf-8')

logging.basicConfig(format=fmt, datefmt=datefmt, level=logging.INFO, handlers=[handler_1, handler_2])

# logging.info('heheheh1')
# logging.error('hahahah1')


# class MyLog(object):
#     @staticmethod
#     def my_log(msg, level):
#         # logging.debug('我是debug')
#         # logging.info('我是info')
#         # logging.warning('我是warning')
#         # logging.error('我是error')
#         # logging.critical('我是critical')
#
#         # 定义一个日志收集器
#         my_logger = logging.getLogger('logging')
#
#         # 设定级别
#         my_logger.setLevel('DEBUG')     # 级别一定要大写
#
#         # 设定日志输入格式
#         formatter = logging.Formatter("%(asctime)s %(filename)s %(funcName)s [line:%(lineno)d] \
#         - %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S")
#
#         # 创建一个输出渠道
#         ch = logging.StreamHandler()
#         ch.setLevel('ERROR')    # 双重筛选，不显示error级别以下的
#         ch.setFormatter(formatter)
#         fh = logging.FileHandler(test_log_path, encoding='utf-8')
#         fh.setLevel('DEBUG')
#         fh.setFormatter(formatter)
#
#         # 对接 -- 指定输出渠道
#         my_logger.addHandler(ch)
#         my_logger.addHandler(fh)
#
#         # 收集日志
#         if level == 'DEBUG':
#             my_logger.debug(msg)
#         elif level == 'INFO':
#             my_logger.info(msg)
#         elif level == 'ERROR':
#             my_logger.error(msg)
#         elif level == 'WARNING':
#             my_logger.warning(msg)
#         elif level == 'CRITICAL':
#             my_logger.critical(msg)
#
#         # 关闭日志收集
#         my_logger.removeHandler(ch)
#         my_logger.removeHandler(fh)
#
#     def debug(self, msg):
#         self.my_log(msg, 'DEBUG')
#
#     def info(self, msg):
#         self.my_log(msg, 'INFO')
#
#     def error(self, msg):
#         self.my_log(msg, 'ERROR')
#
#     def warning(self, msg):
#         self.my_log(msg, 'WARNING')
#
#     def critical(self, msg):
#         self.my_log(msg, 'CRITICAL')


# if __name__ == '__main__':
#     # MyLog().my_log('哈哈哈', 'ERROR')
#     # MyLog().my_log('呵呵呵', 'INFO')
#     # MyLog().my_log('嘻嘻嘻', 'WARNING')
#     MyLog().error('哈哈哈')
#     MyLog().info('呵呵呵')
#     MyLog().warning('嘻嘻嘻')
