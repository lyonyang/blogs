#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
from multiprocessing import Pool
import os
import time

def run(n):
    print("%s run..." % os.getpid())
    # 不令其阻塞,结果会同时打印
    time.sleep(2)
    return n**2

if __name__ == '__main__':
    # 进程池没满就新创建进程执行请求,否则就等待
    # 注意,这里指定进程池数量为3,会一直是这三个进程在执行,只不过执行的请求可能改变
    pool = Pool(3)
    res_list = []
    for i in range(10):
        # 获取执行结果,同步运行,会阻塞等待拿到结果,等待过程中无论是否阻塞都会在原地等
        # 注意等待过程中由于阻塞,其cpu权限会被夺走
        res = pool.apply(run, args=(i,))
        res_list.append(res)
    print(res_list)