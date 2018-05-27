#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import gevent

def eat(name):
    print('%s eat 1' % name)
    gevent.sleep(2)
    print('%s eat 2' % name)

def play(name):
    print('%s play 1' % name)
    gevent.sleep(1)
    print('%s play 2' % name)

g1 = gevent.spawn(eat, 'Lyon')
g2 = gevent.spawn(play, 'Lyon')
g1.join()
g2.join()
# gevent.joinall([g1,g2])
print('End of main thread...')