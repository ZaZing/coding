# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : runcase.py
# Time       ：2021/8/22 19:17
# Author     ：zcding
# Description：读取yaml中测试用例，并执行输出执行结果到html文件
"""
from util.configparser import  Reader
from util.log import Logger
from util.hive import HiveKeywords
import os

class RunCase(object):
    def __init__(self):
        self.last_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        _logfile = os.path.join(self.last_path, "run.log")
        self.mylog = Logger(path=_logfile)
        _conffile = os.path.join(self.last_path,"common.conf")
        self.cf = Reader(_conffile)
        self.hive = HiveKeywords()



    def hive_init(self):
        """
        :return:
        """
        hiveserver = self.cf.get_items_by_section("server_info")
        port = self.cf.get_items_by_section("port")
        user = self.cf.get_items_by_section("user")
        password = self.cf.get_items_by_section("password")
        self.con = self.hive.connect(hiveserver,port,user,password)
        return self.con

    def runcase(self,case):
        """
        根据yaml文件执行测试case
        :param case:
        :return:
        """
        
if __name__ == "__main__":
    runcase = RunCase()



