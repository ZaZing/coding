# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : transecase.py
# Time       ：2021/8/15 14:57
# Author     ：zcding
# Description：读取excel转换成testcase
"""

from __future__ import unicode_literals
import os,sys
sys.path.append("..")
from util.excel_util import ExcelOperate
from util.log import Logger


class TransCase():
    """
    读取excel转换成yaml格式的testcase
    """
    def __init__(self, excel):
        last_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        self.excelfile = os.path.join(last_path,"testcase",excel)
        _logfile = os.path.join(last_path,"run.log")
        self.workbook = ExcelOperate(self.excelfile)
        self.mylog = Logger(path=_logfile)

    def trans_summry(self):
        sheetnames = self.workbook.getsheetname()
        if "汇总" not in sheetnames:
            self.mylog.error("excel{}内容错误，缺少第一页【汇总】页".format(self.excelfile))
        else:
            self.mylog.info("开始读取【汇总】页")
            content = self.workbook.get_sheet_colcontents("汇总",2)
        return content

    def trans_sheet(self,sheetname):
        tableindex = self.findindex(sheetname)
        tablename = tableindex.get("dwd",None)[1]
        startcol = tableindex.get("dwd",None)[0][2]
        startrow = tableindex.get("dwd",None)[0][1] + 1
        tablecase = {}
        content_list = self.workbook.get_sheet_by_coordinate(sheetname=sheetname,
                                                             startrow=int(startrow) + 1,
                                                             startcol=startcol,
                                                             endcol= int(startcol) + 10,
                                                             deal= True)
        for each in content_list:
            #字段名称	字段类型	备注	映射关系	完整性	有效性	唯一性	一致性	及时性	准确性
            tablecase[tablename]["字段名称"] = each[0]
            tablecase[tablename]["字段类型"] = each[1]
            tablecase[tablename]["备注"] = each[2]
            tablecase[tablename]["映射关系"] = each[3]
            tablecase[tablename]["完整性"] = self.generate_sql(tablename,each[0],each[4],key = '完整性')



        pass
        # for sheetname in sheetnames:

    def generate_sql(self,tablename,field,status,key):
        """
        根据状态值，生成对应的字段sql
        :param tablename:
        :param field:
        :param status:
        :return:
        """
        tablename,field,status,key = tablename,field,status,key
        if key == "完整性":
            sql = "select count(*) from {TABLENAME } where {FIELD} is not null or {FIELD} == ''".format(TABLENAME= tablename,FIELD = field) if status == "1" else None

            elif key == "唯一性":
            sql = "select {FIELD},count({FIELD}) from {TABLENAME} group by {FIELD} having count(*) > 1 limit 10".format(TABLENAME = tablename,FIELD = field) if status == "1" else None
        elif key =="有效性":
            sql = "select {FIELD},count({FIELD}) from {TABLENAME} group by {FIELD}".format(TABLENAME = tablename,FIELD = field) if status == "1" else None

        return sql

    def findindex(self,sheetname):
        """
        根据关键词，找出对应的单元格起始位置
        :param sheetname:
        :return:
        """
        keywords = ["ods","pre","dwd","dim"]
        merge = self.workbook.merge_contents(sheetname)
        index = {}
        for each in merge:
            tmp = str(each[0]).lower()
            tablename = tmp.split(":")[-1]
            table = [each[1],tablename]
            if keywords[0] in tmp:
                index["ods"] = table
            elif keywords[1] in tmp:
                index["pre"] = table
            elif keywords[3] in tmp:
                index["dim"] = table
            elif (keywords[2] in tmp and keywords[1] not in tmp): #dwd层数据额外处理，pre、dwd都包含dwd层数据
                index["dwd"] = table
        return index











if __name__ == "__main__":
    trans = TransCase("test.xlsx")