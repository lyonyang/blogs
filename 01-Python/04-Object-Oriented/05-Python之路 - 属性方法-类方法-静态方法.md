# Python之路 - 属性方法,类方法,静态方法

## 属性方法  🍀

属性方法就是通过使用装饰器 `@property ` , 将一个方法变成一个静态属性 , 于是我们就可以通过访问属性 , 来或得一个方法的返回值

```python
from urllib.request import urlopen
class Web_page:
    def __init__(self, url):
        self.url = url
        self.__content = None
    # 将content方法变成属性
    @property
    def content(self):
        # 返回私有属性
        return self.__content if self.__content else urlopen(self.url).read()
con = Web_page('www.baidu.com')
res = con.content
print(res)
```

在property中为我们实现了三种方法 , get , set , delete

```python
class Foo:
    # 获取属性
    @property
    def AAA(self):
        print("执行了get方法")
    # 设定属性值
    @AAA.setter
    def AAA(self, value):
        print("执行了set方法")
    # 删除属性
    @AAA.deleter
    def AAA(self):
        print("执行了delete方法")
# 实例化
f = Foo()
# 获取属性
f.AAA
# 设置属性值,必须设置参数,即使不使用
f.AAA = 'aaa'
# 删除属性值
del f.AAA
'''
执行结果:
执行了get方法
执行了set方法
执行了delete方法
'''
```

换一种写法看看

```python
class Foo:
    def get_AAA(self):
        print('执行了get方法')
    def set_AAA(self,value):
        print('执行了set方法')
    def delete_AAA(self):
        print('执行了delete方法')
    # 实例化property类
    AAA = property(get_AAA, set_AAA, delete_AAA)
# 实例化
f = Foo()
# 获取属性直接调用,执行了get_AAA
f.AAA
# 设置属性值,传入参数执行了set_AAA
f.AAA = 'aaa'
# 删除属性值,执行了delete_AAA
del f.AAA
'''
执行结果:
执行了get方法
执行了set方法
执行了delete方法
'''
```

实际应用

```python
class Goods:
    def __init__(self):
        # 原价
        self.original_price = 100
        # 折扣
        self.discount = 0.8
    @property
    def price(self):
        # 实际价格 = 原价 * 折扣
        new_price = self.original_price * self.discount
        return new_price
    @price.setter
    def price(self, value):
        self.original_price = value
    @price.deleter
    def price(self):
        del self.original_price
goods = Goods()
goods.price         
goods.price = 200  
print(goods.price)
del goods.price    
```

## 类方法  🍀

类方法是通过@classmethod装饰器 , 将普通方法变成类方法 , 类方法只能与类属性交互 , 不能访问实例变量 , 并且默认有一个cls参数传进来表示本类

```python
class Person:
    country = 'China'
    def __init__(self,name,age):
        self.name = name
        self.age = age
    @classmethod    
    def search(cls):
        # 在类方法中不能使用实例变量,会抛出AttributeError
        print("I come from {}".format(cls.country))
        # print("{} come from {}".format(self.name,cls.country))  报错
p = Person('lyon','18')
p.search()
# 执行结果: I come from China
```

_PS_:类方法中的默认参数可以改成self , 并不会改变结果 , 同样只能访问类变量 , 不能访问实例变量

## 静态方法  🍀

静态方法是通过@staticmethod装饰器将类中的方法变成一个静态方法 

静态方法就像静态属性一样 , 在类中可以通过 self. 的方式进行调用 , 但是静态是不能够访问实例变量或类变量的 , 也就是说静态方法中的self已经跟本类没有关系了 , 它与本类唯一的关联就是需要通过类名来进行调用

```python
class Person:
    country = 'China'
    def __init__(self,name,age):
        self.name = name
        self.age = age
    # 已经跟本类没有太大的关系了,所以类中的属性无法调用
    @staticmethod    
    def search():
        print("我是静态方法")
p = Person('lyon','18')
p.search()
# 执行结果: 我是静态方法
```

加上self , self只为一个普通参数而已 

```python
class Person:
    country = 'China'
    def __init__(self,name,age):
        self.name = name
        self.age = age
    @staticmethod
    def search(self):
        print("{} come from {}".format(self.name,self.country))
p = Person('lyon','18')
# 将实例传入search方法中
p.search(p)
# 执行结果: lyon come from China
```











