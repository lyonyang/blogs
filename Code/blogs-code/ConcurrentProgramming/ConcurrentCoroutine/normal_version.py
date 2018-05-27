#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import time

def add1():
    num = 1
    for i in range(10000000):
        num *= i

def add2():
    num = 1
    for i in range(10000000):
        num *= i

start_time = time.time()
add1()
add2()
end_time = time.time()
print(end_time - start_time)