# Python之路 - 字典
<!-- TOC -->

- [Python之路 - 字典](#python之路---字典)
    - [介绍  🍀](#介绍--🍀)
    - [创建  🍀](#创建--🍀)
    - [增加  🍀](#增加--🍀)
    - [修改  🍀](#修改--🍀)
    - [删除  🍀](#删除--🍀)
    - [查找  🍀](#查找--🍀)
    - [遍历  🍀](#遍历--🍀)
    - [嵌套  🍀](#嵌套--🍀)
    - [更多  🍀](#更多--🍀)

<!-- /TOC -->
## 介绍  🍀

字典是一种key - value 的数据类型 , 用 冒号 (" : ") 来分割 , 每个对象之间用逗号(" , ")分割 , 整个字典包括在花括号("{ }")中

字典中的键(key)是唯一的 , 但值(value)则不必

**字典是可变的数据类型 , 并且是无序的**

基本操作如下 : **创建、增加、修改、删除、查找、遍历、多级嵌套**等

注意 : 字典中key是唯一的 , 如果出现多个相同的key被赋值 , 那么值为最后一个赋的值 ; key是不可变的 , 所以可变的数据类型是不能用的 , 如 : list , 对于不可变的数据类型则可以 , 如 : str、int、tuple

2）key是不可变的 , 所以可变的数据类型是不能用的 , 如 : list , 对于不可变的数据类型则可以 , 如 : str、int、tuple

## 创建  🍀

```python
# 创建一个空字典
empty_info = {}
# 创建一个字典
info = {"name":"Lyon","age":21}
# 也可调用dict()方法
info = dict()
```

## 增加  🍀

```python
# 创建一个字典
info = {"name":"Lyon","age":21}
# 增加新的键/值对
info["school"] = "university"
# 打印info
print(info)     
# 注:字典是无序的,所以打印结果也是随机打印
'''
执行结果:
{'school': 'university', 'age': 21, 'name': 'Lyon'}
'''
```

## 修改  🍀

```python
# 创建一个字典
info = {"name":"Lyon","age":21,"school":"university"}
# 修改age
info["age"] = 18
# 打印info
print(info)     
'''
执行结果:
{'age': 18, 'school': 'university', 'name': 'Lyon'}
'''
```

## 删除  🍀

```python
# 创建一个字典
info = {"name":"Lyon","age":21,"school":"university"}
# 标准删除姿势
info.pop("school")
# 打印info
print(info)    
# 换个姿势
del info["age"]
# 打印info
print(info)   
# 随机删除
info.popitem()
# 打印info
print(info)    
'''
执行结果:
{'name': 'Lyon', 'age': 21}
{'name': 'Lyon'}
{}
'''
```

## 查找  🍀

```python
# 创建一个字典
info = {"name":"Lyon","age":21,"school":"university"}
# 标准查找,判断name是否在字典info中
print("name" in info)       #打印：True
# 获取值
print(info.get("name"))     #打印：Lyon
# 换换姿势
print(info["name"])         #打印：Lyon
# 这种方式要注意如果key不存在就会报错,而get仅仅返回None
print(info["home"])
# 报错：KeyError: 'home'
'''
执行结果:
True
Lyon
Lyon
KeyError:'home'
'''
```

## 遍历  🍀

```python
# 创建一个字典
info = {"name":"Lyon","age":21,"school":"university"}
# 方法1,推荐
for key in info:
  print(key,info[key])
# 方法2
for k,v in info.items():
  print(k,v)
'''
执行结果:
school university
name Lyon
age 21
school university
name Lyon
age 21
'''
```

## 嵌套  🍀

```python
# 创建一个多级嵌套字典
datas ={
    '湖北省':{
        "武汉市":{
               "武昌区":["Hello"],
               "洪山区":["Sorry"],
               "江夏区":["Welcome"],
         },
    },
    '湖南省':{
        "长沙市":{
            "岳麓区":{},
            "天心区":{},
            "芙蓉区":{},
        },
    },
    '广东省':{
        "佛山市":{
            "三水区":{},
            "顺德区":{},
            "男海区":{},
        },
    },
}
# 修改最里层的value
datas["湖北省"]["武汉市"]["武昌区"].append("Lyon")
# 打印结果
print(datas["湖北省"]["武汉市"])    
'''
执行结果:
{'洪山区': ['Sorry'], '武昌区': ['Hello', 'Lyon'], '江夏区': ['Welcome']}
'''
```

## 更多  🍀

```python
len(dict)        # 计算字典元素个数
dict.clear()     # 清空词典所有条目
dict.fromkeys(seq, val))  # 创建一个新字典,以列表 seq 中元素做字典的键,val 为字典所有键对应的初始值
dict.has_key(key)  # 如果键在字典dict里返回true,否则返回false
dict.items()       # 以列表返回可遍历的(键, 值) 元组数组
dict.keys()        # 以列表返回一个字典所有的键
dict.values()      # 以列表返回字典中的所有值
dict.setdefault(key, default=None) # 和get()类似, 但如果键不存在于字典中,将会添加键并将值设为default
dict.update(dict2)                 # 把字典dict2的键/值对更新到dict里
```
方法合集

```python
 |  clear(...)
 |      D.clear() -> None.  Remove all items from D.
 |
 |  copy(...)
 |      D.copy() -> a shallow copy of D
 |
 |  fromkeys(iterable, value=None, /) from builtins.type
 |      Returns a new dict with keys from iterable and values equal to value.
 |
 |  get(...)
 |      D.get(k[,d]) -> D[k] if k in D, else d.  d defaults to None.
 |
 |  items(...)
 |      D.items() -> a set-like object providing a view on D's items
 |
 |  keys(...)
 |      D.keys() -> a set-like object providing a view on D's keys
 |
 |  pop(...)
 |      D.pop(k[,d]) -> v, remove specified key and return the corresponding value.
 |      If key is not found, d is returned if given, otherwise KeyError is raised
 |
 |  popitem(...)
 |      D.popitem() -> (k, v), remove and return some (key, value) pair as a
 |      2-tuple; but raise KeyError if D is empty.
 |
 |  setdefault(...)
 |      D.setdefault(k[,d]) -> D.get(k,d), also set D[k]=d if k not in D
 |
 |  update(...)
 |      D.update([E, ]**F) -> None.  Update D from dict/iterable E and F.
 |      If E is present and has a .keys() method, then does:  for k in E: D[k] = E[k]
 |      If E is present and lacks a .keys() method, then does:  for k, v in E: D[k] = v
 |      In either case, this is followed by: for k in F:  D[k] = F[k]
 |
 |  values(...)
 |      D.values() -> an object providing a view on D's values
```

