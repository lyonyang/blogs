#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import threading
import time
def func(name):
    print("I am %s" % name)
    time.sleep(2)
if __name__ == '__main__':
    t1 = threading.Thread(target=func, args=("Lyon",))
    t2 = threading.Thread(target=func, args=("Kenneth",))
    print(t1.isAlive)
    print(t1.daemon)
    print(t1.ident)
    print(t1.name)
    t1.start()
    t2.start()
    t1.join()
    print(t1.getName())
    print(t2.getName())
