#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import time
import random
import queue
import threading
q = queue.Queue()

def Producer(name):
    count = 1
    while count < 20:
        time.sleep(random.randrange(3))
        q.put(count)
        print('Producer %s has produced %s bun...' % (name, count))
        count += 1

def Consumer(name):
    count = 1
    while count < 20:
        time.sleep(random.randrange(4))
        if not q.empty():
            data = q.get()
            print(data)
            print('\033[32;1mConsumer %s has eat %s bun...\033[0m' % (name, data))
        else:
            print("No bun anymore...")
        count += 1

p1 = threading.Thread(target=Producer, args=('Lyon',))
c1 = threading.Thread(target=Consumer, args=('Kenneth',))
p1.start()
c1.start()