# Python之路 - 并发编程之协程

## 前言  🍀

在前面的文章中 , 基本已经可以解决并发编程中的基本问题了 , 但是如果我们要利用单线程来实现并发 , 线程是轻量级的进程 , 为了使计算机资源能更充分的利用 , 那么我们就需要用到协程了

并发的本质就是*上下文切换*加上*保存状态* , 那么我们就可以想到关键字`yield` , 我们在生成器篇章中 , 就是利用了`yield`实现了状态的保存 , 来看一个廖大大的例子

生产者消费者模型yield版

```python
import time
def consumer():
    r = ''
    time.sleep(1)
    while True:
        n = yield r
        if not n:
            return
        time.sleep(1)
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 OK'
def produce(c):
    c.send(None)
    n = 0
    while n < 5:
        n = n + 1
        time.sleep(1)
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)
        print('[PRODUCER] Consumer return: %s' % r)
    c.close()
c = consumer()
produce(c)
'''
# yiled可以保存状态,yield的状态保存与操作系统的保存线程状态很像,但是yield是代码级别控制的,更轻量级
# send可以把一个函数的结果传给另外一个函数,以此实现单线程内程序之间的切换 
'''
```

上述例子中`yield`确实实现了并发 , 但是并没有实现遇到IO操作进行自动切换 , 所以协程出场了

## 协程  🍀

首先通过上述例子 , 我们知道 , 对于单线程下 , 我们不可避免程序中出现IO操作 , 但是如果我们能够在自己的程序中去实现这一步 , 就以为着线程可以最大限度地处于就绪态 , 相当于我们在用户程序级别将自己的IO操作最大限度地隐藏起来 , 这样线程的计算效率将会得到进一步的提升

> 协程(Coroutine) : 是单线程下的并发 , 又称微线程 , 纤程 . 协程是一种用户态的轻量级线程 , 即协程有用户自己控制调度

协程的本质就是在单线程下 , 由用户自己控制一个任务遇到IO阻塞了就切换另外一个任务去执行 , 以此来提升效率

在单线程内开启协程 , 一旦遇到IO , 就会从应用程序级别控制切换 , 非IO操作的切换与效率无关

使用协程的优缺点

优点 : 

1. 协程的切换开销更小 , 属于程序级别的切换 , 更加轻量级
2. 单线程内就可以实现并发的效果 , 最大限度利用CPU

缺点 : 

1. 协程的本质是单线程下 , 无法利用多核 , 可以是一个程序开启多个进程 , 每个进程内开启多个线程 , 每个线程内开启协程
2. 协程指的是单个线程 , 因而一旦协程出现阻塞  将会阻塞整个线程

## Greenlet  🍀

我们在前面已经用`yield`实现了协程 , 但是使用`yield`需要先得到初始化一次的生成器 , 然后再调用send , 这无疑是非常麻烦的 , 所以我们可以使用`greenlet`模块可以非常简单地实现协程

```python
import greenlet
def eat(name):
    print("%s eat 1" % name)
    # 如果协程从来没有被执行过,就会调用self.run()
    # 切换到play协程
    g2.switch("Lyon")
    # 执行完毕
    print("%s eat 2" % name)
def play(name):
    print("%s play 1" % name)
    # 切换到eat协程
    g1.switch()
    # 没有切换回来,所以不执行
    print("%s play 2" % name)
# 创建一个协程对象,不会执行
# greenlet(run=None, parent=None)
g1 = greenlet.greenlet(eat)
g2 = greenlet.greenlet(play)
g1.switch("Lyon")
'''
执行结果:
Lyon eat 1
Lyon play 1
Lyon eat 2
'''
```

greenlet在没有IO的情况下或者没有重复开辟内存空间的操作下 , 反而会降低程序的执行速度 , 因为greenlet仅仅是单纯的切换 , 比如下面的例子

普通版本

```python
import time
def add1():
    num = 1
    for i in range(10000000):
        num *= i
def add2():
    num = 1
    for i in range(10000000):
        num *= i
start_time = time.time()
add1()
add2()
end_time = time.time()
print(end_time - start_time)
'''
执行结果:
1.015699863433838
'''
```

greenlet版本

```python
import greenlet
import time
def add1():
    num = 1
    for i in range(10000000):
        num *= i
        g2.switch()
def add2():
    num = 1
    for i in range(10000000):
        num *= i
        g1.switch()
start_time = time.time()
g1 = greenlet.greenlet(add1)
g2 = greenlet.greenlet(add2)
g1.switch()
end_time = time.time()
print(end_time - start_time)
'''
执行结果:
6.432543992996216
'''
```

greenlet只是提供了一种比`generator`(yield)更加快捷的切换方式 , 当切到一个任务执行时如果遇到IO , 那就原地阻塞 , 仍然是没有解决遇到IO自动切换来提升效率的问题 , 所以为了真正的提高效率 , 我们就需要使用Gevent模块了

## Gevent  🍀

Gevent是一个第三方库 , 可以通过gevent轻松实现并发同步或异步编程 , 在gevent中用到的主要模式是Greenlet , 它是以C扩展模块形式接入Python的轻量级协程 

简单使用介绍

```python
# 在gevent库中,主要使用Greenlet模式
# 创建一个协程对象,参数通过Greenlet.__init__传递
g = gevent.spawn(run=None, *args, **kwargs)
# 等待协程执行完毕,或者超时结束
g.join(timeout=None)
# 将上述两步并一步
gevent.joinall(greenlets, timeout=None, raise_error=False, count=None)
# 让协程睡眠
gevent.sleep(seconds=0, ref=True)
# 更多详细介绍请阅读官方文档
```

IO阻塞自动切换

```python
import gevent
def eat(name):
    print('%s eat 1' % name)
    # 睡2秒
    gevent.sleep(2)
    print('%s eat 2' % name)
def play(name):
    print('%s play 1' % name)
    # 睡1秒
    gevent.sleep(1)
    print('%s play 2' % name)
# 创建协程实例
g1 = gevent.spawn(eat, 'Lyon')
g2 = gevent.spawn(play, 'Lyon')
# join中由执行开关
g1.join()
g2.join()
# gevent.joinall([g1,g2])
print('End of main thread...')
```

PS : 上例中gevent.sleep(2) 模拟的是gevent可以识别的IO阻塞 , 如果是不能直接识别的需要将`from gevent import monkey ; monkey.patch_all()`放到文件的开头

Gevent同步与异步

```python
from gevent import spawn, joinall, monkey
# 打补丁,使其能直接识别
monkey.patch_all()
import time
def task(pid):
    """
    Some non-deterministic task
    """
    time.sleep(0.5)
    print('Task %s done' % pid)
# 异步执行
def synchronous():
    for i in range(10):
        task(i)
# 同步执行
def asynchronous():
    greenlet_list = [spawn(task, i) for i in range(10)]
    joinall(greenlet_list)
if __name__ == '__main__':
    print('Synchronous:')
    synchronous()
    print('Asynchronous:')
    asynchronous()
```

## Gevent实例  🍀

爬虫

```python
from gevent import monkey
monkey.patch_all()
import gevent
import requests
import time
def get_page(url):
    print('GET: %s' % url)
    response = requests.get(url)
    if response.status_code == 200:
        print('%d bytes received from %s' % (len(response.text), url))
start_time = time.time()
gevent.joinall([
    gevent.spawn(get_page, 'https://www.python.org/'),
    gevent.spawn(get_page, 'https://www.yahoo.com/'),
])
end_time = time.time()
print('run time is %s' % (end_time - start_time))
```

socket并发

server.py

```python
from gevent import monkey
monkey.patch_all()
import socket
import gevent
def server(server_ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((server_ip, port))
    s.listen(5)
    while True:
        conn,addr = s.accept()
        gevent.spawn(talk, conn, addr)
def talk(conn, addr):
    try:
        while True:
            res = conn.recv(1024)
            print('Client %s:%s msg: %s' % (addr[0], addr[1], res))
            conn.send(res.upper())
    except Exception as e:
        print(e)
    finally:
        conn.close()
if __name__ == '__main__':
    server('127.0.0.1', 8080)
```

client.py

```python
import socket
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8080))
while True:
    msg = input('>>: ').strip()
    if not msg:
        continue
    client.send(msg.encode('utf-8'))
    msg = client.recv(1024)
    print(msg.decode('utf-8'))
```







