#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import gevent
def func():
    print('hello lyon')
g1 = gevent.spawn(func)