#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import multiprocessing
import time

def run(name):
    print("I am %s" % name)
    time.sleep(2)
    print("When I'm done, I'm going to keep talking...")

if __name__ == '__main__':
    lyon = multiprocessing.Process(target=run, args=('Lyon',))
    kenneth = multiprocessing.Process(target=run, args=('Kenneth',))
    lyon.start()
    lyon.join()
    kenneth.start()
    kenneth.join()
    print("I was the main thread, and I ended up executing")