# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : excel_util.py
# Time       ：2021/8/17 21:42
# Author     ：zcding
# Description：封装常见excel操作
"""

from __future__ import unicode_literals
import xlrd


class ExcelOperate(object):
    """
    封装常见excel操作
    """
    def __init__(self,excelfile):
        self.excelfile = excelfile
        self.wb = self._openexcel()


    def _openexcel(self):
        """
        读取excel
        :param excelfile: excel文件
        :return:
        """
        try:
            workbook = xlrd.open_workbook(self.excelfile)
        except Exception as e:
            print("打开文件{}错误".format(self.excelfile))
        return  workbook


    def getsheetname(self):
        """
        获取sheet页name
        :return:
        """
        return self.wb.sheet_names()

    def _get_sheet_content(self,sheetname):
        """
        根据sheetname获取页面中数据
        :param sheetname:
        :return:
        """
        if sheetname in self.getsheetname():
            return self.wb.sheet_by_name(sheetname)
        else:
            return None

    def get_sheet_onecell(self, sheetname, rowindex, colindex):
        """
        获取sheet页上单元格内容，合并单元格返回第一格数据
        :param sheetname:
        :param rowindex:
        :param colindex:
        :return:
        """
        _sheet= self._get_sheet_content(sheetname)
        merged = _sheet.merged_cells
        rowindex = int(rowindex) -1
        colindex = int(colindex) - 1
        cell_value = _sheet.cell_value(rowindex, colindex)
        for (rlow,rhigh,clow,chigh) in merged:
            if (rowindex >= rlow and rowindex < rhigh): # 行坐标判断
                if (colindex >= clow and colindex < chigh): # 列坐标判断
                    cell_value = _sheet.cell_value(rlow,clow)
                    break
                else:
                    cell_value = _sheet.cell_value(rowindex, colindex)
        return cell_value

    def get_sheet_rowcontents(self, sheetname, rowindex):
        """
        获取行数据，返回list,超出最大行，返回""
        :param sheetname:
        :param rowindex:
        :return:
        """
        ws = self._get_sheet_content(sheetname)
        rows = self._get_sheet_content(sheetname).nrows
        cols = self._get_sheet_content(sheetname).ncols
        row = int(rowindex) - 1
        row_res =[]
        if row > rows:
            print("当前{}页最大行{}，已超出".format(sheetname,rows+1))
            row_res = list(row_res.append("") for i in range(cols))
        elif row < 0:
            row_res = list(row_res.append("") for i in range(cols))
        else:
            for i in range(cols):
                row_cell = self.get_sheet_onecell(sheetname,row,i)
                row_res.append(row_cell)
        return row_res

    def get_sheet_colcontents(self, sheetname, colindex):
        """
        获取列数据，返回list，超出最大列，返回""
        :param sheetname:
        :param colindex:
        :return:
        """
        ws = self._get_sheet_content(sheetname)
        rows = ws.nrows
        cols = ws.ncols
        col = int(colindex) - 1
        col_res = []
        if col > cols:
            print("当前{}页最大列{}，已超出".format(sheetname,cols))
            col_res = list(col_res.append("") for i in range(rows))
        elif col < 0:
            print("输入列错误")
            col_res = list(col_res.append("") for i in range(rows))
        else:
            for i in range(rows):
                col_cell = self.get_sheet_onecell(sheetname,i,col)
                col_res.append(col_cell)
        return col_res

    def get_sheet_row2(self, sheetname, rlow,rhigh):
        """
        根据行号获取区间内的内容，返回list
        :param sheetname:
        :param rlow:
        :param rhigh:
        :return:
        """
        rlow = int(rlow) - 1
        rhigh = int(rhigh)
        row_res = []
        for row in range(rlow,rhigh):
            res = self.get_sheet_rowcontents(sheetname, row)
            row_res.append(res)
        return row_res

    def get_sheet_cols(self, sheetname, clow, chigh):
        """
        根据列号获取区间内的内容，返回list
        :param sheetname:
        :param clow:
        :param chigh:
        :return:
        """
        clow = int(clow) - 1
        chigh = int(chigh)
        col_res = []
        for col in range(clow,chigh):
            res = self.get_sheet_colcontents(sheetname,col)
            col_res.append(res)
        return col_res

    def get_sheet_by_coordinate(self, sheetname, startrow, startcol, endrow, endcol ,deal = False):
        """
        根据开始结束坐标返回结构化数据，按行返回数据，类型list
        :param sheet_name:
        :param startrow:
        :param startcol:
        :param endrow:
        :param endcol:
        :return:
        """
        nrows = self._get_sheet_content(sheetname).nrows
        ncols = self._get_sheet_content(sheetname).ncols
        startrow = int(startrow) - 1
        startcol = int(startcol) - 1
        endrow = endrow if endrow else nrows
        endcol = endcol if endcol else ncols
        res = []
        for row in range(startrow, endrow):
            row_list = []
            #如果需要处理
            if deal:
                #若首个字段为空，则不读取本行
                if self.get_sheet_onecell(sheetname,row,startcol) is None:
                    break
                else:
                    for col in range(startcol, endcol):
                        cell = self.get_sheet_onecell(sheetname, row, col)
                        row_list.append(cell)
            else:
                for col in range(startcol, endcol):
                    cell = self.get_sheet_onecell(sheetname, row, col)
                    row_list.append(cell)
            res.append(row_list)
        return res

    def merge_contents(self,sheetname):
        """
        返回当前sheet页中合并单元格范围和数字内容，返回为list
        :param sheetname:
        :return:
        """
        wb = self._get_sheet_content(sheetname)
        merge = wb.merged_cells
        res = []
        for (rlow,rhigh,clow,chigh) in merge:
            cell = self.get_sheet_onecell(rlow,clow)
            loaction = [rlow+1, rhigh+1 , clow+1, chigh+1]
            res.append([cell,loaction])
        return res

if  __name__  == "__main__":
    eo = ExcelOperate(r"test.xlsx")
    # print(eo.getsheetname())
    # print(eo._get_sheet_content('testname1'))
    # print(eo.get_sheet_onecell("测试2",3,3),2222)
    # print(eo.get_sheet_rowcontents('测试2',9))
    print(eo.get_sheet_by_coordinate('测试2',startrow=3,startcol=2,endrow=5,endcol=3))






