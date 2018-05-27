#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import multiprocessing
# 既然数据共享了,就需要像多线程那样,防止竞争
def run(d,lock):
    # lock.acquire()
    d['count'] -= 1
    # lock.release()
if __name__ == '__main__':
    lock = multiprocessing.Lock()
    with multiprocessing.Manager() as m:
        dic = m.dict({'count': 100})
        process_list = []
        for i in range(100):
            p = multiprocessing.Process(target=run, args=(dic, lock,))
            process_list.append(p)
            p.start()
        for p in process_list:
            p.join()
        print(dic)