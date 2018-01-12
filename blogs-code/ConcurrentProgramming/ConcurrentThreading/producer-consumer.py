#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import threading
import queue
def producer():
    for i in range(10):
        q.put("%d bottle of milk" % i)
    print("Start waiting for all the milk to be taken...")
    q.join()
    print("All the milk was taken out...")

def consumer(name):
    while q.qsize()> 0:
        print("%s got %s" % (name, q.get()))
        q.task_done()

q = queue.Queue()
p = threading.Thread(target=producer,)
p.start()
c1 = consumer("Lyon")