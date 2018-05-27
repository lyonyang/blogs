#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
from gevent import spawn, joinall, monkey
monkey.patch_all()
import time

def task(pid):
    """
    Some non-deterministic task
    """
    time.sleep(0.5)
    print('Task %s done' % pid)

def synchronous():
    for i in range(10):
        task(i)

def asynchronous():
    greenlet_list = [spawn(task, i) for i in range(10)]
    joinall(greenlet_list)

if __name__ == '__main__':
    print('Synchronous:')
    synchronous()
    print('Asynchronous:')
    asynchronous()