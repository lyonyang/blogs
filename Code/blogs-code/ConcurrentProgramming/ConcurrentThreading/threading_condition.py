#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import threading
def condition_func():
    ret = False
    inp = input('>>>')
    if inp == '1':
        ret = True
    return ret
def run(n):
    con.acquire()
    con.wait_for(condition_func)
    print("run the thread: %s" %n)
    con.release()
if __name__ == '__main__':
    con = threading.Condition()
    for i in range(10):
        t = threading.Thread(target=run, args=(i,))
        t.start()