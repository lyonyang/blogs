#  Python之路 - 匿名函数
<!-- TOC -->

- [Python之路 - 匿名函数](#python之路---匿名函数)
    - [匿名函数介绍](#匿名函数介绍)
    - [匿名函数运用](#匿名函数运用)

<!-- /TOC -->
## 匿名函数介绍

lambda是一个表达式 , 而并非语句 , 所以可以出现在def语句所不能出现的位置 , 并且不需要指定函数名; lambda表达式还可以提高代码的可读性 , 简化代码

lambda表达式主要用于写一些简单的方法 , 对于复杂的还是用函数写的好 

示例:

```python
# 普通函数
def func(x):
    return x * x
print(func(5))
-----------------------
# 匿名函数,自带return功能
func = lambda x : x * x
print(func(5))
---------------------------------------------------
func = lambda arguments : expression using argument 
```

使用匿名函数可以减少命名空间使用内存 , 因为没有函数名

可直接后面传递参数

```python
>>> (lambda x,y : x if x > y else y)(1,2)
2
```

非固定参数

```python
>>> (lambda *args : args)(1,2,3,4)
(1, 2, 3, 4)
```

***PS : 匿名函数主要是与其他函数搭配使用***

## 匿名函数运用

***结合使用***

map , 计算平方

```python
# map后返回的对象为map对象,所以利用list方法进行强转
>>> list(map(lambda x : x * x, [1,2,3,4]))
[1,4,9,16]
```

filter , 筛选偶数

```python
>>> list(filter(lambda x : x % 2 == 0,[1,2,3,4]))
[2,4]
```

reduce , 求和

```python
# python3中已经没有reduce方法了,调用需要导入
>>> from functools import reduce
# reduce(function, sequence, initial=None)
>>> reduce(lambda x , y : x + y, [1,2,3,4,5],100)
115
```

***嵌套使用***

版本一

```python
def func(x):
    return lambda x : x + y
f = func(2)
print(f(2))
# output: 4
```

版本二

```python
func = lambda x : (lambda y: x + y)
y = func(1)
y(2)
# output: 3
```