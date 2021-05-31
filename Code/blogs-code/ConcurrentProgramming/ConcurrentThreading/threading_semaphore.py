#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import threading
import time
def func():
    sm.acquire()
    print('%s get semaphores' % threading.current_thread().getName())
    time.sleep(2)
    sm.release()
if __name__ == '__main__':
    sm = threading.Semaphore(5)
    for i in range(10):
        t = threading.Thread(target=func)
        t.start()