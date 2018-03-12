# Python之路 - 反射

## 介绍

反射主要是指程序可以访问、检测和修改它本身状态或行为的一种能力 

Python面向对象中的反射是通过字符串的形式来操作对象相关的属性 , 在Python中一切皆对象 , 并且只要是对象就可以使用反射

## hasattr  🍀

判断对象中是否具有给定名称的属性

```python
def hasattr(*args, **kwargs): # real signature unknown
    """
    Return whether the object has an attribute with the given name.  
    This is done by calling getattr(obj, name) and catching AttributeError.
    """
    pass
```

实例1

```python
# 定义一个字符串
name = 'lyon'
# 查看是否具有给定名称的属性
bool = hasattr(name,'__len__')
# 打印bool
print(bool)
# 执行结果:True
'''
说明:很多初学者可能一直不理解为什么说Python里一切皆对象,因为没有意识到,在Python中str、list、int ...等这些数据类型,其实就是用class写出来的一个模型,那么既然是类就会有属性这一说,就可以利用反射来操作对象了
'''
```

实例2

```python
import sys
def s1():
    pass
def s2():
    pass
this_modules = sys.modules[__name__]
print(type(this_modules),hasattr(this_modules,'s1'))
# 执行结果:<class 'module'> True
```

## getattr  🍀

从一个对象中获取属性名称

```python
def getattr(object, name, default=None): # known special case of getattr
    """
    Get a named attribute from an object; getattr(x, 'y') is equivalent to x.y.
    When a default argument is given, it is returned when the attribute doesn't
    exist; without it, an exception is raised in that case.
    """
    pass
```

实例

```python
class A:
    def __init__(self,name,age):
        self.name = name
        self.age = age
    def hello(self):
        print('hello {}'.format(self.name))
# 创建一个实例a        
a = A('Lyon',18)
# 获取静态属性age
age = getattr(a,'age')
# 打印age
print(age)
# 获取动态属性hello,即方法
hello = getattr(a,'hello')
# 执行hello
hello()
# 如果不存在就需要设置default参数,否则就报错
birthday = getattr(a,'birthday','today')
# 打印birthday,即为default参数
print(birthday)
'''
执行结果:
18
hello Lyon
today
'''
```

## setattr  🍀

定义属性

```python
def setattr(x, y, v): # real signature unknown; restored from __doc__
    """
    Sets the named attribute on the given object to the specified value.   
    setattr(x, 'y', v) is equivalent to ``x.y = v''
    """
    pass
```

实例

```python
class B:
    def __init__(self):
		pass
b = B()
# 新增属性,如果存在即为修改
setattr(b, 'age', 18)
# 打印age属性
print(b.age)
# 新增add方法
setattr(b, 'add', lambda age: age + 1)
# 修改age属性
b.age = b.add(b.age)
# 打印age属性
print(b.age)
'''
执行结果:
18
19
'''
```

## delattr  🍀

删除对象中的属性

```python
def delattr(x, y): # real signature unknown; restored from __doc__
    """
    Deletes the named attribute from the given object.
    delattr(x, 'y') is equivalent to ``del x.y''
    """
    pass
```

实例

```python
class C:
    def __init__(self,name,age):
		self.name = name
        self.age = age
    def add(self):
        self.age = self.age + 1
c = C('Lyon',18)
# 删除c中的
delattr(c,'name')
# print(c.name)   报错
delattr(c,'add')
# c.add()   报错
```