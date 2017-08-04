# Python之路 - 迭代器和生成器
<!-- TOC -->

- [Python之路 - 迭代器和生成器](#python之路---迭代器和生成器)
    - [可迭代对象  🍀](#可迭代对象--🍀)
    - [迭代器  🍀](#迭代器--🍀)
    - [生成器  🍀](#生成器--🍀)
        - [生成器函数](#生成器函数)
        - [列表推导式和生成器表达式](#列表推导式和生成器表达式)

<!-- /TOC -->
## 可迭代对象  🍀

在Python中一切皆对象

迭代是重复反馈过程的活动 , 其目的通常是为了逼近所需目标或结果 

可迭代对象 , 即可以按照迭代的方式进行存取数据的对象 , 在python中我们可以理解为可以用for循环遍历的对象就是可迭代对象

__for循环做的那些事__ :  for循环是我们用来遍历一个数据集合的方法 , 其实就是根据一定的要求 (这个要求叫做'协议' ) 进行一次次的迭代的效果 . 当我们用for循环去遍历时 , 它做的第一件事就是判断对象是否是可迭代对象 , 如果是 , 那么它就会将该对象转换成一个迭代器 , 最后利用` __next__() `方法将迭代器中的内容一个接一个的取出来

可迭代对象的标志是 , 它具有` __iter__() `方法

判断对象是否为可迭代对象方法如下:

```python
# 导入模块
>>> from collections import Iterable
>>> l = ['lyon','oldboy']
# 判断是否为Iterable , 即可迭代对象
>>> isinstance(l,Iterable)
# 返回bool值
True
```

## 迭代器  🍀

通过上面的内容已经知道` for循环 `有一个生成迭代器的过程 , 迭代器是啥 ?

迭代器是访问集合元素的一种方式

特点:

1. 不依赖索引取值 , 访问者不需要关心迭代器内部的结构 , 仅需通过next()方法去访问
2. 不能随机访问集合中的某个值 , 只能从头到尾依次访问 , 不可返回访问
3. 惰性计算 , 只有在需要访问时才会生成值 , 节省内存

在python中有一个`iter()`方法 , 作用就是将可迭代对象变成一个迭代器 , 实质上iter()是去调用了` __iter__() `方法 ,  看代码:

```python
>>> l = ['lyon']
>>> l.__iter__()
# iterator即迭代器
<list_iterator object at 0x0000026DA649D320>
```

可迭代对象与迭代器的区别:

```python
# 用dir方法查看对象中的所有方法
>>> dir_list = dir([1,2])
>>> dir_iter = dir([1,2].__iter__())
# 筛选出不同点
>>> set(dir_iter) - set(dir_list)
{'__length_hint__', '__setstate__', '__next__'}
```

我们可以看出迭代器比可迭代对象多出了三个方法 , 所以我们可以根据这一点来判断一个对象到底是可迭代对象还是一个迭代器

```python
# 创建一个迭代器
>>> i = iter([1,2,3,4])
# 查看迭代器中元素的长度
>>> i.__length_hint__()
4
# 根据索引指定迭代开始位置
>>> i.__setstate__(3)
# 进行取值
>>> i.__next__()
4
```

*判断方法:* 

```python
# 导入Iterable类
>>> from collections import Iterable
# 导入Iterator类
>>> from collections import Iterator
# 是否为可迭代对象
>>> isinstance(obj,Iterable)
# 是否为迭代器
>>> isinstance(obj,Iterator)
# 注意:迭代器也是可迭代对象
```

*** 在迭代时 ,  我们需要注意迭代器中是否有值的问题 ,  即当我们一直调用` __next__ ` 方法取值时 , 如果值都取完了 , 而此时我们再执行 ` __next__ ` 方法 , 解释器就会抛出 StopIteration , 因为已经没有值可以取了 ***

## 生成器  🍀

自定义的一个能够实现迭代器功能的就是生成器

本质: 迭代器(所以自带了` __iter__ ` 方法和` __next__ ` 不需要我们去实现

特点: 惰性运算 , 开发者自定义

### 生成器函数

一个函数调用时返回一个迭代器 , 那么这个函数就叫做生成器函数

利用生成器做一个range( 2.x中的xrange ) 的功能

```python
# 定义函数
>>> def range(n):
...		start = 0
... 	while start < n:
... 		yield start
...			start += 1
>>> obj = range(5)
>>> obj.__next__()
>>> obj.__next__()
>>> obj.__next__()
>>> obj.__next__()
>>> obj.__next__()
```

yield的作用 :  yield的作用是中断函数的执行并记录中断的位置 , 等下次重新调用这个函数时 , 就会接着上次继续执行

PS : 调用生成器函数时 , 仅仅会返回一个生成器 , 并不会执行函数的内容 , 生成器只能由next() 进行调用执行 , 实质上next()方法就是调用的` __next__() `  方法

***yield from***

```python
def func1():
    for i in 'AB':
        yield i
    for j in range(3):
        yield j
print(list(func()))

def func2():
    yield from 'AB'
    yield from range(3)
    
print(list(func2()))
```

**生成器应用**

监听文件

```python
import time
def tail(filename):
    # 打开文件
    f = open(filename,encoding='utf-8')
    # 从文件末尾算起
    f.seek(0, 2) 
    while True:
        # 读取文件中新的文本行
        line = f.readline()  
        if not line:
            time.sleep(0.1)
            continue
        yield line
tail_g = tail('tmp')
# 生成器也是可迭代对象
for line in tail_g:
    print(line)
```

计算动态平均值

```python
def averager():
	total = 0
    count = 0
    average = None
    while True:
        term = yield average
        total += term
        count += 1
        average = total/count
# 生成生成器
g_avg = averager()
# 激活生成器,不激活无法send
next(g_avg)
# send相当于先传参,后调用next()
print(g_avg.send(10))
print(g_avg.send(30))
print(g_avg.send(50))
```

### 列表推导式和生成器表达式

```python
# 列表解析
>>> num = [i for i in range(10)]
>>> num
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# 生成器表达式
>>> num_iter = (i for i in range(10))
>>> num_iter
<generator object <genexpr> at 0x0000021C41003258>
>>> next(num_iter)
0
>>> next(num_iter)
1
>>> next(num_iter)
2
>>> next(num_iter)
3
>>> next(num_iter)
4
>>> next(num_iter)
```

对于推导式会有另一篇专门来写