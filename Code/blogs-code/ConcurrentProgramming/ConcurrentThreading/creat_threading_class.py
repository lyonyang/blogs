#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import threading
import time
class MyThread(threading.Thread):
    def __init__(self, name):
        # threading.Thread.__init__(self)
        super().__init__()
        self.name = name

    def run(self):
        print("I am %s" % self.name)
        time.sleep(2)

if __name__ == '__main__':
    t1 = MyThread('Lyon')
    t2 = MyThread('Kenneth')
    t1.start()
    t2.start()
    print(t1.getName())
    print(t2.getName())