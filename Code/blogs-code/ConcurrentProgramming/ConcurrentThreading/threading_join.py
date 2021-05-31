#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
# import threading
# import time
# class MyThread(threading.Thread):
#     def __init__(self,name):
#         threading.Thread.__init__(self)
#         self.name = name
#
#     def run(self):
#         print("I am %s" % self.name)
#         time.sleep(2)
#
# if __name__ == '__main__':
#     t1 = MyThread('Lyon')
#     t2 = MyThread('Kenneth')
#     t1.start()
#     t1.join()
#     t2.start()
#     t2.join()
#     print("主线程")

import threading
import time

def run(name):
    print("I am %s" % name)
    time.sleep(2)
    print("When I'm done, I'm going to keep talking...")

if __name__ == '__main__':
    lyon = threading.Thread(target=run, args=('Lyon',))
    kenneth = threading.Thread(target=run, args=('Kenneth',))
    lyon.start()
    lyon.join()
    kenneth.start()
    kenneth.join()
    print("I was the main thread, and I ended up executing")
