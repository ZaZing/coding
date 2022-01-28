# -*- coding:utf-8 -*-

def normalize(name):
    alphabet_l = {"A": "a", "B":"b", "C": "c", "D": "d", "E": "e", "F": "f","a":"a","m":"m","d":"d"}
    alphabet_u = {"a":"A"}
    def lower(s):
        return alphabet_l[s]
    def upper(s):
        return alphabet_u[s]
    rs = [upper(name[:1])]+ list(map(lower,name[1:]))
    return "".join(rs)

def prod(L):
    def mul(x,y):
        return x * y
    return reduce(mul,L)

print prod([1,3,5,7])
print normalize("adam")