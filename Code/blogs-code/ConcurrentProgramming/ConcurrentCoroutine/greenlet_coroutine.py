#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import greenlet

def eat(name):
    print("%s eat 1" % name)
    # 开关
    g2.switch("Lyon")
    print("%s eat 2" % name)

def play(name):
    print("%s play 1" % name)
    g1.switch()
    print("%s play 2" % name)

g1 = greenlet.greenlet(eat)
g2 = greenlet.greenlet(play)
g1.switch("Lyon")