#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import multiprocessing
# 假定这是你的银行存款:
balance = 0
def change_it(n):
    # 先存后取，结果应该为0:
    global balance
    balance = balance + n
    balance = balance - n
# 创建一把锁

lock = multiprocessing.Lock()

def run_thread(n):
    for i in range(100000):
        # 先要获取锁:
        lock.acquire()
        try:
            # 放心地改吧:
            change_it(n)
        finally:
            # 改完了一定要释放锁:
            lock.release()

if __name__ == '__main__':
    for j in range(10000):
        t1 = multiprocessing.Process(target=run_thread, args=(5,))
        t2 = multiprocessing.Process(target=run_thread, args=(8,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        print(balance)