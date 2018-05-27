#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import time
import random
import multiprocessing

q = multiprocessing.Queue()

def Producer(name, q):
  count = 1
  while count < 5:
    time.sleep(random.randrange(3))
    q.put(count)
    print('Producer %s has produced %s bun...' % (name, count))
    count += 1

def Consumer(name , q):
    count = 1
    while count < 20:
        time.sleep(random.randrange(4))
        if not q.empty():
            data = q.get()
            print(data)
            print('\033[32;1mConsumer %s has eat %s bun...\033[0m' % (name, data))
        else:
            print("No bun anymore...")

if __name__ == '__main__':
    p1 = multiprocessing.Process(target=Producer, args=('Lyon', q,))
    c1 = multiprocessing.Process(target=Consumer, args=('Kenneth', q,))
    p1.start()
    c1.start()
    p1.join()
    c1.join()
    print("End of main process...")