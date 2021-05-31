#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import threading
import time
import random
def conn_mysql():
    count = 1
    while not event.is_set():
        if count > 3:
            raise TimeoutError('Connection timeout...')
        print('%s %sth attempt to connect' % (threading.current_thread().getName(), count))
        event.wait(0.5)
        count += 1
    print('%s connect successfully' % threading.current_thread().getName())

def check_mysql():
    print('%s is checking mysql' % threading.current_thread().getName())
    time.sleep(random.randint(2, 4))
    event.set()

if __name__ == '__main__':
    event = threading.Event()
    conn1 = threading.Thread(target=conn_mysql)
    conn2 = threading.Thread(target=conn_mysql)
    check = threading.Thread(target=check_mysql)
    conn1.start()
    conn2.start()
    check.start()