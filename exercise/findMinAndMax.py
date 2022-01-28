# -*- coding: utf-8 -*-
def findMinAndMax(L):
    if not L:
        return (None,None)
    else:
        _min = L[0]
        _max = L[0]
        for each in L:
            if each < _min:
                _min = each
            if each > _max:
                _max = each
        return (_min,_max)
if findMinAndMax([]) != (None, None):
    print('测试失败!')
elif findMinAndMax([7]) != (7, 7):
    print('测试失败!')
elif findMinAndMax([7, 1]) != (1, 7):
    print('测试失败!')
elif findMinAndMax([7, 1, 3, 9, 5]) != (1, 9):
    print('测试失败!')
else:
    print('测试成功!')
def triangle():
    # 杨辉三角
    # 1
    # 1 2 1
    # 1 3 3 1
    # 1 4 6 4 1
    L = [1]
    while True:
        yield  L
        L = L[0] + [
            L[n] + L[n-1]  for n in range(len(L)-1)] + L[-1]
# n =0
# for t in triangle():
#     print triangle()
#     n = n + 1




