#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import multiprocessing
import time

def func(sem, num):
    sem.acquire()
    print('%s get semaphores' % num)
    time.sleep(2)
    sem.release()

if __name__ == '__main__':
    sem = multiprocessing.Semaphore(5)
    for i in range(1,11):
        t = multiprocessing.Process(target=func, args=(sem, i,))
        t.start()