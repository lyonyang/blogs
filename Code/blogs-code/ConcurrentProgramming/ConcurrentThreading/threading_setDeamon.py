#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import threading
import time
def run(name):
    print("I am %s" % name)
    time.sleep(2)
    print("When I'm done, I'm going to keep talking...")
if __name__ == '__main__':
    lyon = threading.Thread(target=run, args=('Lyon',))
    kenneth = threading.Thread(target=run, args=('Kenneth',))
    lyon.setDaemon(True)
    lyon.start()
    kenneth.setDaemon(True)
    kenneth.start()
    time.sleep(5)
    print("I was the main thread, and I ended up executing")
