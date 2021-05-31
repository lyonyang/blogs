#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import multiprocessing

def producer(seq, p):
    left,right = p
    right.close()
    for i in seq:
        left.send(i)
    else:
        left.close()

def consumer(p, name):
    left,right = p
    left.close()
    while True:
        try:
            bun = right.recv()
            print('%s got %s buns...' % (name, bun))
        except EOFError:
            right.close()
            break

if __name__ == '__main__':
    left, right = multiprocessing.Pipe()
    c1 = multiprocessing.Process(target=consumer, args=((left, right), 'c1'))
    c1.start()
    seq = (i for i in range(10))
    producer(seq, (left, right))
    right.close()
    left.close()
    c1.join()
    print('End of main process...')
    multiprocessing.Manager