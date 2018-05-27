#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import threading
import time
def run(num):
    print("I like num %d" % num)
    time.sleep(2)
    print("When I'm done, I'm going to keep talking...")
def main():
    for i in range(1, 6):
        t = threading.Thread(target=run, args=(i,))
        t.start()
        t.join()
if __name__ == '__main__':
    m = threading.Thread(target=main, args=[])
    m.setDaemon(True)
    m.start()
    m.join(timeout=8)