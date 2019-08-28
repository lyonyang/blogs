# Python之路 - 正则表达式

## 正则介绍  🍀

正则表达式并不是python的一部分，而是在各个编程语言都有的一种用于处理字符串的强大工具。

使用正则处理字符串在效率上可能不如str自带的方法，但是它的功能十分强大。python中的正则封装在re模块中。

## 匹配方法  🍀

首先将匹配方法进行说明，即re模块的内置方法

> `re.match`(*pattern*, *string*, *flags=0*) :  👈

从字符串的开头开始匹配，匹配成功返回一个`_sre.SRE_Match`类型，可用`.group()` 取出结果，失败返回None

*pattern* : 匹配格式

*string* : 要匹配的字符串

*flags* : 编译标志位，用于修改正则表达式的匹配方式

```python
# 导入re模块，后续方法实例省略这一步
>>> import re
>>> res = re.match('lyon','lyon')
# 查看类型
>>> type(res)
<class '_sre.SRE_Match'>
# 用.group()取出结果
>>> res.group()
'lyon'
```

> `re.search`(*pattern*, *string*, *flags=0*) :  👈

扫描整个字符串，匹配成功则返回匹配到的第一个对象（`_sre.SRE_Match`类型），失败返回None

*pattern* : 匹配格式

*string* : 要匹配的字符串

*flags* : 编译标志位，用于修改正则表达式的匹配方式

```python
# 匹配数字
>>> re.search('\d+','abc123abc').group()
'123'
```

> `re.findall`(*pattern*, *string*, *flags=0*) :  👈

匹配字符串所有的内容，把匹配到的字符串以列表的形式返回

*pattern* : 匹配格式

*string* : 要匹配的字符串

*flags* : 编译标志位，用于修改正则表达式的匹配方式

```python
# 匹配数字
>>> re.findall('\d','abc123abc456')
['1','2','3','4','5','6']
```

> `re.split`(*pattern*, *string*, *maxsplit=0*, *flags=0*) :  👈

指定格式进行切分，返回一个列表

*pattern* :  切分格式

*string* : 要切分的字符串

*maxsplit* : 切分次数

*flags* : 编译标志位，用于修改正则表达式的匹配方式

```python
# 以数字进行切分
>>> re.split('\d+','abc123abc123+-*/45')
['abc', 'abc', '+-*/', '']
```

> `re.sub`(*pattern*, *repl*, *string*, *count=0*, *flags=0*) : 👈

替换匹配到的字符串并返回替换后的结果

*pattern* : 匹配格式

*repl* : 替换格式

*string* : 要匹配替换的字符串

*flags* : 编译标志位，用于修改正则表达式的匹配方式

```python
>>> re.sub("abc","def","abc123abc")
'def123def'
# 只替换查找到的字符串一次
>>> re.sub("abc","def","abc123abc",count=1)
'def123abc'
```

*flags说明（轻轻了解） :*

| 标志                    | 说明                                 |
| --------------------- | ---------------------------------- |
| re.I  (re.IGNORECASE) | 忽略大小写（括号内为全拼写法，效果一样）               |
| re.M  (MULTILINE)     | 多行模式，改变 '^' 和 '$' 的行为 （改变？见下节匹配模式） |
| re.S  (DOTALL)        | 任意匹配模式，改变 ' . '  的行为（同上）           |
| re.L  (LOCALE)        | 做本地化识别（locale-aware）匹配，法语等         |
| re.X  (VERBOSE)       | 该标志通过给予更灵活的格式以便将正则表达式写得更易于理解       |
| re.U                  | 根据Unicode字符集解析字符，这个标志影响\w,\W,\b,\B |

```python
# 忽略大小写
>>> re.findall('a','aA123aAAA',flags=re.I)
['a', 'A', 'a', 'A', 'A', 'A']
```

*注意转义的问题：当我们的匹配格式中有我们需要匹配的特殊字符，如 ' \ '、' * '、' + '等，为了让解释器知道我们这是需要匹配的，我们可以在格式前加 'r' 进行转义，或者在每个需要匹配的之前加个 ' \ '来完成转义。*

*`.group()`小知识：*

在我们使用`.group()`方法时，要注意如果我们的正则表达式没有匹配到结果，即返回None时，用`.group()`时就会报错，因为`"NoneType"`是没有该方法的，只有`_sre.SRE_Match`类型才能使用该方法。

## 匹配模式   🍀

### 字符匹配   🍡

| 字符    | 描述                                       |
| :---- | ---------------------------------------- |
| .     | 默认匹配除\n之外的任意一个字符，若指定flag DOTALL,则匹配任意字符，包括换行 |
| \d \D | 匹配数字0-9/非数字                              |
| \s    | 匹配空白字符、\t、\n、\r , re.search("\s+","ab\tc1\n3").group() 结果 '\t' |
| \S    | 非空白字符                                    |
| \w    | 匹配[A-Za-z0-9]                            |
| \W    | 匹配非[A-Za-z0-9]                           |
| \b    | 匹配一个单词边界，也就是指单词和空格间的位置。例如， 'er\b' 可以匹配"never" 中的 'er'，但不能匹配 "verb" 中的 'er'。 |
| \B    | 匹配非单词边界。'er\B' 能匹配 "verb" 中的 'er'，但不能匹配 "never" 中的 'er'。 |

### 次数匹配  🍡 

| 字符       | 描述                                       |
| -------- | ---------------------------------------- |
| *        | 匹配\*号前的字符0次或多次，re.findall("ab*","cabb3abcbbac")  结果为['abb', 'ab', 'a'] |
| +        | 匹配前一个字符1次或多次，re.findall("ab+","ab+cd+abb+bba") 结果['ab', 'abb'] |
| ?        | 匹配前一个字符0次或者1次                            |
| {m}      | 匹配前一个字符m次                                |
| {n,m}    | 匹配前一个字符n到m次，re.findall("ab{1,3}","abb abc abbcbbb") 结果'abb', 'ab', 'abb'] |
| *?/+?/?? | 转为非贪婪模式（尽可能少的匹配）                         |
| [...]    | 字符集，匹配字符集中任意字符，字符集可给出范围或者逐个列出            |

### 边界匹配  🍡

| 字符   | 描述                                       |
| ---- | ---------------------------------------- |
| ^    | 匹配字符串开头，若指定flags MULTILINE，这种也可以匹配上，(r'^a','\nabc\neee',flags=re.MULTILINE) |
| $    | 匹配字符结尾，或e.search("foo$","bfoo\nsdfsf",flags=re.MULTILINE).group()也可以 |
| \A   | 只从字符开头匹配，re.search("\Aabc","alexabc") 是匹配不到的 |
| \Z   | 匹配字符结尾，同$                                |

### 分组匹配  🍡

| 字符        | 描述                                       |
| :-------- | :--------------------------------------- |
| 丨        | 匹配丨左或丨右的字符，re.search("abc丨ABC","ABCBabcCD").group() 结果'ABC' |
| (...)     | 分组匹配，re.search("(abc){2}a(123丨456)c", "abcabca456c").group() 结果 abcabca456c |
| (?P\<..>) | 命名分组匹配 re.search("(?P\<province>[0-9]{4})(?P\<city>[0-9]{2})(?P\<birthday>[0-9]{4})","371481199306143242").groupdict("city") 结果{'province': '3714', 'city': '81', 'birthday': '1993'} |

## 匹配方法补充  🍀

补充方法

> `re.subn`(pattern, repl, string, count=0, flags=0) :  

返回替换后的字符串和替换次数

> `re.escape`(pattern) :                                

自动进行转义，除了ASCII字母、数字和'_'之外

> `re.compile`(pattern, flags=0) :                      

生成一个_sre.SRE_Pattern对象，以便多次调用

> `re.finditer`(pattern, string, flags=0) :             

返回一个匹配结果的迭代器，可迭代取值

> `re.fullmatch`(pattern, string, flags=0) :            

完整匹配，不完整则返回None

> `re.template`(pattern, flags=0) :                     

没人知道是干嘛的，跟compile差不多

> `re.purge()` :                              

清除正则表达式缓存

'''
当你在程序中使用 re 模块，无论是先使用 compile 还是直接使用比如 findall 来使用正则表达式操作文本，re 模块都会将正则表达式先编译一下， 并且会将编译过后的正则表达式放到缓存中，这样下次使用同样的正则表达式的时候就不需要再次编译， 因为编译其实是很费时的，这样可以提升效率，而默认缓存的正则表达式的个数是 100, 当你需要频繁使用少量正则表达式的时候，缓存可以提升效率，而使用的正则表达式过多时，缓存带来的优势就不明显了
'''

## 正则实例  🍀

连续匹配

```python
# 导入模块
>>> import re
# 获取字符串
>>> source ='192.168.0.1 25/Oct/2012:14:46:34 "GET /api HTTP/1.1" 200 44 "http://abc.com/search" "Mozilla/5.0"'
# 设置匹配格式
>>> res = re.match('^(?P<remote_ip>[^ ]*) (?P<date>[^ ]*) "(?P<request>[^"]*)" (?P<status>[^ ]*) (?P<size>[^ ]*) "(?P<referrer>[^"]*)" "(?P<user_agent>[^"]*)"',source)
# 返回一个字典，groupdict中的key为组名，value为值
>>> source_dic = res.groupdict()
# for循环打印
>>> for k in source_dic:
        #打印key和vaule
...     print(k+": "+source_dic[k])
...
# 打印结果
date: 25/Oct/2012:14:46:34
remote_ip: 192.168.0.1
referrer: http://abc.com/search
status: 200
user_agent: Mozilla/5.0
size: 44
request: GET /api HTTP/1.1
```
