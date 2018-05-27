#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import greenlet
import time

def add1():
    num = 1
    for i in range(10000000):
        num *= i
        g2.switch()

def add2():
    num = 1
    for i in range(10000000):
        num *= i
        g1.switch()

start_time = time.time()
g1 = greenlet.greenlet(add1)
g2 = greenlet.greenlet(add2)
g1.switch()
end_time = time.time()
print(end_time - start_time)