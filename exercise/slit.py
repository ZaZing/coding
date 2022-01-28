# -*- coding: utf-8 -*-
def trim(s):
    # ""空字符直接返回
    if s == "":
        return s
    # 首字符为空，切片后再判断
    elif s[:1] == " ":
        return trim(s[1:])
    # 尾字符为空，切片后在判断
    elif s[-1:] == " ":
        return trim(s[:-1])
    # 其他
    else:
        return s
# 测试:
if trim('hello ') != 'hello':
    print('测试失败!')
elif trim('  hello') != 'hello':
    print('测试失败!')
elif trim('  hello  ') != 'hello':
    print('测试失败!')
elif trim('  hello  world  ') != 'hello  world':
    print('测试失败!')
elif trim('') != '':
    print('测试失败!')
elif trim('    ') != '':
    print('测试失败!')
else:
    print('测试成功!')