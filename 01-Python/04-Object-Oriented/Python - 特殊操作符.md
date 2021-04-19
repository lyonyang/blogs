# Python - 特殊操作符


<extoc></extoc>

## 介绍  🍀

在 Python 中 , 我们自定义类都是基于 Object 对象实现的 , 而在 Object 对象中有一些特殊的操作符 (`__method__`) 控制着整个对象的行为 , 所以 , 如果我们想对对象的行为进行控制 , 我们就需要自己来实现这些方法 ; 当然很多人称这些方法为 Python 魔法方法 (魔术方法) 

下面 , 看看这些方法吧

## 基本行为  🍀

| 操作符       | 控制行为                | 调用说明                                                     |
| ------------ | ----------------------- | ------------------------------------------------------------ |
| `__new__`    | 对象创建                | `__init__` 只是用处初始化 , `__new__` 调用的结果会交给 `__init__` 进一步处理 |
| `__init__`   | 对象初始化              | 构造函数 , 进行属性设置                                      |
| `__del__`    | 对象删除                | 析构函数 , 进行对象的销毁                                    |
| `__repr__`   | 对象显示 , 针对对象     | 终端显示 , 返回值必须为字符串 , 实例见表下方                 |
| `__str__`    | 对象显示 , 针对 `print` | `print` 显示结果 , 返回值必须为字符串 , 如果未实现该方法 , `print` 将使用 `__repr__` |
| `__bytes__`  | 字节对象转换            | 返回值必须为一个bytes对象 , bytes(obj)                       |
| `__format__` | 格式化字符串            | 返回值必须为字符串对象 , format(obj)                         |
| `__lt__`     | `<` 运算                | `x < y ` , 返回布尔值 , 下同                                 |
| `__le__`     | `<=` 运算               | `x <= y `                                                    |
| `__eq__`     | `=` 运算                | `x == y `                                                    |
| `__ne__`     | `!=` 运算               | `x != y `                                                    |
| `__gt__`     | `>` 运算                | `x > y `                                                     |
| `__ge__`     | `>=` 运算               | `x >= y`                                                     |
| `__hash__`   | 可哈希                  | 返回一个哈希对象 , hash(obj) , 注意 : 定义该方法同时应该定义 `__eq__` |
| `__bool__`   | 真假测试                | 返回布尔值                                                   |
| `__call__`   | 对象调用                | 在对象被调用时执行                                           |
| `__len__`    | `len()`                 | 使用 `len(obj)` 时被调用 , 为防止值测试抛出 ` OverflowError  ` , 必须定义 `__bool__()` |

`__repr__` 与 `__str__` 对比实例 : 

```python
# 类定义
class Foo:
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<repr:%s>' % self.name
    
    def __str__(self):
        return '<str:%s>' % self.name

# 终端结果
>>> obj = Foo('Lyon')
>>> obj
<repr:Lyon>
>>> print(obj)
<str:Lyon>
```

## 访问行为  🍀

| 操作符             | 控制行为         | 调用说明                                                     |
| ------------------ | ---------------- | ------------------------------------------------------------ |
| `__getattr__`      | `.` 属性访问运算 | 获取 `x.name` , `__getattribute__` 查询失败后被调用 , 下方实例进一步说明 |
| `__getattribute__` | `.` 属性访问运算 | 获取 `x.name` , 查询属性时被调用                             |
| `__setattr__`      | `.` 属性赋值运算 | `self.attr = value → self.__setattr__("attr", value)` , 见下方实例进一步说明 |
| `__delattr__`      | `.` 属性删除运算 | `del obj.name` 时被调用                                      |
| `__dir__`          | `dir` 运算       | `dir()` 调用时被调用 , 必须返回一个序列 , `dir()` 会将序列转换成 list 并排序 |

`__getattr__` 说明实例 : 

```python
# __getattr__
# 注意在定义__getattr__或者__getattribute__时,不要出现 self. 因为这样会导致递归调用
# 正确的方式是,使用object的__getattr__,__getattribute__,或者直接定义返回值
class Foo:

    def __init__(self, name):
        self.name = name

    def __getattr__(self, item):
        return 'Attribute <%s> fetch failure' % item

    def __getattribute__(self, item):
        # return object.__getattribute__(self, item)
        if item == "name":
            return 'Lyon'
        else:
            raise AttributeError(item)

x = Foo('Lyon')
print(x.name)
print(x.age)
"""
执行结果:
Lyon
Attribute <age> fetch failure
"""
```

 `__setattr__`  说明实例 : 

```python
# __setattr__
# 与__getattr__一样,在定义__setattr__时,不要出现 self. 因为这样会导致递归调用
# 正确的方式是,使用object的__setattr__,或者使用self.__dict__[key]
class Foo:

    def __init__(self, name):
        self.name = name

    def __setattr__(self, key, value):
        # object.__setattr__(self, key, value)
        if key == "name":
            self.__dict__[key] = value
        else:
            raise AttributeError(key + ' not allowed')


x = Foo('Lyon')
x.name = "Kenneth"
x.age = 18
print(x.__dict__)
"""
执行结果:
{'name': 'Kenneth'}
Traceback (most recent call last):
  File "test.py", line 19, in <module>
    x.age = 18
  File "test.py", line 11, in __setattr__
    raise AttributeError(key + ' not allowed')
AttributeError: age not allowed
"""
```

## 描述器行为  🍀

| 操作符         | 控制行为         | 调用说明                                                     |
| -------------- | ---------------- | ------------------------------------------------------------ |
| `__get__`      | `.` 对象访问运算 | 访问对象时被调用 , 对象访问意指 `.` 后面接的不是一个属性而是一个对象 , 见下方实例说明 |
| `__set__`      | `.` 对象赋值运算 | 对象赋值时被调用                                             |
| `__delete__`   | `.` 对象删除运算 | 对象删除时被调用                                             |
| `__set_name__` | 所有者创建       | 在创建所有者时被调用 , Python 3.6 新增                       |

`__get__` , `__set__` , `__delete__` 实例

```python
# 关于对象访问一说,是建立在两个的使用基础上的
# 单纯来讲,就是所有者类中的一个属性,是另一个类的实例
class Dependency:
    """ 附属类 """

    def __get__(self, instance, owner):
        print('%s.%s is called...' % ('Dependency', '__get__'))

    def __set__(self, instance, value):
        print('%s.%s is called...' % ('Dependency', '__set__'))

    def __delete__(self, instance):
        print('%s.%s is called...' % ('Dependency', '__delete__'))

class Owner:
    """ 所有者类 """
    dependency = Dependency()

o = Owner()
o.dependency
o.dependency = 'Lyon'
del o.dependency

"""
执行结果:
Dependency.__get__ is called...
Dependency.__set__ is called...
Dependency.__delete__ is called...
"""
```

`__set_name__` 是在上例 `Owner` 实例创建时被调用 , Python 3.6 新增

## 容器行为  🍀

| 操作符         | 控制行为         | 调用说明                                      |
| -------------- | ---------------- | --------------------------------------------- |
| `__getitem__`  | 序列方式访问     | `self[key]` 时被调用                          |
| `__missing__`  | 序列方式访问失败 | `self[key]` 时 key 不在字典中被调用           |
| `__setitem__`  | 序列方式赋值     | `self[key] = value` 时被调用                  |
| `__delitem__`  | 序列方式删除     | `del self[key]` 时被调用                      |
| `__iter__`     | 迭代环境         | 通过 `iter(obj)` 调用 , 如使用for循环进行遍历 |
| `__reversed__` | `reversed()`     | `reversed(obj)` 时被调用                      |
| `__contains__` | 成员关系 `in`    | `item in self` 时调用                         |

## 运算行为  🍀

```python
# 基本运算行为
object.__add__(self, other)              # +
object.__sub__(self, other)              # -
object.__mul__(self, other)              # *
object.__matmul__(self, other)           # @
object.__truediv__(self, other)          # /
object.__floordiv__(self, other)         # //
object.__mod__(self, other)              # %
object.__divmod__(self, other)           # divmod()
object.__pow__(self, other[, modulo])    # pow()  **
object.__lshift__(self, other)           # <<
object.__rshift__(self, other)           # >>
object.__and__(self, other)              # &
object.__xor__(self, other)              # ^
object.__or__(self, other)               # |

# 二进制运算行为
object.__radd__(self, other)             
object.__rsub__(self, other)             
object.__rmul__(self, other)             
object.__rmatmul__(self, other)          
object.__rtruediv__(self, other)        
object.__rfloordiv__(self, other)       
object.__rmod__(self, other)             
object.__rdivmod__(self, other)  
object.__rpow__(self, other)
object.__rlshift__(self, other)         
object.__rrshift__(self, other)          
object.__rand__(self, other)            
object.__rxor__(self, other)           
object.__ror__(self, other) 

# 加=运算行为
object.__iadd__(self, other)             # +=
object.__isub__(self, other)             # -=
object.__imul__(self, other)             # *=
object.__imatmul__(self, other)
object.__itruediv__(self, other)
object.__ifloordiv__(self, other)
object.__imod__(self, other)
object.__ipow__(self, other[, modulo])
object.__ilshift__(self, other)
object.__irshift__(self, other)
object.__iand__(self, other)
object.__ixor__(self, other)
object.__ior__(self, other)

# 一元算数运算
object.__neg__(self)
object.__pos__(self)
object.__abs__(self)
object.__invert__(self)

# complex(),int(),float()
object.__complex__(self)
object.__int__(self)
object.__float__(self)

# 整数值hex(X),bin(X),oct(X),o[X],O[X:]
object.__index__(self)

# round(),trunc(),floor(),ceil()
object.__round__(self[, ndigits])
object.__trunc__(self)
object.__floor__(self)
object.__ceil__(self)
```

## 上下文管理行为  🍀

| 操作符      | 控制行为       | 调用说明                       |
| ----------- | -------------- | ------------------------------ |
| `__enter__` | 进入上下文环境 | 使用with进入上下文环境时被调用 |
| `__exit__`  | 退出上下文环境 | 退出上下文环境时被调用         |

实例

```python
class Foo:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        # 返回值赋值给as指定变量
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('exc_type',exc_type)  # 异常类型
        print('exc_val',exc_val)    # 异常值
        print('exc_tb',exc_tb)      # 追溯信息
        return True                 # 返回值为True,那么异常会被清空,就好像啥都没发生一样,
                                    # with后的语句正常执行
                                    # 为False异常会抛出

with Foo('Lyon') as f:
    raise AttributeError('ignore exception')
print('over')
```

## \_\_slots\_\_  🍀

`__slots__` 的作用是阻止在实例化类时为实例分配dict , 默认情况下每个类都会有一个dict,通过`__dict__` 访问 , 这个dict维护了这个实例的所有属性 

作用 : 

- 减少内存使用
- 限制对实例添加新的属性

缺点 : 

- 不可被继承
- 不可动弹添加新属性

实例

```python
class Foo:
    __slots__ = ['name', 'age']

    def __init__(self, name, age):
        self.name = name
        self.age = age

f = Foo('Lyon', 18)
print(f.name)
print(f.age)

# 报错
f.sex = 'Man' 
```

更多 [Data model](https://docs.python.org/3/reference/datamodel.html#object.__index__)