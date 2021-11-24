# -*- coding:utf-8  -*-
from multiprocessing import Process
import os
"""
multiprocessing模块提供了一个Process类来代表一个进程对象，
"""
def run(name):
    """
    子进程执行的代码
    :return:
    """
    print "Run child process {1} :{2}".format(name, os.getpid())

if __name__ == '__main__':
    from multiprocessing import Process
    print "Parent process is {}".format({os.getpid()})
    p = Process(target = run,args= ("test",))
    print "Child process will start"
    p.start()
    p.join()
    print "Child process end"
