# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from allpairspy import AllPairs


if __name__ == '__main__':
    # 带宽，丢包，延迟
    parameters = [["有C01","无C01"],["有C02","无C02"],["有C03","无C03"],["有C07","无C07"]]
    # 设置组合因子n的数目，默认为2
    pairwise = AllPairs(parameters, n=2)
    for i, v in enumerate(pairwise):
        print("%i:\t%s" % (i, str(v).decode('utf-8')))
    # parameters2 = [["有C03","无C03"],["有C02","无C02"],["有C01","无C01"]]
    # pairwise2 = AllPairs(parameters2, n=2)
    # for i, v in enumerate(pairwise2):
    #     print("%i:\t%s" % (i, str(v).decode('utf-8')))
    # combine = set(pairwise)&set(pairwise2)
    # print combine,111