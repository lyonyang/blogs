# Flask - 源码之本地线程


<extoc></extoc>

## 介绍  🍀

Flask 中的一条设计原则是保持任务的简单 , 任务的实现不需要花费太多的代码 , 也不会限制到你 ; 例如 , 为了保持线程安全 , Flask 使用了本地线程 `(thread-local)` , 所以在一个请求中你不需要在函数之间传递对象 

本地线程 `(thread-local)` : 希望不同的线程对于内容的修改只在线程内发挥作用 , 线程之间互不影响

## Threading的Local  🍀

我们可以通过一个例子来看看 , 本地线程是如何实现的 , 示例如下 : 

```python
import threading

data = threading.local()
data.number = 1
print(data.number)
log = []


def func():
    data.number = 2
    log.append(data.number)


thread = threading.Thread(target=func)
thread.start()
thread.join()
print(log)
print(data.number)
"""
执行结果:
1
[2]  # 在线程内data.number变成了其他的值
1    # 但是没有影响到开始设置的值
"""
```

之所以会有这样的结果 , 都是因为 `threading.local()` 在作祟 , 以上面的代码为例 , 我们来分析一下这个 `local` , 其源码如下 : 

```python
class local:
    # 仅允许_local__iml和__dict__进行绑定
    # 其他属性绑定将会触发AttributeError
    __slots__ = '_local__impl', '__dict__'

    def __new__(cls, *args, **kw):
        if (args or kw) and (cls.__init__ is object.__init__):
            raise TypeError("Initialization arguments are not supported")
        self = object.__new__(cls)
        # _localimpl为管理本地线程dicts属性的类
        impl = _localimpl()
        impl.localargs = (args, kw)
        impl.locallock = RLock()
        object.__setattr__(self, '_local__impl', impl)
        # 初始化_localimpl对象的dicts属性
        impl.create_dict()
        return self

    def __getattribute__(self, name):
        """ 此处内容省略 """

    def __setattr__(self, name, value):
        """ 此处内容省略 """

    def __delattr__(self, name):
        """ 此处内容省略 """
```

我们需要先弄明白 `impl.create_dict()` 做了什么操作 , 因为这里是本地线程的一个关键点 , 还有一个关键点就是 `__setattr__` 方法 , 先看看 `impl.create_dict()` :

```python
def create_dict(self):
    """
    为当前线程创建一个新字典,并返回它
    """
    localdict = {}
    # self.key:{ id(Thread) -> (ref(Thread), thread-local dict) }
    key = self.key
    # 获取当前线程对象
    thread = current_thread()
    # 获取当前线程对象id
    idt = id(thread)
    def local_deleted(_, key=key):
        thread = wrthread()
        if thread is not None:
            del thread.__dict__[key]
    def thread_deleted(_, idt=idt):
        local = wrlocal()
        if local is not None:
            dct = local.dicts.pop(idt)
    # 封装成ReferenceType对象
    wrlocal = ref(self, local_deleted)
    wrthread = ref(thread, thread_deleted)
    # 在当前线程对象的__dict__属性中,以线程id为key,wrlocal为value设置值
    # 以保存不同线程的状态
    thread.__dict__[key] = wrlocal
    
    # 以线程对象id为key,(ReferenceType,ReferenceType)对象为value
    # self为_localimpl对象
    # self.dicts数据形式如下:
    #     {2552096368904: (<weakref at 0x0000025234CE3B38; to '_MainThread' at 0x0000025234CC2908>, {'number': 1})}
    self.dicts[idt] = wrthread, localdict
    # 未设置值前localdict为空
    return localdict
```

此时 `impl.dicts` 属性已经有了 , 接下来回到我们的示例代码 , 当本地线程对象实例化完成之后 , 下一步就是设置属性 `data.number = 1` , 也就是会执行 `local` 对象的 `__setattr__` 方法 , 在上面我们把它给省略了 , 现在列出来 : 

```python
def __setattr__(self, name, value):
    if name == '__dict__':
        raise AttributeError(
            "%r object attribute '__dict__' is read-only"
            % self.__class__.__name__)
    with _patch(self):
        return object.__setattr__(self, name, value)
```

可以看到 , 它走了一个 `_patch` 方法 , 继续看看 `_patch` 的详细内容 : 

```python
# 该装饰器用于将_patch转换为上下文对象
@contextmanager
def _patch(self):
    impl = object.__getattribute__(self, '_local__impl')
    try:
        # 返回当前进程对象中的字典
        # 如:{'number': 1}
        dct = impl.get_dict()
    except KeyError:
        dct = impl.create_dict()
        args, kw = impl.localargs
        self.__init__(*args, **kw)
    # impl.locallock = RLock()
    # RLock是一个上下文对象
    with impl.locallock:
        # 设置属性到local对象
        object.__setattr__(self, '__dict__', dct)
        yield
```

到这里我们可以看出 , 如果在 `_localimpl` 对象的 `dicts` 中不存在以线程 id 为 key 的键值对 , 那么必定会调用 `create_dict()` 来为其创建一个 , 创建形式如下 : 

```python
# key为当前线程对象id,wrlocal为ReferenceType对象
threading.current_thread().__dict__[key] = wrlocal

# 随后以当前线程对象id为key,wrthread,localdict为value存入_localimpl.dicts中
# whthread中存入了当前线程对象,localdict为设置属性字典
# self.dicts[idt] = wrthread, localdict

# 当然local对象的__dict__中也存在属性,因为最后调用了object的setattr方法
object.__setattr__(self, name, value)
```

本地线程的实现原理就是 , 数据的改变是在线程内部进行的 , 在每一个线程内部都有一个独立的字典 , 存放着那些数据 , 并且通过线程 id 和 dicts 属性 , 保存了不同线程的状态

## Werkzeug的Local  🍀

总而言之 , 本地线程的实现 , 相当于在线程内部建立了一个数据副本 , 只不过我们需要一些手段来保存好这些线程的状态

上面分析的是 `threading` 中的本地线程 , 而 Flask 基于的 `Werkzeug`  , 它自己实现了本地线程 , 也就是 `werkzeug.local.Local` 对象 : 

```python
class Local(object):
    __slots__ = ('__storage__', '__ident_func__')

    def __init__(self):
        # 此处不能使用self.__storage__ = {}来初始化,原因:
        #    1. 首先会调用self.__setattr__
        #    2. 随后执行self.__ident_func__(),于是会调用self.__getattr__
        #    3. self.__storage__[self.__ident_func__()][name]会再次调用__getattr__
        #    4. 于是,这里将永远递归下去
        object.__setattr__(self, '__storage__', {})
        object.__setattr__(self, '__ident_func__', get_ident)

    def __iter__(self):
        return iter(self.__storage__.items())

    def __call__(self, proxy):
        """Create a proxy for a name."""
        return LocalProxy(self, proxy)

    def __release_local__(self):
        self.__storage__.pop(self.__ident_func__(), None)

    def __getattr__(self, name):
        try:
            return self.__storage__[self.__ident_func__()][name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        # 获取线程/协程标识符
        ident = self.__ident_func__()
        storage = self.__storage__
        try:
            storage[ident][name] = value
        except KeyError:
            # 以线程/协程标识符为key,属性键值对为value
            storage[ident] = {name: value}

    def __delattr__(self, name):
        try:
            del self.__storage__[self.__ident_func__()][name]
        except KeyError:
            raise AttributeError(name)
```

相对来讲 , `Werkzeug` 自己实现的本地线程 , 可能比 `threading` 提供的本地线程更加简单明了 , 两者区别如下 : 

- Werkzeug 使用了自定义的 `__storage__` 保存不同线程下的状态
- Werkzeug 提供了释放本地线程的 `release_local` 方法
- Werkzeug 使用 `get_ident` 函数来获取线程/协程标识符

在 `werkzeug.local` 中 , `gent_ident` 的导入如下 : 

```python
try:
    from greenlet import getcurrent as get_ident
except ImportError:
    try:
        from thread import get_ident
    except ImportError:
        from _thread import get_ident
```

如果已经安装了 `Greenlet` , 会优先使用 `Greenlet` , 否则将使用系统线程 ; `Greenlet` 是以 C 扩展模块形式接入 Python 的轻量级协程 , 它运行在操作系统进程的内部 , 但是会被协作式地调度

## 小结  🍀

Werkzeug 基于自己实现的 `Local` 还实现了两种数据结果 : 

- LocalStack : 基于 `werkzeug.local.Local` 实现的栈结果 , 可以将对象推入 , 弹出 , 也可以快速拿到栈顶对象
- LocalProxy : 作用和名字一样 , 最标准的代理模式 , 构造此结构时接收一个可以调用的参数 (一般为函数) , 这个函数执行后就是通过 `LocalStack` 实例化的栈的栈顶对象 ; 对于 LocalProxy 对象的操作实际上都会转发到这个栈顶对象 (也就是一个 `thread-local` 对象) 上面

本地线程是 Flask 中非常重要的一部分 , 因为在请求处理时 , 为了解决请求对象在每一个视图函数传递 (意味着每个视图函数需要像 Django 那样添加一个 request 参数) 的问题 , Flask 巧妙地使用上下文把某些对象变为全局可访问 (实际上是特定环境的局部对象的代理) , 再配合本地线程 , 这样每个线程看到的上下文对象都是不同的

**`本地线程`** 与 **`上下文`** 的结合 , 解决了 Flask 请求的问题