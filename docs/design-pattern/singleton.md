# 单例模式








<extoc></extoc>

## 定义

单例模式 ( `Singleton Pattern` ) 

确保某一个类只有一个实例 , 而且自行实例化并向整个系统提供这个实例 ( `Ensure a class has only one instance, and provide a global point of access to it.` )

## 场景

在一个系统中 , 要求一个类有且仅有一个对象 , 如果出现多个对象就会出现 "不良反应" , 可以采用单例模式 

如 : 

- 在整个项目中需要一个共享访问点或共享数据
- 要生成唯一数据
- 创建一个对象需要消耗的资源过多 , 如要访问 IO 和数据库等资源
- 需要定义大量的静态常量和静态方法 (如工具类) 的环境

我们可能最多见的就是需要共享数据 , 比如在项目中的配置数据 , 又比如 Web 框架中的路由

## 实例

要实现单例模式 , 即保证一个类仅有一个实例 , 并提供一个访问它的全局访问点

### Module

Python 中的 module 天生就是单例 , 至于为什么 , 你应该去看看 [compiled-python-file](https://docs.python.org/3.6/tutorial/modules.html#compiled-python-files)

**singleton.py**

```python
class Singleton(object):
    pass

singleton = Singleton()
```

使用

```python
from singleton import singleton
```

### \_\_new__

Python 中的对象将有 `__new__` 来开辟空间创建实例

```python
import threading

class Singleton(object):
    _threading_lock = threading.RLock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._threading_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = object.__new__(cls)
        return cls._instance
```

Python 是支持多线程的 , 所以为了线程安全 , 加上锁

### Metaclass

使用元类来实现单例模式 , 实际上就是控制 `class()` 的行为 , 也就是 `__call__` 魔术方法

如果对于 `metaclass` 不懂 , 你可以看我的另一篇博客 [《Python之路 - 元类》](<https://lyonyang.github.io/blogs/01-Python/09-In-Depth/09-Python%E4%B9%8B%E8%B7%AF%20-%20%E5%85%83%E7%B1%BB.html>)

```python
class SingletonMeta(type):
    
    _instances = {}

    def __call__(self, *args, **kwargs):
        if self not in self._instances:
            self._instances[self] = super(SingletonMeta, self).__call__(*args, **kwargs)
        return self._instances[self]

class Singleton(metaclass=SingletonMeta):
    pass

singleton = Singleton()
```

元类创建类本身就是线程安全的 , 所以你并不需要担心抢占资源的问题

### 类装饰器

```python
def singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton

@singleton
class Singleton:
    pass
```

使用类装饰器 , 实际上就是把类转换成一个函数对象 , 因此跟实例的创建关系不大 , 因为从始至终也就实例化了一次 , 而且它是线程安全的

### 类方法

通过我们自定义的方法来获取对象 , 而不通过实例化的途径

```python
class Singleton(object):

    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = cls(*args, **kwargs)
        return cls._instance

singleton = Singleton.instance()
```

虽然这种方式也能实现单例模式 , 但是它不是线程安全的 , 就算在方法里加了锁 , 也不是线程安全的 , 这里可能跟 Python 的类的加载机制有关 , 不深究了

**注意 : 在测试过程中 , 千万要把 Python 的垃圾回收这一问题隔离 , 也就是说实例不要一实例化之后就丢弃 , 否则可能会出现无效的结果**

