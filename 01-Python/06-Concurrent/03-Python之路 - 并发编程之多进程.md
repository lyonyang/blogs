# Python之路 - 多进程编程

## 前言  🍀

上一篇《[多线程编程](https://lyonyang.gitbooks.io/blog/01-Python/06-%E5%B9%B6%E5%8F%91%E7%BC%96%E7%A8%8B%E7%AF%87/02-Python%E4%B9%8B%E8%B7%AF%20-%20%E5%A4%9A%E7%BA%BF%E7%A8%8B%E7%BC%96%E7%A8%8B.html)》中已经对Python中多线程部分进行了整理 , 进程中有很多也是相似的

概念在并发编程第一篇中就已经介绍了 , So直接开始操作

## multiprocessing  🍀

从上一篇我们也已经知道了 , Python中的多线程无法利用多核优势 , 所以如果我们想要充分地使用多核CPU的资源 , 那么就只能靠多进程了 , 因为进程是系统调度的 , Python提供了` multiprocessing`模块了对多进程的支持

multiprocessing模块中提供了Process , Queue , Pipe , Lock , RLock , Event , Condition等组件 , 与threading模块有很多相似之处

## Process  🍀

用于创建进程的类 , 与threading模块中的` _Thread`类类似 

```python
'''
Process类的构造函数
def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
'''
```

参数说明

| 参数     | 说明                                       |
| ------ | ---------------------------------------- |
| group  | 未使用 , 值始终                                |
| target | 与threading.Tread中的target参数一样 , 表示调用对象 , 即子进程要执行的任务 |
| name   | 子进程的名称                                   |
| args   | 传入target函数中的位置参数 , 是一个元组 , 与线程一样 , 参数后必须加逗号 |
| kwargs | 表示调用对象的字典                                |

方法说明

| 方法                                | 说明                                       |
| --------------------------------- | ---------------------------------------- |
| Process.run (self)                | 进程启动时运行的方法 , 由该方法调用target参数所指定的函数 , 在子类中可以进行重构 , 与线程中一样 |
| Process.start (self)              | 启动进程 , start方法就是去帮你调用run方法               |
| Process.terminate (self)          | 强制终止进程 , 不会进行任何清理操作 , 使用时需小心其子进程与锁的问题    |
| Process.join (self, timeout=None) | 与线程中一样 , 阻塞调用 , 主进程进行等待 , timeout为超时时间   |
| Process.is_alive (self)           | 判断进程是否正在运行 , 返回bool值                     |

实例属性说明

| 属性               | 说明                                       |
| ---------------- | ---------------------------------------- |
| Process.daemon   | 默认值为False , True则为守护进程                   |
| Process.name     | 进程的名称                                    |
| Process.pid      | 进程的pid                                   |
| Process.exitcode | 进程运行时为None , 如果为-N , 表示被信号N结束            |
| Process.authkey  | 进程的身份验证键 , 默认是由os.urandom()随机生成的32字符的字符串 .  这个键的用途是为涉及网络连接的底层进程间通信提供安全性 , 这类连接只有在具有相同的身份验证键时才能成功 |

**创建进程** 

与创建线程的方式一样 , 有两种

函数调用

```python
import multiprocessing
import time
def hello(name):
    print("I am %s" % name)
    time.sleep(1)
    print("Hello future...")
if __name__ == '__main__':
    # 创建一个进程实例
    p = multiprocessing.Process(target=hello, args=("Lyon",))
    # 启动进程,实质调用run()
    p.start()
    print("End of main process...")
'''
执行结果:
End of main process...
I am Lyon
Hello future...
'''
```

类继承调用

```python
import multiprocessing
import time
# 自定义进程类,继承multiprocessing中的Process类
class MyProcess(multiprocessing.Process):
    def __init__(self, name):
        super().__init__()
        self.name = name
    # 重构父类中的run方法
    def run(self):
        print("I am %s" % self.name)
        time.sleep(1)
        print("Hello future...")
if __name__ == '__main__':
    # 创建一个进程实例
    p = MyProcess('Lyon')
    # 启动进程
    p.start()
    print("End of main process...")
'''
执行结果:
End of main process...
I am Lyon
Hello future...
'''
```

在上栗创建进程中有一个问题 , 就是如果我们在Windows下 , 使用`start()`方法 , 就必须加上`if __name__ == '__main__':`  , 进程是通过`fork`系统调用 , 而Windows中并没有fork , 所以多处理模块启动了一个新的Python进程 , 并导入了调用模块 . 如果进程在导入的时候被调用 , 那么这就会引发无限的新进程 , 后果不言而喻 . 当然还是可以直接使用`run()`的

## Join & Daemon  🍀

join

进程中join与线程中的join是一样的 , 就进行阻塞调用 , 让主进程进行等待 , 整体串行

实例

```python
# 多线程中的例子,换汤不换药
import multiprocessing
import time
def run(name):
    print("I am %s" % name)
    time.sleep(2)
    print("When I'm done, I'm going to keep talking...")
if __name__ == '__main__':
    lyon = multiprocessing.Process(target=run, args=('Lyon',))
    kenneth = multiprocessing.Process(target=run, args=('Kenneth',))
    lyon.start()
    lyon.join()
    kenneth.start()
    kenneth.join()
    print("I was the main thread, and I ended up executing")
'''
执行结果:
I am Lyon
When I'm done, I'm going to keep talking...
I am Kenneth
When I'm done, I'm going to keep talking...
I was the main thread, and I ended up executing
'''
```

Daemon

守护进程会在主进程代码执行结束后就终止

```python
# 还是多线程中的例子
import multiprocessing
import time
def run(num):
    print("I like num %d" % num)
    time.sleep(2)
    print("When I'm done, I'm going to keep talking...")
def main():
    for i in range(1, 6):
        t = multiprocessing.Process(target=run, args=(i,))
        t.daemon = True
        t.start()
        t.join()
if __name__ == '__main__':
    m = multiprocessing.Process(target=main, args=[])
    m.start()
    m.join(timeout=8)
'''
执行结果:
I like num 1
When I'm done, I'm going to keep talking...
I like num 2
When I'm done, I'm going to keep talking...
I like num 3
When I'm done, I'm going to keep talking...
I like num 4
When I'm done, I'm going to keep talking...
I like num 5
When I'm done, I'm going to keep talking...
'''
```

PS : 与线程不同的是 , 守护进程内无法再开启子进程 , 否则就抛出异常

## Lock  🍀

进程之间的数据是不共享的 , 因为每个进程之间是相互独立的 , 但是进程共享一套文件系统 , 所以访问同一个文件 , 是没有问题的 , 但是如果有多个进程对同一文件进行修改 , 就会造成错乱 , 所以我们为了保护文件数据的安全 , 就需要给其进行加锁

同样的 , join为整体串行 , lock为局部串行

廖大大实例 , Lock

```python
import multiprocessing
# 假定这是你的银行存款:
balance = 0
def change_it(n):
    # 先存后取，结果应该为0:
    global balance
    balance = balance + n
    balance = balance - n
# 创建一把锁
lock = multiprocessing.Lock()
def run_thread(n):
    for i in range(100000):
        # 先要获取锁:
        lock.acquire()
        try:
            # 放心地改吧:
            change_it(n)
        finally:
            # 改完了一定要释放锁:
            lock.release()
# 在多线程例子中并没有写这句,但是多进程中使用start()必须加
if __name__ == '__main__':
    for j in range(10000):
        t1 = multiprocessing.Process(target=run_thread, args=(5,))
        t2 = multiprocessing.Process(target=run_thread, args=(8,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        print(balance)
'''
执行结果:
0
.
# 数据安全得到了保障,所以全为0
...
```

RLock

```python
import multiprocessing
import time
mutexA = mutexB = multiprocessing.RLock()
class MyThread(multiprocessing.Process):
    def run(self):
        self.func1()
        self.func2()
    def func1(self):
        mutexA.acquire()
        print("\033[31m%s get mutexA...\033[0m" % self.name)
        mutexB.acquire()
        print("\033[33m%s get mutexB...\033[0m" % self.name)
        mutexB.release()
        mutexA.release()
    def func2(self):
        mutexB.acquire()
        print("\033[35m%s get mutexB...\033[0m" % self.name)
        time.sleep(1)
        mutexA.acquire()
        print("\033[37m%s get mutexA...\033[0m" % self.name)
        mutexA.release()
        mutexB.release()
if __name__ == '__main__':
    for i in range(10):
        t = MyThread()
        t.start()
```

## Producer-consumer  🍀

生产者消费者模式 , 在多线程中已经有过说明了 , 目的是为了解决并发问题

实例

```python
# 可与多线程篇中进行对照
import time
import random
import multiprocessing
q = multiprocessing.Queue()
def Producer(name, q):
	count = 1
    while count < 5:
        time.sleep(random.randrange(3))
        q.put(count)
        print('Producer %s has produced %s bun...' % (name, count))
        count += 1
def Consumer(name , q):
    count = 1
    while count < 20:
        time.sleep(random.randrange(4))
        if not q.empty():
            data = q.get()
            print(data)
            print('\033[32;1mConsumer %s has eat %s bun...\033[0m' % (name, data))
        else:
            print("No bun anymore...")
if __name__ == '__main__':
    # 进程间的数据是不共享的,注意我们需要把q,即队列对象传入函数中
    p1 = multiprocessing.Process(target=Producer, args=('Lyon', q,))
    c1 = multiprocessing.Process(target=Consumer, args=('Kenneth', q,))
    p1.start()
    c1.start()
    p1.join()
    c1.join()
    print("End of main process...")
```

## Queue  🍀

multiprocessing模块支持进程间通信有两种主要形式 , 队列和管道

在多线程中有queue模块 , 供我们实现队列接口 , 在多进程中则是Queue类为我们提供队列接口

Queue为单向通道 , 先进先出(FIFO)

```python

class Queue(object):
    def __init__(self, maxsize=-1):
        self._maxsize = maxsize
	# 返回队列中目前项目数量,使用时防止竞争,最好令其串行
    def qsize(self):
        return 0
	# 队列是否为空,返回True,使用时防止竞争,最好令其串行
    def empty(self):
        return False
	# 队列是否已满,返回True,使用时防止竞争,最好令其串行
    def full(self):
        return False
	# 将数据放入队列
    def put(self, obj, block=True, timeout=None):
        pass
	# 同上put
    def put_nowait(self, obj):
        pass
	# 从队列中取出项
    def get(self, block=True, timeout=None):
        pass
	# 同上get
    def get_nowait(self):
        pass
	# 关闭队列,垃圾回收会调用此方法
    def close(self):
        pass
	# 连接队列的后台线程,用于等待所有队列项消耗
    def join_thread(self):
        pass
	# 不会在在进程退出时自动连接后台线程,可防止join_thread()方法阻塞
    def cancel_join_thread(self):
        pass
```

实例

```python
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
'''
执行结果:
True
First
Second
Third
True

'''
```

## Pipe  🍀

介绍

```python
# Pipe在进程之间创建一条管道,并返回元组(connection(),connection())
def Pipe(duplex=True):
    return Connection(), Connection()
# 管道端的连接对象
class Connection(object):
    # 发送对象
    def send(self, obj):
        pass
	# 接收另一端发送的对象
    def recv(self):
        pass
	# 返回连接使用的整数文件描述符
    def fileno(self):
        return 0
	# 关闭链接
    def close(self):
        pass
	# 如果链接上的数据可用,返回True
    def poll(self, timeout=None):
        pass
	# 发送字节到数据缓冲区,buffer是支持缓冲区接口的任意对象,offset为偏移量,size为字节数
    def send_bytes(self, buffer, offset=-1, size=-1):
        pass
	# 接收一条完整字节消息
    def recv_bytes(self, maxlength=-1):
        pass
	# 接收一条完整的字节消息,并把它保存在buffer对象中,该对象支持可写入的缓冲区接口
    def recv_bytes_into(self, buffer, offset=-1):
        pass
'''
Connection类与我们网络编程中所使用的socket(TCP)类似,socket(TCP)对象之间通信也是双向的
...
```

基于管道实现进程间通信

```python
import multiprocessing
def producer(seq, p):
    left,right = p
    # 关闭不使用的一端
    right.close()
    for i in seq:
        # 发送进管道中
        left.send(i)
    else:
        # 关闭管道
        left.close()
def consumer(p, name):
    left,right = p
    # 关闭不使用的一端
    left.close()
    while True:
        # 如果消费者不使用的一端忘记关闭,消费者中的recv()就一直等下去
        try:
            bun = right.recv()
            print('%s got %s buns...' % (name, bun))
        # 触发EOFError
        except EOFError:
            right.close()
            break
if __name__ == '__main__':
    # 创建管道实例
    left, right = multiprocessing.Pipe()
    c1 = multiprocessing.Process(target=consumer, args=((left, right), 'c1'))
    c1.start()
    seq = (i for i in range(10))
    producer(seq, (left, right))
    right.close()
    left.close()
    c1.join()
    print('End of main process...')
```

## Manager  🍀

进程之间是相互独立的 , 在multiprocessing模块中的Manager可以实现进程间数据共享 , 并且Manager还支持进程中的很多操作 , 比如Condition , Lock , Namespace , Queue , RLock , Semaphore等

由于基于消息传递(Queue , Pipe)的并发编程才是未来的主流 , 所以对于Manager应该尽量避免使用

Manager实例

```python
import multiprocessing
# 既然数据共享了,就需要像多线程那样,防止竞争
def run(d,lock):
  	# 演示没加锁的实例
    # lock.acquire()
    d['count'] -= 1
    # lock.release()
if __name__ == '__main__':
    # lock = multiprocessing.Lock()
    with multiprocessing.Manager() as m:
        dic = m.dict({'count' : 100})
        process_list = []
        for i in range(100):
            p = multiprocessing.Process(target=run, args=(dic, lock,))
            process_list.append(p)
            p.start()
        for p in process_list:
            p.join()
        print(dic)
'''
执行结果:
# 该结果看缘分了,没加锁数据共享,导致混乱,与线程中一样
{'count': 1}
'''
```

更多详细内容< [multiprocessing.Manager](https://docs.python.org/3/library/multiprocessing.html?highlight=manager#module-multiprocessing.managers) > 

## Semaphore  🍀

与线程中一样

```python
class Semaphore(object):
    def __init__(self, value=1):
        pass

    def acquire(self, blocking=True, timeout=None):
        pass

    def release(self):
        pass
```

实例

```python
import multiprocessing
import time
def func(sem, num):
    sem.acquire()
    print('%s get semaphores' % num)
    time.sleep(2)
    sem.release()
if __name__ == '__main__':
    sem = multiprocessing.Semaphore(5)
    for i in range(1,11):
        t = multiprocessing.Process(target=func, args=(sem, i,))
        t.start()
```

## Event  🍀

与线程中一样

```python
class Event(object):
    def is_set(self):
        return False
    def set(self):
        pass
    def clear(self):
        pass
    def wait(self, timeout=None):
        pass
```

实例

```python
import multiprocessing
import time
import random
def conn_mysql(conn, event):
    count = 1
    while not event.is_set():
        if count > 3:
            # 主动触发超时异常
            raise TimeoutError('Connection timeout...')
        print('%s %sth attempt to connect' % (conn, count))
        event.wait(0.5)
        count += 1
    print('%s connect successfully' % conn)
def check_mysql(conn, event):
    print('%s is checking mysql' % conn)
    time.sleep(random.randint(2, 4))
    event.set()
if __name__ == '__main__':
    event = multiprocessing.Event()
    for i in range(10):
        conn = multiprocessing.Process(target=conn_mysql, args=('conn'+str(i), event))
        conn.start()
```

## Pool  🍀

`multiprocessing`中的Process实现了我们对多进程的需求 , 但是当我们进行并发编程时 , 一旦需要开启的进程数量非常大时 , 使用Process已经不能满足我们的要求了 . 因为进程是需要占用系统资源的 , 操作系统不可能去无限的开启进程 ; 并且使用Process动态生成多个进程 , 我们还需要手动的去限制进程的数量 , 所以这个时候我们就应该用进程池(Pool)来实现了

`multiprocessing.Pool` 

参数说明

| 参数          | 说明                               |
| ----------- | -------------------------------- |
| numprocess  | 要创建的进程数 , 如果省略  将默认使用cpu_count() |
| initializer | 每个进程启动时要执行的可调用对象                 |
| initargs    | 传给initializer的参数组                |

方法说明

| 方法                                       | 说明                                       |
| ---------------------------------------- | ---------------------------------------- |
| Pool.apply(self, func, args=(), kwds={}) | 在一个进程池中执行func(*args , **kwargs) , 并返回结果  |
| Pool.apply_async(self, func, args=(), kwds={}, callback=None, | 与apply()方法一样 , 该方法为异步版本应用的方法 , 返回结果是AsyncResult类的实例 , callback指定回调的函数 . callback禁止执行任何阻塞操作 , 否则将接收其他异步操作中的结果 |
| Pool.close(self)                         | 关闭进程池 , 如果所有操作持续挂起 , 它们将在工作进程终止前完成       |
| Pool.join(self)                          | 等待所有工作进程退出                               |
| Pool.get(self, timeout=None)             | 获取结果 , timeout可选                         |
| Pool.ready(self)                         | 完成调用就返回True                              |
| Pool.successful(self)                    | 完成调用并且没有引发异常返回True , 在结果就绪之前调用此方法会引发异常   |
| Pool.wait(self, timeout=None)            | 等待结果变为可用                                 |
| Pool.terminate(self)                     | 立即终止所有工作进程 , 垃圾回收会自动调用此方法                |

同步调用apply

```python
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
```

异步调用apply_async

```python
from multiprocessing import Pool
import os
import time
def run(n):
    print("%s run..." % os.getpid())
    time.sleep(2)
    return n**2
if __name__ == '__main__':
    # 进程池没满就新创建进程执行请求,否则就等待
    # 注意,这里指定进程池数量为3,会一直是这三个进程在执行,只不过执行的请求可能改变
    pool = Pool(3)
    res_list = []
    for i in range(10):
        res = pool.apply_async(run, args=(i,))
        res_list.append(res)
    pool.close()
    pool.join()
    for res in res_list:
        print(res.get())
```