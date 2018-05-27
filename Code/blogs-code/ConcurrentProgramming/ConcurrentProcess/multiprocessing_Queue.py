#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import multiprocessing
q = multiprocessing.Queue(3)
q.put("First")
q.put("Second")
q.put("Third")
print(q.full())
print(q.get())
print(q.get())
print(q.get())
print(q.empty())