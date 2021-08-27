# -*- coding: utf-8 -*-
from datetime import *
import random,os,copy,time
import itertools


class utils2(object):
    """

    """
 #1、笛卡尔积 对参数分组全排列
    def product(self,allparams):
        newlist = []
        for x in eval('itertools.product'+str(tuple(allparams))):
            newlist.append(x)
        print newlist

        return newlist

     #2、对笛卡尔积处理后的二维原始数据进行N配对处理，得到Pairwise计算之前的数据
    def get_pairslist(self,productedlist,pairlen):
        pwlist = []
        for i in productedlist:
             subtemplist = []
             for sublista in itertools.combinations(i,pairlen):
                 subtemplist.append(sublista)
             pwlist.append(subtemplist)
        return pwlist

     #3、进行Pirwise算法计算
    def pairwise(self,allparams,pairlen):
         productedlist=self.product(allparams)   #productedlist笛卡尔积全排列组合的测试用例
         self.pprint(productedlist)
         print ('笛卡尔积全排列组合数量：',len(productedlist),'--'*11)
         listb = self.get_pairslist(productedlist,pairlen)   #listb:对测试用例结对拆分后的二维列表
         sublistlen = len(listb[1])  #sublistlen:每个测试用例拆分后一维列表长度
         flag = [0]*sublistlen       #一条测试用例拆分后，每个结对在二维列表同位置上是否有相
                                     #同值，其标识列表为flag,flag长度根据sublistlen改变
         templistb = copy.deepcopy(listb)#【有效组】的原始值与listb相同
         delmenu = []    #无效测试用例编号列表
         holdmenu=[]     #有效测试用例编号列表
         # self.pprint (listb)
         print ('--'*7,'有效测试用例计算结果','--'*7)
         for cow in listb:           #一维遍历，等同于二维数组按照行遍历
             for column in cow:      #二维遍历，等同二维数组中任意一行按照‘列’横向遍历
                 for templistbcow in templistb:      #【有效组=templistb】中按照行，从上至下遍历
                     Xa = cow.index(column)          #待校验元素的横坐标
                     Ya = listb.index(cow)           #待校验元素的纵坐标
                     #有效组中行不能是当前要对比元素所在的行，
                     #且带对比元素与【有效组】的行templistbcow中的坐标Xa元素相同，
                     #则认为对比成功，跳出第三层for循环。
                     if templistbcow != cow and column == templistbcow[Xa]:
                         # print (column,'===>' ,templistbcow[Xa],'相等了。。。')
                         flag[Xa] = 1   #1表示对比成功
                         break
                     else: #对比不成功，需要继续第三层for循环对比
                         # print (column,'===>' ,templistbcow[Xa],'不不不等了。。。')
                         flag[Xa] = 0   #0表示对比不成功
             # print ('下标%d,子元素 %s 双匹配对比结果flag:%s'%(listb.index(cow),cow,flag))
             if 0 not in flag:    #如果对比列表中都是1，表明该行的所有结对都在同列的对应位置找到了
                 num = listb.index(cow)
                 delmenu.append(num)     #记录该无用用例所在总列表listb中的位置
                 templistb.remove(cow)   #有效组中删除该无用用例，保持有效性
                 # print ('下标为%d行应删除,内容=%s,'%(num,cow))
                 # print ('delmenu:',delmenu)
             else:  #如果有0出现在对比列表flag中，则表示该行所有结对组并未全在同列对应位置找到，此用例为有效用例应保留
                 num2 = listb.index(cow)
                 holdmenu.append(num2)     #记录有效用例在总列表listb中的坐标
                 # print ('---------------下标为%d行应保留,内容=%s'%(num2,cow))
                 # print('holdmenu=',holdmenu)
             # print ('***'*20)
         print ('保留元素列表：%s \n匹配重复元素列表：%s'%(holdmenu,delmenu))
         return self.pwresult(productedlist,holdmenu)

    def pwresult(self,slist,holdmenu):
         holdparamslist = []
         for  item in holdmenu:
             holdparamslist.append(slist[item])
         return holdparamslist

    def pprint(self,list):
         for item in list:
             print ('line %d:'%(list.index(item)+1),item)

if __name__ == '__main__':
    u2 = utils2()
    allparams=[["有C01","无C01"],["有C02","无C02"],["有C03","无C03"]]
    finallist = u2.pairwise(allparams,4)
    print('最终保留测试用例个数：%d 个'%(len(finallist)))
    u2.pprint(finallist)
