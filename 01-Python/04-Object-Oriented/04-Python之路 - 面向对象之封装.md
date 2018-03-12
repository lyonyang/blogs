# Python之路 - 面向对象特性之封装

## 介绍

封装就是把客观事物封装成抽象的类 , 并且类可以把自己的数据和方法只让可信的类或者对象操作 , 对不可信的进行信息隐藏

## 私有问题  🍀

当我们类中的一些属性或者方法想要对不可信的类或者对象隐藏时 , 我们就可以将这些属性或者方法 , 定义成私有属性或者私有方法

在Python中用双下划线开头的方式将属性隐藏起来 , 即带双下划线就为私有属性或者私有方法

- 私有属性

```python
class A:
    def __init__(self,name):
        # 定义私有属性
        self.__name = name
# 实例化
a = A("Lyon")
# 访问a中的__name属性
print(a.__name)
# 执行结果 : AttributeError: 'A' object has no attribute '__name'
'''
结果报错,意思是对象A中没有__name这个属性
也就是说,外部已经不能直接利用 .__name 来访问这个属性了
因为此时它是一个私有属性
'''
```

将属性定义成私有属性其实是一种变形操作 , 即类中所有以双下划线开头的名称都会自动变形成:\_类名+名称 如下:

```python
class A:
    def __init__(self):
        # 定义私有属性
        self.__name = name
# 实例化
a = A("Lyon")
# 访问a中的__name属性
print(a._A__name)      
# 执行结果: Lyon
'''
__name自动变形为 _A__name
所以使用a._A__name是可以访问到的
'''
```

由上可知变形的特点如下:

1. 类中定义的\_\_name只能在内部使用 , 并且内部使用是引用的变形的结果,即( self.\_A\_\_name)
2. 这种变形其实是针对外部的变形 , 在外部是无法通过__name访问的

***PS : 这种变形机制其实并没有真正意义上限制我们从外部直接访问属性 , 知道了类名和属性名就可以拼出名字 : \_类名\_\_属性 , 然后就可以访问了 , 如 a.\_A\_\_name . 并且变形的过程只在类的定义时发生一次*** 

- 私有方法

```python
class A:
    def __func(self):
        print("In the A")
a = A()
a.__func()
# 执行结果: AttributeError: 'A' object has no attribute '__func'
```

```python
a._A__func()
# 执行结果: In the A
```

## 当私有遇到继承  🍀

当我们在继承中使用私有属性或者方法时 , 因为变形机制 , 我们已经不能将私有属性或者方法 , 来与普通属性或者方法那样看待了

- 私有属性继承

```python
class A:
    def __init__(self, ame):
        self.__name = ame
class B(A):
    def __init__(self, name, ame):
        self.__name = name
        # 继承父类中的属性
        super().__init__(ame)
a = B('a', 'b')
print(a._A__name)
print(a._B__name)
'''
执行结果:
b
a
'''
```

例子说明 : 在上节中已经知道变形操作这回事了 , 当遇到继承时需要注意的就是 , 我们表面上看到的是两个类中都只有一个\_\_name属性 , 但是由于变形 , 使其在定义完成后就分别变成了\_A\_\_name 和 \_B\_\_name  , 所以继承时已经是两个不同的属性了 , 所以两个属性都存在 , 只是我们表面上还是看不到

- 私有方法继承

与私有属性继承一样 , 需要注意私有方法名变形的问题

我们可以利用这一特点 , 来实现继承时达到子类不会覆盖父类方法的效果

```python
class A:
    def __func(self):
        print('from A')
    def test1(self):
        self.__func()
class B(A):
    def __func(self):
        print('from B')
    def test2(self):
        self.__func()
b=B()
b.test1()
b.test2()
'''
执行结果:
from A
from B
'''
```

## 封装与扩展性  🍀

封装在于明确区分内外 , 使得类实现者可以修改封装内的东西而不影响外部调用者的代码 ; 而外部使用者只知道一个接口(函数) , 只要接口(函数)名 , 参数不变 , 使用者的代码永远无需改变 . 这就提供了一个良好的合作基础 , 相当于只要接口这个基础约定不变 , 则代码改变也不足为虑

原始类

```python
class Room:
    def __init__(self, name, owner, width, length, high):
        self.name = name
        self.owner = owner
        self.__width = width
        self.__length = length
        self.__high = high
    # 对外提供的求面积接口,隐藏内部实现详解
    def tell_area(self):
        return self.__width * self.__length
r1 = Room('卧室','Lyon','0.3','2','2')
r1.tell_area() 
```

修改类

```python
class Room:
    def __init__(self, name, owner, width, length, high):
        self.name = name
        self.owner = owner
        self.__width = width
        self.__length = length
        self.__high = high
    # 对外提供的求体积接口,隐藏内部实现详解
    def tell_area(self):
        return self.__width * self.__length * self.__high
r1 = Room('卧室','Lyon','0.3','2','2')
r1.tell_area()
```

我们发现我们将类的功能作出了修改 , 但是对于使用类功能的人来说 , 接口并没有发生变化 , 他们依然可以用原来的接口使用新功能
