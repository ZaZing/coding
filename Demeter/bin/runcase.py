# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : runcase.py
# Time       ：2021/8/22 19:17
# Author     ：zcding
# Description：读取yaml中测试用例，并执行输出执行结果到html文件
"""
from util.configparser import Reader
from util.log import Logger
from util.hive import HiveKeywords
import os,io
import ruamel.yaml as yaml

class RunCase(object):
    def __init__(self):
        self.last_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        _logfile = os.path.join(self.last_path, "run.log")
        self.mylog = Logger(path=_logfile)
        self.testcase = os.path.join(self.last_path,"testcase","testcase.yaml")
        _conffile = os.path.join(self.last_path,"common.conf")
        self.cf = Reader(_conffile)
        self.hive = HiveKeywords()
        self._hive_init()


    def _hive_init(self):
        """
        :return:
        """
        hiveserver = self.cf.get_items_by_section("server_info")
        port = self.cf.get_items_by_section("port")
        user = self.cf.get_items_by_section("user")
        password = self.cf.get_items_by_section("password")
        self.con = self.hive.connect(hiveserver,port,user,password)

    def excutecase(self):
        """
        根据yaml文件执行测试case
        :param case:
        :return:
        """
        with io.open(self.testcase,"r",encoding= "utf-8") as f:
            testcases = yaml.load(f)
        print testcases
        for tablename in testcases.keys():
            self.mylog.info("开始执行{}的测试用例".format(tablename))
            for each in testcases[tablename].keys():
                self.mylog.info("开始执行{}".format(each))
                sql = each["case_execute"]
                res = self.hive.hive_query_list(sql)
                testcases[tablename][each]["actual_res"] = res
        return testcases

    def output(self):
        """
        输出html报告
        :return:
        """

    def compare(self):
        pass

if __name__ == "__main__":
    runcase = RunCase()
    runcase.excutecase()



