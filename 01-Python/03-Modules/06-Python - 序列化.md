# Python之路 - 序列化

## 介绍  🍀
  
先说个例子 , 当我们将一个字典或者列表再或者变量存入磁盘中 , 而存入磁盘后原本数据类型就得不到保持了 . 这个时候我们就得用序列化和反序列化了

序列化是将对象进行存储时保持当时对象的状态 , 实现其生命周期的延长 

反序列化则是将存储的对象读取出来并转成原本的数据类型

序列化的目的

1. 以某种存储形式使自定义对象持久化
2. 将对象从一个地方传递到另一个地方
3. 使程序更具维护性

***此时应该想到 eval :***那么问题来了 , 序列化所达到的功能我用eval()也能达到啊 , eval()直接就可以把字符串转换成python解释器能解释的代码 , 即可以直接将字符串中的字典 , 列表都转成原来的数据类型 . 但是要注意的是 , eval本来就是将字符串内容转换成python可以执行的代码 , 并执行它 , 这样看来eval就不安全了 , 因为如果在我能读取的内容中含有一些其他的 ' 危险代码 ' 如 ' 删除文件 ' , 于是造成了毁灭性的打击 , 所以eval是存在风险的 

Python为我们提供了三个序列化工具 , 分别是 json , pickle , shelve

## json  🍀

用于字符串和python数据类型之间进行转换 , 因为json表示出来就是一个字符串

json模块提供了四个方法

| 方法    | 描述                            |
| ----- | ----------------------------- |
| dump  | 接收一个文件句柄 , 将原数据类型转换成字符串写入文件   |
| load  | 接收一个文件句柄 , 将文件中的字符串转换成原数据类型返回 |
| dumps | 接收一个数据类型 , 将其转换成字符串           |
| loads | 接收一个字符串 , 将其转换成原数据类型          |

dump 和 load 实例

```python
# 导入json模块
import json
# 创建一个文件句柄
f = open('json_file','w')
# 创建一个字典
dic = {'k1':'v1','k2':'v2'}
# 将字典转换成字符串写入文件
json.dump(dic,f)
# 关闭文件
f.close()
# 创建一个文件句柄
f = open('json_file')
# 将文件中的字符串读出并转换成原数据类型
dic2 = json.load(f)
# 关闭文件句柄
f.close()
# 打印类型和结果
print(type(dic2),dic2)
# <class 'dict'> {'k1': 'v1', 'k2': 'v2'}
```

dumps 和 loads 实例

```python
# 导入json模块
import json
# 创建一个新列表
lst = ['1','2','3','4']
# 将列表转换成字符串,用j_d来接收返回值
j_d = json.dumps(lst)
# 将字符串转换成原数据类型,用j_s来接收返回值
j_s = json.loads(j_d)
# 打印j_d的值以及类型
print(j_d,type(j_d))
# ["1", "2", "3", "4"] <class 'str'>
# 打印j_s的值以及类型
print(j_s,type(j_s))
# ['1', '2', '3', '4'] <class 'list'>
```

loads的特殊情况

```python
# 导入json模块
import json
# 创建一个字符串,内部为一个字典
dic_s = "{'k1':'v1','k2':'v2','k3':3}"
# 将字符串转换成字典
json.loads(dic_s)
# 解释器出现报错
# json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
'''
报错原因,用json的loads功能时,字符串类型的字典中的字符串必须由 "" 表示
即上面的dic_s应该改为 '{"k1":"v1","k2":"v2","k3":3}'

结论:用json的loads功能时,字符串类型的字典中的字符串必须由 "" 表示
'''
```

PS : json可用于不同语言之间的数据交换

## pickle   🍀

用于python特有的类型和python的数据类型间进行转换

pickle模块也提供了四个方法 , 与json一样 dumps , dump , loads , load

由于pickle是对于python特有的类型 , 所以 load 和 loads方法不仅支持字典 , 列表  , 它还能把python中任意的数据类型进行序列化

```python
-------dumps和loads--------
# 导入pickle模块
import pickle
# 创建一个字典
dic = {'k1':'v1','k2':'v2'}
# 将字典转换成二进制内容
p_d = pickle.dumps(dic)
# 将二进制内容转换成字典
p_l = pickle.loads(p_d)
# 打印p_d
print(p_d)  
# b'\x80\x03}q\x00(X\x02\x00\x00\x00k2q\x01X\x02\x00\x00\x00v2q\x02X\x02\x00\x00\x00k1q\x03X\x02\x00\x00\x00v1q\x04u.'
# 打印p_d的类型
print(type(p_d))
# <class 'bytes'>
# 打印p_l
print(p_l)
# {'k2': 'v2', 'k1': 'v1'}
# 打印p_l的类型
print(type(p_l))
# <class 'dict'>
---------dump 和 load---------
# 创建一个文件句柄
f = open('pickle_file','wb')
# 写入内容
pickle.dump('lyon',f)
# 关闭文件
f.close()
# 创建一个文件句柄
f = open('pickle_file','rb')
# 读出内容
p_f = pickle.load(f)
# 关闭文件
f.close()
# 打印
print(p_f)
# lyon
```

**但是pickle仅仅只能对python中的数据进行序列化 , 反序列化时其他语言就无法读懂了这是什么了** , 所以我们一般用推荐使用json

## shelve  🍀

shelve也是python提供给我们的序列化工具 , 比pickle用起来简单一些

shelve只提供给我们一个open方法 , 是用key来访问的 ,  使用起来和字典类似

```python
# 导入shelve模块
import shelve
# shelve提供open方法
f = shelve.open('shelve_file')
# 直接对文件句柄进行操作,就可以写入文件中
f['key'] = {'int':10, 'float':9.5, 'string':'Sample data'}  
# 关闭文件
f.close()
# 打开文件
f1 = shelve.open('shelve_file')
# 直接用key取值,key不存在就报错
existing = f1['key']
# 关闭文件
f1.close()
# 打印结果
print(existing)
# {'float': 9.5, 'int': 10, 'string': 'Sample data'}
```

shelve不支持多个应用同时往一个数据库进行操作 , 所以当我们知道我们的应用如果只进行操作 , 我们可以设置shelve.open() 方法的参数来进行

 shelve.open(filename, flag='c', protocol=None, writeback=False)

```python
import shelve
# flag参数为设置操作模式,r 设置只读模式
f = shelve.open('shelve_file', flag='r')
existing = f['key']
f.close()
print(existing)
```

`  writeback  `参数 , 可以减少我们出错的概率 , 并且让对象的持久化对用户更加的透明了 ; 但这种方式并不是所有的情况下都需要 , 首先 , 使用writeback以后 , shelf在open()的时候会增加额外的内存消耗 , 并且当数据库在close()的时候会将缓存中的每一个对象都写入到数据库 , 这也会带来额外的等待时间 , 因为shelve没有办法知道缓存中哪些对象修改了 , 哪些对象没有修改 , 因此所有的对象都会被写入

```python
import shelve
f1 = shelve.open('shelve_file')
print(f1['key'])
f1['key']['new_value'] = 'this was not here before'
f1.close()
# 设置writeback
f2 = shelve.open('shelve_file', writeback=True)
print(f2['key'])
f2['key']['new_value'] = 'this was not here before'
f2.close()
```