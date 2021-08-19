# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : run.py
# Time       ：2021/8/15 14:58
# Author     ：zcding
# Description：执行主文件
"""

import click

@click.command()
@click.option('--o', '-o', type=click.Choice(['trans', 'runcase', 'getresult', 'all']), default='trans',help='选择操作选项: trans表示转化case，runcase表示执行查询，getresult表示获取结果'.decode('utf-8'))
def run():
    """
    执行主文件
    :return:
    """
    op = o
    excel = 'table.xlsx'
    if op == "trans":
        pass
    elif op == "runcase":
        pass
    elif op == "getresult":
        pass
    elif op == "all":
        pass
    else:
        print("操作选项错误，选择操作选项: trans表示转化case，runcase表示执行查询，getresult表示获取结果")


if __name__ == "__main__":
    run()


