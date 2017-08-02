# Python之路 - 内置函数

<!-- TOC -->

- [Python之路 - 内置函数](#python之路---内置函数)
    - [str类型代码的执行(3个) 🍀](#str类型代码的执行3个-🍀)
    - [数据类型相关(38) 🍀](#数据类型相关38-🍀)
        - [数字相关](#数字相关)
            - [数据类型](#数据类型)
            - [进制转换](#进制转换)
            - [数学运算](#数学运算)
        - [数据结构相关](#数据结构相关)
            - [序列](#序列)
            - [数据集合](#数据集合)
            - [相关内置函数](#相关内置函数)
    - [迭代器/生成器相关(3个) 🍀](#迭代器生成器相关3个-🍀)
    - [作用域相关(2个)  🍀](#作用域相关2个--🍀)
    - [面向对象相关(8个) 🍀](#面向对象相关8个-🍀)
        - [定义类方法](#定义类方法)
        - [判断类之间的关系](#判断类之间的关系)
        - [所有类的基类](#所有类的基类)
        - [类的继承](#类的继承)
        - [封装](#封装)
    - [反射相关(4个) 🍀](#反射相关4个-🍀)
    - [其他（10个) 🍀](#其他10个-🍀)

<!-- /TOC -->
## str类型代码的执行(3个) 🍀 

> `exec`(object[, globals[, locals]])   :point_left:

将字符串当做表达式去执行，没有返回值

```python
# 流程语句用exec
>>> exec("print('123')")
123
>>> exec('1+2+3+4')
10
>>> res = exec('1+2+3+4')
None
```

> `eval`(expression, globals=None, locals=None)   :point_left:

将字符串当做表达式去执行，并返回执行结果

```python
# 简单求值表达式用eval
>>> res = eval('1+2+3+4')
>>> res
10
```

> `compile`(source, filename, mode, flags=0, dont_inherit=False, optimize=-1)   :point_left:

把字符传编译成python可执行的代码，但是不会执行

*filename* : 默认`sys.stout`，即默认打印在控制台，打印到指定文件

*mode* : 指定compile后的对象的执行模式，注意有个`single`模式，当source带有变量赋值时，eval模式是解释不了的，所以需要用single模式或者exec模式

```python
# 交互语句用single
>>> code3 = 'name = input("please input your name:")'
>>> compile3 = compile(code3,'','single')
# 执行前name变量不存在
>>> name 
# 报错说'name'变量没有定义
Traceback (most recent call last):
  File "<pyshell#29>", line 1, in <module>
    name
NameError: name 'name' is not defined
>>> exec(compile3) 
# 执行时显示交互命令，提示输入
please input your name:'pythoner'
# 执行后name变量有值    
>>> name 
"'pythoner'"
```

## 数据类型相关(38) 🍀

### 数字相关

#### 数据类型

> `bool`([*x*])   :point_left:

查看一个元素的布尔值

> `int`(*x=0*)  /  `int`(*x*, *base=10*)   :point_left:

获取一个数的十进制或者进行进制转换

```python
>>> int('1')
1
# 二进制转十进制
>>> int('0b11',base=2)
3
```

> `float`([*x*])   :point_left:

将整数和字符串转换成浮点数

> `complex`([*real*[, *imag*]])   :point_left:

创建一个值为real + imag * j的复数或者转化一个字符串或数为复数。如果第一个参数为字符串，则不需要指定第二个参数

```python
>>> complex(1, 2)
(1+2j)
# 数字
>>> complex(1)
(1+0j)
# 当做字符串处理
>>> complex("1")
(1+0j)
# 注意：这个地方在“+”号两边不能有空格，也就是不能写成"1 + 2j"，应该是"1+2j"，否则会报错
>>> complex("1+2j")
(1+2j)
```

#### 进制转换

> `bin`(*x*)   :point_left:

将整数x转换为二进制字符串，如果x不为Python中int类型，x必须包含方法`__index__()`并且返回值为整数

```python
# 返回一个整数的二进制
>>> bin(999)
'0b1111100111'
# 非整型的情况，必须包含__index__()方法且返回值为integer的类型
>>> class myType:
...   def __index__(self):
...       return 35
...
>>> myvar = myType()
>>> bin(myvar)
'0b100011'
```

> `oct`(*x*)   :point_left:

转换为八进制

```python
>>> oct(8)
'0o10'
```

> `hex`(*x*)   :point_left:

转换为十六进制

```python
>>> oct(13)
'0o15'
```

#### 数学运算

>`abs`(*x*)  :point_left:

返回一个数的绝对值

```python
>>> num = -1
>>> abs(num)
1
```

> `divmod`(*a*, *b*)  :point_left:

返回两个数的除,余

```python
>>> divmod(5,2)
# 第一个数为整除,第二个为取余
(2, 1)
```

>`min`(*iterable*, **[, key, default]*)   👈
>
>`min`(*arg1*, *arg2*, **args*[, *key*])   👈

返回最小值,如果多个参数最小值一样,则返回第一个

```python
>>> min([1,2,3,4])
1
# 返回第一个
>>> min([1,2,3],[4,5],[1,2])
[1,2,3]
```

>`max`(*iterable*, **[, key, default]*)  👈
>
>`max`(*arg1* , *arg2*, **args*[, *key*])  👈

返回最大值,如果多个参数最大值,则返回第一个

```python
>>> max([1,2,3,4])
4
>>> max([2,3],[1,2,3])
[2, 3]
```

> `sum`(*iterable*[, *start*])  :point_left:

求和,参数为可迭代对象

```python
>>> sum((1,2,3,4))
10
```

> `round`(*number[, ndigits]*)  :point_left:

小数精确

```python
# 保留两位小数,四舍五入
>>> round(1.235,2)
1.24
```

> `pow`(*x*, *y*[, *z*])  :point_left:

幂运算

```python

>>> pow(2,2)
4
# 参数z相当余  x**y % z
>>> pow(2,2,2)
0
```

### 数据结构相关

#### 序列

列表和元组

>`list`([*iterable*])  :point_left:

将可迭代对象转换成list对象,实际上我们创建一个空list时,python解释器自动为我们调用了该方法

> `tuple`([*iterable*])  :point_left:

将可迭代对象转换成tuple对象,与list类似

相关内置函数

>`reversed`(*seq*)  :point_left:

顺序翻转,与list中reverse的区别在于,该翻转为新生成了一个对象,而不是在原对象上操作

>`slice`(*stop*)   :point_left:
>
>`slice`(*start*, *stop*[, *step*])   :point_left:

返回切片操作的三个参数

```python
# 相当于[0:2:],注意最后一个参数不能为0而是None
>>> op = slice(0,2,None)
>>> l = [1,2,3,4]
>>> l[op]
[1,2,3]
```

字符串

>`str`(*object=''*)   :point_left:
>
>`str`(*object=b''*, *encoding='utf-8'*, *errors='strict'*)   :point_left:

返回一个字符串对象,创建字符串时python解释器为我们调用了该方法进行创建

> `repr`(*object*)   :point_left:

返回一个可打印的字符串对象

```python
>>> repr(123)
```

>`format`(*value*[, *format_spec*])  :point_left:

格式化字符串

>`bytes`([*source*[, *encoding*[, *errors*]]])   :point_left:

将字符串转成bytes类型

```python
>>> bytes('lyon',encoding='utf-8')
b'lyon'
```

> `bytearray`([*source*[, *encoding*[, *errors*]]])   :point_left:

返回一个byte数组,Bytearray类型是一个可变的序列,并且序列中的元素的取值范围为[0,255]

*source* : 

1. 如果source为整数,则返回一个长度为source的初始化数组;
2. 如果source为字符串,则按照指定的encoding将字符串转换为字节序列;
3. 如果source为可迭代类型,则元素必须为[0,255]中的整数;
4. 如果source为与buffer接口一致的对象,则此对象也可以被用于初始化bytearray

>`memoryview`(*obj*)   :point_left:

函数返回给定参数的内存查看对象(Momory view)

所谓内存查看对象，是指对支持缓冲区协议的数据进行包装，在不需要复制对象基础上允许Python代码访问

>`ord`(*c*)  :point_left:

把一个字符转换成ASCII表中对应的数字

```python
>>> ord('a')
97
```

>  `chr`(*i*)   :point_left:

返回一个数字在ASCII编码中对应的字符

```python
>>> chr(66)
'B'
```

> `ascii`(*object*)  :point_left:

在对象的类中寻找` __repr__`方法,获取返回值

```python
>>> class Foo:
...  def __repr_(self):
...     return "hello"
...
>>> obj = Foo()
>>> r = ascii(obj)
>>> print(r)
# 返回的是一个可迭代的对象
<__main__.Foo object at 0x000001FDEE13D320>
```

#### 数据集合

字典


>`dict`(**\*kwarg*)
>
>`dict`(*mapping*, **\*kwarg*)
>
>`dict`(*iterable*, **\*kwarg*) 

转换成字典类型,创建一个字典时python解释器会自动帮我们调用该方法

集合

> `set`([*iterable*])  :point_left:

转换成集合类型,创建集合时,事实上就是通过该方法进行创建的

> `frozenset`([*iterable*])   :point_left:

定义冻结集合,即不可变集合,存在hash值

好处是它可以作为字典的key，也可以作为其它集合的元素。缺点是一旦创建便不能更改，没有add，remove方法

#### 相关内置函数

>`len`(*s*)   :point_left:

返回一个对象的长度

>`enumerate`(*iterable*, *start=0*)   :point_left:

为元素生成序号,可以定义序号的初始值,默认从0开始

```python
>>> l = ['a','b','c']
>>> for i,k in enumerate(l,0):
...      print(i,k)
...    
0 a
1 b
2 c
```

> `all`(*iterable*)   ​:point_left:​

判断一个可迭代对象中的元素是否都为空,返回bool值

>`any`(*iterable*)   :point_left:

判断一个可迭代对象中是否有真元素,返回bool值

>`zip`(**iterables*)   :point_left:

将两个长度相同的序列整合成键值对,返回一个zip对象可以用dict方法转换查看

```python
>>> l1 = ['k1','k2','k3']
>>> l2 = ['v1','v2','v3']
>>> ret = zip(l1,l2)
>>> dict(ret)
{'k1':'v1','k2':'v2','k3':'v3'}
```

> `filter`(*function*, *iterable*)   :point_left:

筛选过滤,把可迭代对象中的元素一一传入function中进行过滤

```python
# 筛选出偶数
>>> def func(x):
...		return x % 2 == 0
>>> f = filter(func,[1,2,3,4,5])
<filter object at 0x0000026DA649D160>
>>> ret = list(f)
[2,4]
```

>`map`(*function*, *iterable*, *...*)   :point_left:

将可迭代对象中的元素一一传入function中执行并返回结果

```python
>>> def func(s):
...     return s + ' hello'
>>> m = map(func,['alex','egon','lyon'])
>>> m
<map object at 0x0000026DA649D2E8>
>>> ret = list(m)
>>> ret
['alex hello', 'egon hello', 'lyon hello']
```

> `sorted`(*iterable*, ***, *key=None*, *reverse=False*)   :point_left:

为一个对象进行排序,在list中有个sort方法;区别:sort会改变原list,而sorted则不会改变原list

```python
>>> l = [3,4,5,1,2,9,8,7,6]
>>> sorted(l)
[1,2,3,4,5,6,7,8,9]
>>> l

```

## 迭代器/生成器相关(3个) 🍀

> `range`(*stop*)   :point_left:
>
> `range`(*start*, *stop*[, *step*])   :point_left:

返回一个序列,为一个可迭代对象,并可用下标取值

```python
>>> from collections import Iterable
>>> r = range(10)
>>> r[0]
0
>>> isinstance(r,Iterable)
True
>>> list(r)
[0,1,2,3,4,5,6,7,8,9]
```

> `next`(*iterator*[, *default*])  :point_left:

拿取迭代器中的元素,一次只拿一个

```python
>>> Iter = iter([1,2,3,4])
>>> next(Iter)
1
>>> next(Iter)
2
>>> next(Iter)
3
>>> next(Iter)
4
# 没有元素就会进行报错
>>> next(Iter)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

>`iter`(*object*[, *sentinel*])   :point_left:

创建一个迭代器

```python
>>> obj = iter([1,2,3,4])
>>> obj
<list_iterator object at 0x0000026DA649D278>
```

## 作用域相关(2个)  🍀

>`locals`()  :point_left:

打印函数局部命名空间

>`globals`()   :point_left:

打印函数的全局命名空间

## 面向对象相关(8个) 🍀

### 定义类方法

>`classmethod`(*function*)  :point_left:

返回一个函数的类方法

>`staticmethod`(*function*)   :point_left:

返回一个函数的属性方法

>`property`(*fget=None*, *fset=None*, *fdel=None*, *doc=None*)   :point_left:

返回一个静态属性

### 判断类之间的关系

>`isinstance`(*object*, *classinfo*)  :point_left:

判断对象的类型,返回bool值,主要用于判断类之间的关心,因为type无法判断类之间的关心

>`issubclass`(*class*, *classinfo*)   :point_left:

判断一个类是否为另一个类的子类,返回bool值

### 所有类的基类

> *class*`object`   :point_left:

返回一个基类,不接收任何参数

### 类的继承

> `super`([*type*[, *object-or-type*]])  :point_left:

用于继承父类

### 封装

> `vars`([*object*])  :point_left:

返回一个对象中包含的属性

## 反射相关(4个) 🍀

>`hasattr`(*object*, *name*)  :point_left:

参数是一个对象和一个字符串。如果字符串是对象的一个属性的名称，则结果为True,否则为False

>`getattr`(*object*, *name*[, *default*])   :point_left:

返回对象的命名属性的值,name必须是字符串,如果字符串是对象属性之一的名称,则返回该属性的值

>`setattr`(*object*, *name*, *value*)   :point_left:

为某个对象设置一个属性

>`delattr`(*object*, *name*)   :point_left:

删除对象中的属性值

## 其他(10个) 🍀

>`input`([*prompt*])   :point_left:

交互式输入

>`print`(**objects*, *sep=' '*, *end='\n'*, *file=sys.stdout*, *flush=False*)  :point_left:

交互式输出

>`open`(*file*, *mode='r'*, *buffering=-1*, *encoding=None*, *errors=None*, *newline=None*, *closefd=True*, *opener=None*)   :point_left:

打开文件

>`help`([*object*])  :point_left:

查找官方说明

>`hash`(*object*)  :point_left:

返回一个hash地址

>`callable`(*object*)   :point_left:

判断一个对象是否可以被调用执行

>`dir`([*object*])  :point_left:

返回一个对象中的所有方法

>`id`(*object*)   :point_left:

返回一个对象的内存地址

>`type`(*object*)
>
>`type`(*name*, *bases*, *dict*)   :point_left:

查看一个对象的数据类型

>`__import__`(*name*, *globals=None*, *locals=None*, *fromlist=()*, *level=0*)   :point_left:

该函数是由import进行调用的,我们一般不用