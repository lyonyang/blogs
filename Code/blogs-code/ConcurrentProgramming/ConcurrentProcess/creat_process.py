#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
'''
import multiprocessing
import time
def hello(name):
    print("I am %s" % name)
    time.sleep(1)
    print("Hello future...")
if __name__ == '__main__':
    p = multiprocessing.Process(target=hello, args=("Lyon",))
    p.start()
    print("End of main process...")
'''

# 类继承调用
import multiprocessing
import time
# 自定义进程类,继承multiprocessing中的Process类
class MyProcess(multiprocessing.Process):
    '''自定义进程类'''
    def __init__(self, name):
        super().__init__()
        self.name = name
    # 重构父类中的run方法
    def run(self):
        print("I am %s" % self.name)
        time.sleep(1)
        print("Hello future...")

# if __name__ == '__main__':
# 创建一个进程实例
p = MyProcess('Lyon')
# 启动进程
# p.start()

p.run()
print("End of main process...")

