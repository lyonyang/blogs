#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import threading
import time
mutexA = mutexB = threading.RLock()
class MyThread(threading.Thread):
    def run(self):
        self.func1()
        self.func2()
    def func1(self):
        mutexA.acquire()
        print("\033[31m%s get mutexA...\033[0m" % self.name)
        mutexB.acquire()
        print("\033[33m%s get mutexB...\033[0m" % self.name)
        mutexB.release()
        mutexA.release()
    def func2(self):
        mutexB.acquire()
        print("\033[35m%s get mutexB...\033[0m" % self.name)
        time.sleep(1)
        mutexA.acquire()
        print("\033[37m%s get mutexA...\033[0m" % self.name)
        mutexA.release()
        mutexB.release()

if __name__ == '__main__':
    for i in range(10):
        t = MyThread()
        t.start()