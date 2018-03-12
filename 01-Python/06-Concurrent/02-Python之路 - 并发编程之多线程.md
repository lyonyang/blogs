# Python之路 - 多线程编程

## 前言  🍀

在上一篇中说了一大堆理论 , 那么现在就开始实践了 

先说线程再说进程 , 为什么 ?  因为在Python中有一个` Python GIL  `全局解释器锁 , 这是个什么东西? 最后来说

总之线程和进程都是与操作系统有关的知识 , 所以操作系统基础 , 对于这两节内容的理解会有很大的帮助

## Threading  🍀

Python通过两个标准库` _thread` (built-in) 和`threading`提供对线程的支持 , threading对_thread进行了封装

```python
_thread.py
'''
This module provides primitive operations to write multi-threaded programs.
The 'threading' module provides a more convenient interface.
'''
```

So , 明显我们一般直接使用threading

threading模块中提供了Thread , Lock , RLock , Semaphore , Event , Condition , Timer等组件

## Thread  🍀

参数说明

| 参数     | 说明                                  |
| ------ | ----------------------------------- |
| group  | 未使用 , 值始终                           |
| target | 表示调用对象 , 即子线程要执行的任务                 |
| name   | 子线程的名称                              |
| args   | 传入target函数中的位置参数 , 是一个元组 , 参数后必须加逗号 |
| kwargs | 表示调用对象的字典                           |

方法说明

| 方法                               | 说明                                       |
| -------------------------------- | ---------------------------------------- |
| Thread.run (self)                | 进程启动时运行的方法 , 由该方法调用target参数所指定的函数 , 在子类中可以进行重构 , 与线程中一样 |
| Thread.start (self)              | 启动进程 , start方法就是去帮你调用run方法               |
| Thread.terminate (self)          | 强制终止线程 , 不会进行任何清理操作 , 使用时需小心其子进程与锁的问题    |
| Thread.join (self, timeout=None) | 阻塞调用 , 主线程进行等待 , timeout为超时时间            |
| Thread.is_alive (self)           | 这个方法在run()方法开始之前返回True , 在run()方法结束之后 , 返回所有活动线程的列表 |
| Thread.isDaemon(self)            | 判断是否为守护线程 , 返回bool值                      |
| Thread.setDaemon(self,daemonic)  | 将子线程设置为守护线程 , daemonic = daemon          |
| Thread.getName(self,name)        | 获取线程名称                                   |
| Thread.setName(self,name)        | 设置线程名称                                   |

实例属性说明

| 属性             | 说明                     |
| -------------- | ---------------------- |
| Thread.daemon  | 默认值为False , True则为守护线程 |
| Thread.name    | 线程的名称                  |
| Thread.isAlive | 即为is_alive的返回值         |
| Thread.ident   | 线程标识符 , 没启动则为None      |

**创建线程**  

Python中使用线程有两种方式 : 函数或者用类来包装线程对象

函数调用

```python
import threading
import time
# 定义线程要运行的函数
def func(name):
    print("I am %s" % name)
    # 为了便于观察,让它睡上2秒
    time.sleep(2)
# 防止被导入执行两次
if __name__ == '__main__':
    # 创建一个线程实例,args参数是一个元组,必须加逗号
    t1 = threading.Thread(target=func, args=("Lyon",))
    # 再创建一个线程实例
    t2 = threading.Thread(target=func, args=("Kenneth",))
    # 启动线程
    t1.start()
    # 启动另一个线程
    t2.start()
    # 打印线程名
    print(t1.getName())
    # 打印线程名
    print(t2.getName())
'''
执行结果:
I am Lyon
I am Kenneth
Thread-1
Thread-2
'''
```

类继承调用

```python
import threading
import time
# 继承threading中的Thread类
class MyThread(threading.Thread):
    # 线程中所需要的参数
    def __init__(self, name):
        # threading.Thread.__init__(self)
        super().__init__()
        self.name = name
	# 重构run方法,注意这个是表示线程活动的方法,必须有
    def run(self):
        print("I am %s" % self.name)
        time.sleep(2)
# 防止被导入执行两次
if __name__ == '__main__':
    # 创建一个线程实例
    t1 = MyThread('Lyon')
    # 创建另一个线程实例
    t2 = MyThread('Kenneth')
    # 启动线程,调用了类中的run方法
    t1.start()
    # 启动另一个线程
    t2.start()
    # 获取线程名
    print(t1.getName())
    # 获取线程名
    print(t2.getName())
'''
执行结果: 
I am Lyon
I am Kenneth
Lyon
Kenneth
'''
```

```
Thread实例对象的方法
  # isAlive(): 返回线程是否活动的。
  # getName(): 返回线程名。
  # setName(): 设置线程名。
threading模块提供的一些方法：
  # threading.currentThread(): 返回当前的线程变量。
  # threading.enumerate(): 返回一个包含正在运行的线程的list。正在运行指线程启动后、结束前，不包括启动前和终止后的线程。
  # threading.activeCount(): 返回正在运行的线程数量，与len(threading.enumerate())有相同的结果。
```



## Join & setDaemon  🍀

在说这两个方法之前 , 需要知道主线程与子线程的概念

主线程 : 当一个程序启动时 , 就有一个进程被操作系统创建 , 与此同时一个线程也立刻运行 , 该线程通常叫做程序的主线程

子线程 : 因为程序是开始时就执行的 , 如果你需要再创建线程 , 那么创建的线程就是这个主线程的子线程

` 主线程的重要性体现在两方面 : 1. 是产生其他子线程的线程 ; 2. 通常它必须最后完成执行比如执行各种关闭作` 

` 在Python中线程的一些机制与C/C++不同 , 在C/C++中 , 主线程结束后 , 其子线程会默认被主线程kill掉 . 而在Python中 , 主线程结束后 , 会默认等待子线程结束后 , 主线程才退出` 

> **Join**

在上面的线程的创建时 , 获取线程名并不是在最后执行的 , 而是遇到sleep阻塞自动切换执行的 , 而sleep(2)则是在最后执行的 , 如果还不明白在看下面一个例子

遇到阻塞自动切换

```python
import threading
import time
# 定义线程要执行的函数
def run(name):
    # 打印内容
    print("I am %s" % name)
    # 睡两秒
    time.sleep(2)
    # 睡完继续起来干活
    print("When I'm done, I'm going to keep talking...")
if __name__ == '__main__':
    # 创建一个线程实例
    lyon = threading.Thread(target=run, args=('Lyon',))
    # 创建另一个线程实例
    kenneth = threading.Thread(target=run, args=('Kenneth',))
    # 启动线程
    lyon.start()
    # 启动另一个线程
    kenneth.start()
    # 我是主线程,我应该最后执行的
    print("I was the main thread, and I ended up executing")
'''
执行结果:
I am Lyon
I am Kenneth
I was the main thread, and I ended up executing
When I'm done, I'm going to keep talking...
When I'm done, I'm going to keep talking...
结果分析:
第一行打印了 I am Lyon,这没问题第一个线程启动了
第二行打印了 I am Kenneth,这就有问题了,这明明是第二个线程中的事情,我擦我的第一个线程都没执行完
第三行打印了 I was the main thread, and I ended up executing,你牛逼把我主线程的事都打印了
睡了两秒,看来是遇到阻塞自动切换了
最后打印了两个线程中的 When I'm done, I'm going to keep talking...
'''
```

在很多情况下 , 我们需要的是让各个线程执行完毕后 , 才接着往下执行 , 也就是不跳过阻塞 , 就让它等下去 , 这个时候就需要用join了

join : 阻塞调用程序 , 知道join () 方法的线程调用终止 , 才会继续往下执行

上面加上join后

```python
import threading
import time
def run(name):
    print("I am %s" % name)
    time.sleep(2)
    print("When I'm done, I'm going to keep talking...")
if __name__ == '__main__':
    lyon = threading.Thread(target=run, args=('Lyon',))
    kenneth = threading.Thread(target=run, args=('Kenneth',))
    lyon.start()
    lyon.join()
    kenneth.start()
    kenneth.join()
    print("I was the main thread, and I ended up executing")
'''
执行结果:
I am Lyon
# sleep 2 seconds
When I'm done, I'm going to keep talking...
I am Kenneth
# sleep 2 seconds
When I'm done, I'm going to keep talking...
I was the main thread, and I ended up executing
'''
```

程序按照我们的意愿按顺序执行了

> **setDaemon** 

无论进程还是线程 , 都遵循 : 守护进程 (线程) 会等待主进程 (线程) 运行完毕后被销毁

对于主进程来说 , 运行完毕指的是主进程代码运行完毕

对于主线程来说 , 运行完毕指的是主线程所在的进程内所有非守护线程统统运行完毕

setDaemon() 与 join() 基本上是相对的 , join会等子线程执行完毕 ; 而setDaemon则不会等 , 只要主线程执行完了 ,  我才不管你子线程执没执行完毕 , 统统给我回收 , 这样才能保证进程能正常结束

setDaemon设置守护线程

```python
import threading
import time
def run(name):
    print("I am %s" % name)
    time.sleep(2)
    print("When I'm done, I'm going to keep talking...")
if __name__ == '__main__':
    lyon = threading.Thread(target=run, args=('Lyon',))
    kenneth = threading.Thread(target=run, args=('Kenneth',))
    # 设置守护线程,必须在启动前设置
    lyon.setDaemon(True)
    # 启动线程
    lyon.start()
    # 设置守护线程
    kenneth.setDaemon(True)
    kenneth.start()
    print("I was the main thread, and I ended up executing")
'''
执行结果:
I am Lyon
I am Kenneth
I was the main thread, and I ended up executing
结果说明:
主线程一旦执行完毕,那么守护线程就一并退出,不管被守护线程是否执行完毕
所以lyon和kenneth两个子线程并没有执行完毕,如果在主线程中在加上sleep(5),
即超过子线程阻塞,那么这两个子线程就能执行完毕了
'''
```

将主线程设置为守护线程

```python
import threading
import time
def run(num):
    print("I like num %d" % num)
    time.sleep(2)
    print("When I'm done, I'm going to keep talking...")
def main():
    for i in range(1, 6):
        # 创建线程实例
        t = threading.Thread(target=run, args=(i,))
        # 启动线程
        t.start()
        # 阻塞调用
        t.join()
if __name__ == '__main__':
    # 创建一个主线程
    m = threading.Thread(target=main, args=[])
    # 设置为守护线程
    m.setDaemon(True)
    # 启动线程
    m.start()
    # 等待其子线程执行完毕后,再8秒退出
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
结果说明:
子线程并没有执行完毕,主线程退出,守护线程一并退出
'''
```

## Python GIL  🍀

```python
'''
In CPython, the global interpreter lock, or GIL, is a mutex that prevents multiple 
native threads from executing Python bytecodes at once. This lock is necessary mainly 
because CPython’s memory management is not thread-safe. (However, since the GIL 
exists, other features have grown to depend on the guarantees that it enforces.)
'''
```

基本意思是说 , 在CPython解释器中 , 同一个进程下开启的多线程 , 同一时刻只能有一个线程执行 , 无法利用多核优势

GIL并不是Python的一种特性 , 它是在实现Python解释器(CPhthon)时引入的一个概念 , 就比如同一段代码可以通过CPython , PyPy , Psyco等不同的Python执行环境来执行 , 像JPython中就没有GIL . 由于CPython是大部分环境下默认的Python执行环境 , 所以在很多人的概念里CPython就是Python , 但是要记住 , GIL并不是Python的特性 , Python完全可以不依赖GIL

> **GIL** 

GIL本质就是一把互斥锁 , 即会将并发运行变成串行 , 以此来控制同一时间内共享数据只能被一个任务进行修改 , 从而保证数据的安全性

` 保护不同的数据时 , 应该加不同的锁`  , GIL是解释器级别的锁 , 又叫做全局解释器锁

CPython加入GIL主要的原因是为了降低程序的开发复杂度 , 让你不需要关心内存回收的问题 , 你可以理解为Python解释器里有一个独立的线程 , 每过一段时间它起wake up做一次全局轮询看看哪些内存数据是可以被清空的 , 此时你自己的程序 里的线程和Python解释器自己的线程是并发运行的 , 假设你的线程删除了一个变量 , py解释器的垃圾回收线程在清空这个变量的过程中的clearing时刻 , 可能一个其它线程正好又重新给这个还没来及得清空的内存空间赋值了 , 结果就有可能新赋值的数据被删除了 , 为了解决类似的问题 , Python解释器简单粗暴的加了锁 , 即当一个线程运行时 , 其它人都不能动 , 这样就解决了上述的问题 , 这可以说是Python早期版本的遗留问题 . 毕竟Python出来的时候 , 多核处理还没出来呢 , 所以并没有考虑多核问题

以上就可以说明 , Python多线程不适合CPU密集型应用 , 但适用于IO密集型应用

##Lock  🍀

多线程与多进程最大的不同在于 , 多进程中 , 同一个变量 , 各自有一份拷贝存在于每个进程中 , 互不影响 , 但是在多线程中 , 所有变量对于所有线程都是共享的 , 因此 , 线程之间共享数据最大的危险在于多个线程同时修改一个变量 , 那就乱套了 , 所以我们需要GIL一样 , 来锁住数据

上面说了 , 保护不同的数据 , 要加不同的锁 , GIL是为了保护解释器的数据 , 明显我们还需要保护用户数据的锁

所以为了保证用户数据的安全 , 我们需要另一个锁 , 互斥锁(Mutex)

无锁版本

```python
# 线程的调度是由操作系统决定的,一旦线程交替执行,并且次数足够多,那么就可能出问题了
# 直接用廖大大的例子,地址:www.liaoxuefeng.com
import threading
# 假定这是你的银行存款:
balance = 0
def change_it(n):
    # 先存后取，结果应该为0:
    global balance
    balance = balance + n
    balance = balance - n
def run_thread(n):
    for i in range(100000):
        change_it(n)
for j in range(10000):
    t1 = threading.Thread(target=run_thread, args=(5,))
    t2 = threading.Thread(target=run_thread, args=(8,))
    # 这里跟join的位置有关系,因为join也是可以实现锁的功能的,下面说
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(balance,end="")
'''
执行结果:
0
0
5
5
5
# 这里我就只给出5次的结果,因为5次就已经出现错误了
# 正常情况下数据不混乱,结果应该一直为0
'''
```

加锁版本

```python
import threading
# 假定这是你的银行存款:
balance = 0
def change_it(n):
    # 先存后取，结果应该为0:
    global balance
    balance = balance + n
    balance = balance - n
# 创建一把锁
lock = threading.Lock()
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
for j in range(10000):
    t1 = threading.Thread(target=run_thread, args=(5,))
    t2 = threading.Thread(target=run_thread, args=(8,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(balance)
'''
执行结果:
0
# 这里的结果一直都是0,So我就只写出一个结果了 
'''
```

**join vs lock** 

上面第一个无锁版本的例子中 , 其实join()就可以实现我们想要的功能 , 只需要各个线程后面不加多余的东西直接接join()就行 , 因为我们知道join()的功能是进行阻塞 , 一加join() , 肯定其他就没有线程能动了 , 上面例子中故意将`t1.join()` 加在了`t2.start()`的后面 , 就是为了能让t2"有机可趁" , 既然`join()` 就可以实现 , 那我们还要锁干嘛?

我们应该想想 , join实现的原理 , join会使线程进行阻塞 , 也就是说会让真个线程变成完全串行的 , 既然只有一个线程在进行操作 , 那么它肯定就不会乱 , 但是使用join影响了执行效率 , 所以我们想能不能只让线程中的一部分串行? 答案是能的 , 就是利用互斥锁 , 想让哪里串行就让哪里串行

PS : `Python3.x`好像会自动加锁 , 但是`Python2.x`是不会的 , 写的时候还是都加上把 , 保证安全性

## RLock  🍀

RLock叫做递归锁 , 在说之前先说一个死锁问题

进程也有死锁和递归锁 , 所谓死锁 : 是指两个或两个以上的进程或线程在执行过程中 , 因争夺资源而造成的一种互相等待的现象 , 若无外力作用 , 他们都将无法推进下去 . 此时称系统处于死锁状态或系统产生了死锁 , 这些永远在互相等待的进程称为死锁进程 , 如下

```python
import threading
import time
# 创建两个锁
mutexA = threading.Lock()
mutexB = threading.Lock()
class MyThread(threading.Thread):
    # 重构run方法
    def run(self):
        self.func1()
        self.func2()
    def func1(self):
        # 获取锁A
        mutexA.acquire()
        print("\033[31m%s get mutexA...\033[0m" % self.name)
        # 获取锁B
        mutexB.acquire()
        print("\033[33m%s get mutexB...\033[0m" % self.name)
        # 释放锁B
        mutexB.release()
        # 释放锁A
        mutexA.release()
    def func2(self):
        mutexB.acquire()
        print("\033[35m%s get mutexB...\033[0m" % self.name)
        # 睡1秒
        time.sleep(1)
        mutexA.acquire()
        print("\033[37m%s get mutexA...\033[0m" % self.name)
        mutexA.release()
        mutexB.release()
if __name__ == '__main__':
    for i in range(10):
        t = MyThread()
        t.start()
'''
执行结果:
Thread-1 get mutexA...
Thread-1 get mutexB...
Thread-1 get mutexB...
Thread-2 get mutexA...
# 到这里整个程序就永远等着了
结果说明: 
首先执行了func1,没有阻塞,顺利执行完毕
然后执行func2,获取了锁B后就开始睡1一秒,也就是阻塞开始
于是系统自动切换,再次执行了func1,而B的锁在阻塞前没释放
最后func1中的mutexB.acquire()就一直等前面一个线程把锁给释放了
等到天荒地老,海枯石烂,也等不到了
'''
```

为了解决这样的问题 , 于是就有了递归锁 , 在Python中为了支持在同一线程中多次请求同一资源 , Python提供了可重入锁RLock

这个RLock内部维护着一个Lock和一个counter变量 , counter记录了acquire的次数 , 从而使得资源可以被多次require . 直到一个线程所有的acquire都被release , 其他的线程才能获得资源

RLock版本

```python
# 仅仅只需如下修改
mutexA = threading.Lock()
mutexB = threading.Lock()
# 以上两行修改为
mutexA = mutexB = threading.RLock()
# 注意如果仅仅修改后部分,即将Lock() -> RLock()是不行的,那样等于创建了两把递归锁
```

## queue  🍀

我们可以使用队列处理线程编程中多个线程之间交换的安全问题

在queue中有三种模式 , Queue (先进先出 , FIFO) , LifoQueue (后进先出 , LIFO) , 还有一个可以设置优先级的队列PriorityQueue

Queue

```python
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
```

LifoQueue

```python
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
```

PriorityQueue

```python
import queue
q = queue.PriorityQueue()
# put进入一个元组,元组的第一个元素是优先级,越小优先级越高
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
```

更多请阅读Python标准库目录下的queue模块内容

## Producer-Consumer  🍀

**生产者 - 消费者问题**  

又称有界缓冲区问题 , 在进程中 , 两个进程共享一个公共的固定大小的缓冲区 , 其中一个是生产者 , 将信息放入缓冲区 ; 另一个是消费者 , 从缓冲区取出信息 . 问题在于当缓冲区满时 , 而此时生产者还想向其中放入一个新的数据项的情况 ; 相反 , 当缓冲区为空时 , 消费者视图从缓冲区中取数据 , 该如何去解决? 

为了解决这个问题于是引入了生产者和消费者模式 , 基本思路也是如进程中睡眠和唤醒

**生产者消费模式** 

通过一个容器来解决生产者和消费者的强耦合问题 . 生产者与消费者彼此之间不直接通讯 , 而通过阻塞队列来进行通讯 , 所以生产者生产完数据之后不用等待消费者处理 , 直接扔给阻塞队列 , 消费者不找生产者要数据 , 而是直接从阻塞队列里取 , 阻塞队列就相当于一个缓冲区 , 平衡了生产者和消费者的处理能力

在并发编程中使用生产者和消费者模式能解决绝大多数并发问题 , 在线程世界里 , 生产者就是生产数据的线程 , 消费者就是消费数据的线程 . 以下有两个生产者消费者问题的例子

基础版本

```python
import threading
import queue
def producer():
    for i in range(10):
        # 进行生产,放入队列
        q.put("%d bottle of milk" % i)
    print("Start waiting for all the milk to be taken...")
    q.join()
    print("All the milk was taken out...")

def consumer(name):
    # 队列中有就取
    while q.qsize() > 0:
        print("%s got %s" % (name, q.get()))
        q.task_done()
# 创建一个队列对象
q = queue.Queue()
p = threading.Thread(target=producer,)
p.start()
c1 = consumer("Lyon")
```

生产与消费同时进行

```python
import time
import random
import queue
import threading
q = queue.Queue()
def Producer(name):
  count = 1
  while count < 20:
    time.sleep(random.randrange(3))
    # 将数据放入队列
    q.put(count)
    print('Producer %s has produced %s bun...' % (name, count))
    count += 1
def Consumer(name):
  count = 1
  while count < 20:
    time.sleep(random.randrange(4))
    # 不为空就取,为空就提示
    if not q.empty():
        # 从队列中取出信息
        data = q.get()
        print(data)
        print('\033[32;1mConsumer %s has eat %s bun...\033[0m' % (name, data))
    else:
        print("No bun anymore...")
    count += 1
p1 = threading.Thread(target=Producer, args=('Lyon',))
c1 = threading.Thread(target=Consumer, args=('Kenneth',))
p1.start()
c1.start()
```

## Semaphore  🍀

信号量(Semaphore) , 引入一个整型变量来累计线程的唤醒次数 , threading模块中 , 有一个Semaphore类管理一个内置的计数器 , 每当调用acquire()时内置计数器 -1 ;调用release()时内置计数器 +1;计数器不能小于0 ; 当计数器等于0时 , acquire()将阻塞线程知道其他线程调用release()

一次最多连接5个线程

```python
import threading
import time
def func():
    # 内置计数器 -1
    sm.acquire()
    print('%s get semaphores' % threading.current_thread().getName())
    time.sleep(2)
    # 内置计数器 +1
    sm.release()
if __name__ == '__main__':
    # 一次最多只能有5个线程获取信号量
    sm = threading.Semaphore(5)
    for i in range(10):
        t = threading.Thread(target=func)
        t.start()
```

利用信号量可以解决生产者与消费者问题 , 《现代操作系统中》一书中进行了简单的实现

## Event  🍀

在多线程中 , 每个线程都是互相独立的 , 互不影响 , 如果我们需要通过某个线程的状态来控制程序的执行过程 , 是非常难的 . 为了解决这些问题 , 我们就可以使用threading中的Event对象来实现我们的目的

Event对象中包含一个可由线程设置的信号标志 , 它允许线程等待某些事件的发生 . 在初始情况下 , Event对象中的信号标志被设置为假 ; 如果有线程等待一个Event对象 , 而这个Event对象的标志为假 , 那么这个线程将会被一直阻塞直至该标志为真 . 一个线程如果将一个Event对象的信号标志设置为真 , 它将唤醒所有等待这个Event对象的线程 . 如果一个线程等待一个已经被设置为真的Event对象 , 那么它将忽略这个事件 , 继续执行

| 方法            | 描述                                       |
| ------------- | ---------------------------------------- |
| Event.isSet() | 返回Event的状态 , isSet == is_set             |
| Event.wait()  | 如果Event.isSet() == False将阻塞线程            |
| Event.set()   | 设置Event的状态值为True , 所有阻塞池中的线程激活进入就绪状态 , 等待操作系统调度 |
| Event.clear() | 回复Event的状态值为False                        |

解决重复连接问题

```python
import threading
import time
import random
def conn_mysql():
    count = 1
    while not event.is_set():
        # 大于3次主动触发TimeoutError
        if count > 3:
            raise TimeoutError('Connection timeout...')
        print('%s %sth attempt to connect' % (threading.current_thread().getName(), count))
        # 阻塞0.5秒
        event.wait(0.5)
        count += 1
    print('%s connect successfully' % threading.current_thread().getName())
def check_mysql():
    print('%s is checking mysql' % threading.current_thread().getName())
    time.sleep(random.randint(2, 4))
    # 激活线程
    event.set()
if __name__ == '__main__':
    event = threading.Event()
    conn1 = threading.Thread(target=conn_mysql)
    conn2 = threading.Thread(target=conn_mysql)
    check = threading.Thread(target=check_mysql)
    conn1.start()
    conn2.start()
    check.start()
```

## Condition  🍀

使线程等待 , 只有满足条件时 , 才释放线程

```python
import threading
def condition_func():
    ret = False
    inp = input('>>>')
    # 只有当inp等于1时才会执行
    if inp == '1':
        ret = True
    return ret
def run(n):
    con.acquire()
    con.wait_for(condition_func)
    print("run the thread: %s" %n)
    con.release()
if __name__ == '__main__':
    con = threading.Condition()
    for i in range(10):
        t = threading.Thread(target=run, args=(i,))
        t.start()
```

## Timer  🍀

threading模块中还有一个Timer类 , 可以指定时间后执行某操作

```python
import threading
def hello1():
    print("I am Lyon")
def hello2():
    print("Hello, future")
# 1秒后执行
t1 = threading.Timer(1, hello1)
# 两秒后执行
t2 = threading.Timer(2,hello2)
t1.start()
t2.start()
```