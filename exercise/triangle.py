# -*- coding: utf-8 -*-
def triangle():
    # 杨辉三角
    # 1
    # 1 2 1
    # 1 3 3 1
    # 1 4 6 4 1
    L = [1]
    while True:
        yield L
        L = [1] + [L[n] + L[n + 1] for n in range(len(L) - 1)] + [1]
        # print (L)

n = 0
for t in triangle():
    print t
    n = n +1
    if n == 10:
        break
