# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : hive.py
# Time       ：2021/8/15 10:23
# Author     ：zcding
# Description：hive数据库连接
"""

from __future__ import unicode_literals
import jaydebeapi
import traceback
import os



class HiveKeywords(object):
    """
    Hive连接查询
    """
    def __init__(self):
        self.cursor = None
        self.conn = None
        #todo:确认set role admin 的使用方式

    def connect(self,url,port,user,password,jarpathlist=None):
        """
        通过jdbc方式连接hive数据库
        :param url:
        :param port:
        :param user:
        :param password:
        :param jarpathlist:
        :return:
        """
        url = 'jdbc:hive2://{url}:{port}/default'.format(url=url, port=int(port))
        driver = 'org.apache.hive.jdbc.HiveDriver'
        if not jarpathlist:
            jar1 = os.path.join(os.path.dirname(__file__),'hadoop-common-2.6.2.jar')
            jar2 = os.path.join(os.path.dirname(__file__), 'hive-jdbc-1.2.1-standalone.jar')
            jar_List = [jar1, jar2]
        else:
            jar_List = jarpathlist
        self.conn = jaydebeapi.connect(driver,url,[user,password],jar_List)
        self.cursor = self.conn.cursor()
		self.cursor.execute("set role admin;")


    def hive_execute_sql(self,sql):
        """
        执行sql语句，不返回结果
        :param sql:
        :return:
        """
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print(traceback.format_exc())
        else:
            return True

    def hive_query_list(self,sql):
        """
        查询hive，返回list结果
        :param sql:
        :return:
        """
        if self.hive_execute_sql(sql):
            query_result = self.cursor.fetchall()
            return  query_result

    def hive_query_dict(self,sql):
        """
        查询hive，返回dict结果
        :param sql:
        :return:
        """
        if self.hive_execute_sql(sql):
            desc = self.cursor.description
            query_result = [dict(zip([col[0].upper() for col in desc], row)) for row in self.cursor.fetchall()]
            return query_result


    def load_data(self):
        pass


    def hive_disconnect(self):
        """
        断开数据库连接
        :return:
        """
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    hive = HiveKeywords()
    hive.connect()
