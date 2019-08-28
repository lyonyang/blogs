# Python之路 - 集合

## 介绍  🍀

集合是一个无序的 , 不重复的数据组合 , 它的主要作用如下 : 

- 去重 , 把一个列表变成集合 , 就自动去重了
- 关系测试 , 测试两组数据之间的交集 , 差集 , 并集关系

在Python 2.7中集合表示如下 : 

```python
set([1,2,3])
```

在Python 3.x 中则是如下 : 

```python
{1,2,3}
```

集合支持一系列标准操作 , 包括并集 , 交集 , 差集 , 对称差集

## 创建  🍀

与字符串等数据类型一样 , 集合支持如下方式创建

```python
# 创建空集合只能用这种方式,参数为一个可迭代对象
s = set()
# 注意集合是单个元素,字典是键值对
s = {1,2,3}
```

## 添加  🍀

为集合添加元素

```python
# 定义集合
s = {'lyon','kenneth'}
# 添加一项
s.add('geek')
```

注意 : 集合不支持 "+"

## 更新  🍀

```python
# 定义集合
s = {'lyon','kenneth'}
# 添加多项,参数为可迭代对象
s.update(['1','2','3'])
```

## 删除  🍀

```python
# 定义集合
s = {'lyon','kenneth'}
# 删除一项
s.remove('kenneth')
# 清空集合
s.clear()
```

## 测试  🍀

```python
a = {1,2,3,4,5}
b = {1,2,3}
# 测试是否b中的每一个元素都在a中,即 b<=a ,返回bool值
b.issubset(a)
# 测试是否a中的每一个元素都在b中,即 b>=a ,返回bool值
b.issuperset(a)
```

## 集合操作  🍀

```python
>>>a = {1,2,3}
>>>b = {4,5,6}
# 求并集
>>>a.union(b)
# 同上,求并集
>>>a | b
# 求交集
>>>a.intersection(b)
# 同上,求交集
>>>a & b
# 求差集
>>>a.difference(b)
# 同上,求差集
>>>a - b
# 求对称差集
>>>a.symmetric_difference(b)
# 同上,求对称差集
>>>a ^ b
```

集合对象所有方法 

```python
 |  add(...)
 |      Add an element to a set.
 |
 |      This has no effect if the element is already present.
 |
 |  clear(...)
 |      Remove all elements from this set.
 |
 |  copy(...)
 |      Return a shallow copy of a set.
 |
 |  difference(...)
 |      Return the difference of two or more sets as a new set.
 |
 |      (i.e. all elements that are in this set but not the others.)
 |
 |  difference_update(...)
 |      Remove all elements of another set from this set.
 |
 |  discard(...)
 |      Remove an element from a set if it is a member.
 |
 |      If the element is not a member, do nothing.
 |
 |  intersection(...)
 |      Return the intersection of two sets as a new set.
 |
 |      (i.e. all elements that are in both sets.)
 |
 |  intersection_update(...)
 |      Update a set with the intersection of itself and another.
 |
 |  isdisjoint(...)
 |      Return True if two sets have a null intersection.
 |
 |  issubset(...)
 |      Report whether another set contains this set.
 |
 |  issuperset(...)
 |      Report whether this set contains another set.
 |
 |  pop(...)
 |      Remove and return an arbitrary set element.
 |      Raises KeyError if the set is empty.
 |
 |  remove(...)
 |      Remove an element from a set; it must be a member.
 |
 |      If the element is not a member, raise a KeyError.
 |
 |  symmetric_difference(...)
 |      Return the symmetric difference of two sets as a new set.
 |
 |      (i.e. all elements that are in exactly one of the sets.)
 |
 |  symmetric_difference_update(...)
 |      Update a set with the symmetric difference of itself and another.
 |
 |  union(...)
 |      Return the union of sets as a new set.
 |
 |      (i.e. all elements that are in either set.)
 |
 |  update(...)
 |      Update a set with the union of itself and others.
```