#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import threading

def hello1():
    print("I am Lyon")
def hello2():
    print("Hello, future")
t1 = threading.Timer(1, hello1)
t2 = threading.Timer(2,hello2)
t1.start()
t2.start()