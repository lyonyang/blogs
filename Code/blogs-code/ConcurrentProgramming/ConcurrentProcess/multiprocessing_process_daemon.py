#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import multiprocessing
import time

def run(num):
    print("I like num %d" % num)
    time.sleep(2)
    print("When I'm done, I'm going to keep talking...")

def main():
    for i in range(1, 6):
        t = multiprocessing.Process(target=run, args=(i,))
        t.daemon = True
        t.start()
        t.join()

if __name__ == '__main__':
    m = multiprocessing.Process(target=main, args=[])
    m.start()
    m.join(timeout=8)