#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon

# 先进先出
import queue
q = queue.Queue()
q.put('First')
q.put('Second')
q.put('Third')
print(q.get())
print(q.get())
print(q.get())
'''
执行结果:
First
Second
Third
'''

# 后进先出
import queue
q = queue.LifoQueue()
q.put('First')
q.put('Second')
q.put('Third')
print(q.get())
print(q.get())
print(q.get())
'''
执行结果:
Third
Second
First
'''

# 可设置优先级
import queue
q = queue.PriorityQueue()
#put进入一个元组,元组的第一个元素是优先级,越小优先级越高
q.put((20, 'A'))
q.put((10, 'B'))
q.put((30, 'C'))

print(q.get())
print(q.get())
print(q.get())
'''
执行结果:
(10, 'B')
(20, 'A')
(30, 'C')
'''