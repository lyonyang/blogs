#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import os
# os.getpid()获取父进程的ID
print("Process %s start..." % os.getpid())
# fock()调用一次会返回两次
pid = os.fork()
# 子进程返回0
if pid == 0:
    print("I am child process %s and my parent is %s" % (os.getpid(), os.getppid()))
# 父进程返回子进程的ID
else:
    print("I %s just created a child process %s" % (os.getpid(), pid))
