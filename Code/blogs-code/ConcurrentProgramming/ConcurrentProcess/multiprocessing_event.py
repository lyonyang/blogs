#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import multiprocessing
import time
import random

def conn_mysql(conn, event):
    count = 1
    while not event.is_set():
        if count > 3:
            raise TimeoutError('Connection timeout...')
        print('%s %sth attempt to connect' % (conn, count))
        event.wait(0.5)
        count += 1
    print('%s connect successfully' % conn)

def check_mysql(conn, event):
    print('%s is checking mysql' % conn)
    time.sleep(random.randint(2, 4))
    event.set()

if __name__ == '__main__':
    event = multiprocessing.Event()
    for i in range(10):
        conn = multiprocessing.Process(target=conn_mysql, args=('conn'+str(i), event))
        conn.start()
