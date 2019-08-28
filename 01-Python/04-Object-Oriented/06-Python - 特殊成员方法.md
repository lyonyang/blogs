# Python之路 - 特殊成员方法

## \_\_doc\_\_   🍀

查看类的描述信息

```python
class Foo:
    """
    这是一个类,什么都没有的类
    """
    def __init__(self):
        pass
print(Foo.__doc__)
# 执行结果: 这是一个类,什么都没有的类
```

## \_\_module\_\_  🍀

查看当前操作对象位于哪个模块

```python
# my_module.py
class Foo:
    def __init__(self):
        pass
```

```python
# test.py
from my_module import Foo
print(Foo.__module__)
# 执行结果: my_module
```

## \_\_class\_\_  🍀

查看对象的类

```python
class Foo:
    def __init__(self):
        pass
a = Foo()
print(a.__class__)
# 执行结果：<class '__main__.Foo'>
```

## \_\_new\_\_  \  \_\_init\_\_  🍀

\_\_new\_\_

创建对象时 , 自动触发执行 , 会返回当前对象的一个实例 

\_\_init\_\_ 

构造方法 , 创建对象时 , 自动触发执行 , 初始化对象的属性

python中的\_\_init\_\_ 在执行的时候 , 其实已经进行实例化了一次 , \_\_init\_\_ 有一个参数self , 就是\_\_new\_\_ 方法返回的实例

## \_\_del\_\_  🍀

析构方法 , 通当对象在内存中被释放时 , 自动触发执行

此方法一般无须定义 , 因为Python是一门高级语言 , 程序员在使用时无需关心内存的分配和释放 , 因为此工作都是交给Python解释器来执行 , 所以 , 析构方法是由解释器在进行垃圾回收时自动触发执行的 (Python采用 ' 引用计数 ' 的算法方式处理)

```python
class A:
    def __del__(self):
        print("析构方法执行!")
a = A()
# 自动回收触发析构方法
del a
# 执行结果: 析构方法执行!
```

## \_\_call\_\_   🍀

对象后面加括号 , 触发执行

构造方法的执行是由创建对象触发的 , 而对于\_\_call\_\_ 方法的执行是由对象后加括号触发的

```python
class A:
    def __init__(self):
        print("执行init")
    def __call__(self, *args, **kwargs):
        print("执行call")
a = A()  # init触发执行
a()  #call触发执行
```

## \_\_dict\_\_  🍀

查看类或对象中的所有成员

```python
class Person:
    __country = 'China'
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def func(self):
        print('func')
print("打印类成员".center(30, '-'))
for i in Person.__dict__:
    print('{} : {}'.format(i, Person.__dict__[i]))
p = Person("Lyon", 18)
print("打印对象成员".center(30, '-'))
for i in p.__dict__:
    print('{} : {}'.format(i, p.__dict__[i]))
'''
执行结果:
------------打印类成员-------------
__dict__ : <attribute '__dict__' of 'Person' objects>
__init__ : <function Person.__init__ at 0x000001F93FDDA048>
_Person__country : China
__module__ : __main__
__weakref__ : <attribute '__weakref__' of 'Person' objects>
func : <function Person.func at 0x000001F93FDDA6A8>
__doc__ : None
------------打印对象成员------------
name : Lyon
age : 18
'''
```

## \_\_str\_\_  \  \_\_repr\_\_  🍀

改变对象的字符串显示 , 这两个方法都只能返回字符串

\_\_str\_\_ ()用于显示给用户，而\_\_repr\_\_ ()用于显示给开发人员 , 也就是在终端下print(Class)则会调用`__repr__`，非终端下会调用`__str__`方法 , 并且\_\_str\_\_ 能够友好的显示\_\_repr\_\_ 方法返回的字符串 , 反之则不能友好的显示

```python
class A:
    def __str__(self):
        return "I am str"
a = A()
print(str(a))
print(repr(a))
'''
执行结果:
I am str
<__main__.A object at 0x000002007B3FE630>
'''
```

## item  🍀

\_\_getitem\_\_ , \_\_setitem\_\_ , \_\_delitem\_\_

用于索引操作 , 如字典 , 以上分别表示获取 , 设置 , 删除数据

```python
class Foo(object):
    def __getitem__(self, key):
        print('__getitem__', key)
    def __setitem__(self, key, value):
        print('__setitem__', key, value)
    def __delitem__(self, key):
        print('__delitem__', key)
obj = Foo()
result = obj['k']  # 触发执行 __getitem__
obj['name'] = 'Lyon'  # 触发执行 __setitem__
del obj['k']   #触发执行 __delitem__
'''
执行结果:
__getitem__ k
__setitem__ name Lyon
__delitem__ k
'''
```

## \_\_eq\_\_  🍀

定义类里的 == 行为

```python
class A(object):
    def __init__(self, name):
        self.name = name
    def __eq__(self, obj):
        return self.name == obj.name
a = A("Lyon")
b = A("Lyon")
print(a == b)
# 执行结果: True
```

一道面试题

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def __hash__(self):
        return hash(self.name)
    def __eq__(self, other):
        if self.name == other.name:
            return True
p_lst = []
for i in range(84):
    p_lst.append(Person('Lyon', i))
print(p_lst)
print(set(p_lst))
```

在定义一个类时，如果我们需要改写该类的\_\_eq\_\_ 函数，特别要注意的是它将会变为不可哈希对象，也就是说如果你将它放到哈希集会报错