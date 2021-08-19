#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import unicode_literals
import logging
import inspect


# 取log打印所在位置函数
def get_current_function_name():
    stack = inspect.stack()
    len_stack = len(stack)
    log_name = ''
    line = ''
    if len_stack == 4:
        log_name = inspect.stack()[-1][1]
        line = str(inspect.stack()[-1][2])
    elif len_stack == 5 or len_stack == 6:
        log_name = inspect.stack()[-2][1]
        line = str(inspect.stack()[-2][2])
    if log_name != None and line != None:
        loglist = [log_name, line]
        head = ':'.join(loglist)
        return head
    return log_name


# 颜色函数
def _wrap_with(code):
    def inner(text, bold=False):
        c = code
        if bold:
            c = "1;%s" % c
        return "%s[%sm%s%s[0m" % (chr(27),c, text,chr(27))
    return inner


red = _wrap_with('31')
green = _wrap_with('32')
yellow = _wrap_with('33')
blue = _wrap_with('34')
magenta = _wrap_with('35')  # 粉色
cyan = _wrap_with('36')  # 天蓝色
white = _wrap_with('37')  # 灰白色


class Logger:
    # todo: 定义日志与 spark日志不兼容 后期需要调整
    def __init__(self, path=None, log_name=None, log_print=None, Flevel=logging.INFO, Slevel=logging.INFO):
        """
        #根据需要自定义输出日志,有五种级别，分别是DEBUG-->INFO-->WARNING-->ERROR-->CRITICAL
        :param path: 输出到日志文件,如果不填，则只在屏幕打印结果,如果需要写多份日志，只要多次初始化该类即可
        :param log_name: 如果需要写多分日志，而且彼此独立，互不影响，再新实例化一个类时需要重新给log_name赋值
        :param Slevel: 屏幕打印设置
        :param Flevel: 定义写入日志中的内容，logging.DEBUG表示写入日志的是logging.DEBUG级别以上的，级别顺序为 CRITICAL>ERROR>WARNING>INFO>DEBUG>NOTSET
        :return:
        """
        self.path = path
        self.logname = log_name
        self.root = logging.getLogger(self.logname)
        self.rootfmt = logging.Formatter('[%(asctime)s]  [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        self.fmt2 = logging.Formatter('[%(name)s] [%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        if log_print == 1:
            self.rootfmt = self.fmt2

        self.root.setLevel(0)
        if self.path:
            self.file_root = logging.FileHandler(self.path, 'a+')
            self.file_root.setLevel(Flevel)
            self.file_root.setFormatter(self.rootfmt)
            if not self.root.handlers:
                self.root.addHandler(self.file_root)
            else:
                self.root.handlers[0] = self.file_root
        if len(self.root.handlers) <= 1:
            self.stream_root = logging.StreamHandler()
            self.stream_root.setFormatter(self.rootfmt)
            self.stream_root.setLevel(Slevel)
            self.root.addHandler(self.stream_root)

    def __getLogger(self):
        if not self.logname:
            log_name = get_current_function_name()
            logger = logging.getLogger(log_name)
            logger.setLevel(10)
            return logger
        else:
            logger = logging.getLogger(self.logname)
            logger.setLevel(10)
            return logger

    def debug(self, message):
        """正常运行打印，黑色"""
        self.__getLogger().debug(message)

    def info(self, message):
        """运行成功打印，绿色"""
        self.__getLogger().info(green(message))

    def warning(self, message):
        """警告提示，黄色"""
        self.__getLogger().warning(yellow(message))

    def error(self, message, log_print=None):
        """错误提示，红色,当fmt为1时，打印错误信息位置"""
        if log_print == 1:
            self.file_root.setFormatter(self.fmt2)
            self.root.addHandler(self.file_root)
            self.stream_root.setFormatter(self.fmt2)
            if len(self.root.handlers) == 2:
                self.root.handlers[1] = self.stream_root
        self.__getLogger().error(red(message))

    def critical(self, message, log_print=None):
        """严重错误，红色"""
        if log_print == 1:
            self.file_root.setFormatter(self.fmt2)
            self.root.addHandler(self.file_root)
            self.stream_root.setFormatter(self.fmt2)
            if len(self.root.handlers) == 2:
                self.root.handlers[1] = self.stream_root
        self.__getLogger().critical(red(message))

    def exception(self, message, log_print=None):
        """严重错误，红色, 打印回溯回溯"""
        if log_print == 1:
            self.file_root.setFormatter(self.fmt2)
            self.root.addHandler(self.file_root)
            self.stream_root.setFormatter(self.fmt2)
            if len(self.root.handlers) == 2:
                self.root.handlers[1] = self.stream_root
        self.__getLogger().exception(red(message))


# 使用方法
if __name__ == '__main__':
    ilog = Logger(r'../log/test.log','aaa',Flevel=logging.DEBUG)  # 如果不需要写入文件，则此日志路径不需要填写
    ilog.debug(u'一个debug信息test')
    ilog.info('一个info信息test')
    ilog.warning('一个warning信息test')
    ilog.error('一个error信息test',log_print=1)
    ilog2 =  Logger(r'../log/test2.log','bb',Flevel=logging.DEBUG)
    ilog2.debug(u'一个debug信息test2')
    ilog2.info('一个info信息test2')
    ilog.info('一个info信息test')
    # ilog2.root.handlers[0] = ilog2.root.handlers[0]
    # print(type(ilog2.root.handlers[0]))
    # print(type(ilog2.root.handlers[1]))
    # ilog2.root.handlers[0] = ilog2.root.handlers[1]
    # print(8, ilog2.root.handlers)
    # if isinstance(ilog2.root.handlers[1],logging.FileHandler):
    #     print('is filehander')
    # if isinstance(ilog2.root.handlers[1],logging.StreamHandler):
    #     print('is streamhander')
