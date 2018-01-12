#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import time

def consumer():
    r = ''
    time.sleep(1)
    while True:
        n = yield r
        if not n:
            return
        time.sleep(1)
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 OK'

def produce(c):
    c.send(None)
    n = 0
    while n < 5:
        n = n + 1
        time.sleep(1)
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)
        print('[PRODUCER] Consumer return: %s' % r)
    c.close()

c = consumer()
produce(c)