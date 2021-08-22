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
import ruamel.yaml as yaml
from ruamel.yaml.comments import CommentedMap, CommentedSeq


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

    def read_sheet(self,sheetname):
        self.mylog.info("开始读取sheet页{}".format(sheetname))
        tableindex = self.findindex(sheetname)
        tablename = tableindex.get("dwd",None)[1]
        # 合并单元格第一列
        startcol = tableindex.get("dwd",None)[0][2]
        # 合并单元格最后一行+1
        startrow = tableindex.get("dwd",None)[0][1]
        content_list = self.workbook.get_sheet_by_coordinate(sheetname=sheetname,
                                                             startrow=int(startrow)+1 ,
                                                             startcol=startcol,
                                                             endcol= int(startcol) + 10,
                                                             deal= False)
        #todo:表格中存在列的合并，取值时应按照正常字段来取（单元格除第一个返回数据外，其他返回空），后续在做判断
        pretablecase = {}
        pretablecase[tablename] = {}
        for each in content_list:
            #字段名称	字段类型	备注	映射关系	完整性	有效性	唯一性	一致性	及时性	准确性
            key = ["字段类型","备注","映射关系","完整性","有效性","唯一性","一致性","及时性","准确性"]
            if each[0]:
                tmp = {}
                for i in range(len(key)):
                    tmp[key[i]] = each[i+1]
                pretablecase[tablename][each[0]] = tmp
            self.mylog.debug("{}字段".format(each[0]))
        # 生成测试sql
        # 所有表均包含表结构比对
        # 表结构检查
        global case_no
        case_no = 0
        tablecase = {}
        tablecase[tablename] = {}
        for i in pretablecase.keys():
            self.mylog.info("开始生成{}测试sql".format(i))
            case_field = {}
            # todo:case_number 自动生成
            case_number = "testcase_"+ str(case_no)
            case_no = case_no + 1
            case_tablename = str(i)
            case_field["case_name"] = "{}表结构对比测试".format(i)
            case_field["case_author"] = "zcding"
            case_field["case_expect"] = {}
            for each in pretablecase[i].keys():
                case_field["case_expect"][each] = pretablecase[i][each]["字段类型"]
            case_field["case_execute"] = self.structure_compare(tablename = case_tablename)
            self.mylog.debug("{0}字段测试sql为：{1}".format(each,case_field["case_execute"]))
            tablecase[tablename][case_number] = case_field
        # 根据关键词构造测试sql
        for i in pretablecase.keys():
            tablecase[i] = {}
            case_field = {}
            # Todo:后续优化代码结构，此处冗余较多
            for each in pretablecase[i].keys():
                if pretablecase[i][each]["完整性"]:
                    case_number = "testcase_" + str(case_no)
                    case_no = case_no + 1
                    case_field["case_name"] = "{}表{}字段完整性测试".format(i,each);
                    case_field["case_author"] = "zcding"
                    case_field["case_expect"] = ""
                    case_field["case_execute"] = self.generate_sql(tablename=i,field=each,key="完整性")
                    tablecase[tablename][case_number] = case_field
                elif pretablecase[i][each]["及时性"]:
                    case_number = "testcase_" + str(case_no)
                    case_no = case_no + 1
                    case_field["case_name"] = "{}表{}字段及时性测试".format(i,each);
                    case_field["case_author"] = "zcding"
                    # 后续增加时间字段
                    case_field["case_expect"] = ""
                    case_field["case_execute"] = self.generate_sql(tablename=i,field=each,key="及时性")
                    tablecase[tablename][case_number] = case_field
                elif pretablecase[i][each]["唯一性"]:
                    case_number = "testcase_" + str(case_no)
                    case_no = case_no + 1
                    case_field["case_name"] = "{}表{}字段及时性测试".format(i, each);
                    case_field["case_author"] = "zcding"
                    case_field["case_expect"] = "0"
                    case_field["case_execute"] = self.generate_sql(tablename=i, field=each, key="及时性")
                    tablecase[tablename][case_number] = case_field
                else:
                    pass

        print tablecase

        return tablecase

    def generate_sql(self,tablename, field, key):
        """
        根据状态值，生成对应的字段sql
        :param tablename:
        :param field:
        :param status:
        :return:
        """
        sql = None
        tablename,field,key = tablename,field,key
        if key == "完整性":
            sql = "select count(*) from {0} where {1} is not null or {2} == ''".format(tablename,field,field)
        elif key == "唯一性":
            sql = "select {0},count({1}) from {2} group by {3} having count(*) > 1 limit 10".format(field,field,tablename,field)
        elif key =="有效性":
            sql = "select {0},count({1}) from {2} group by {3}".format(field,field,tablename,field)
        elif key == "及时性":
            pass
        elif key == "准确性":
            pass
        elif key == "一致性":
            # 一致性需要手动增加sql，通常表现为a推出b，数据清洗时可以不做关注
            #
            pass


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



    def structure_compare(self,tablename):
        """
        生成desc语句
        :param tablename:
        :return:
        """
        desc_sql = "desc {};".format(tablename)
        return desc_sql












if __name__ == "__main__":
    trans = TransCase("数据清洗测试demo.xlsx")
    summry = trans.trans_summry()
    for each in summry[1:]:
        if  each:
            trans.read_sheet(each)