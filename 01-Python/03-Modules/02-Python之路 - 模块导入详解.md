# Python之路 - 模块导入详解

## import 🍀

我们知道一个模块就是一个py文件 , 当我们执行py文件时 , python解释器会先加载内置命名空间 , 其次是加载全局命名空间( 学习函数就已知道 )  , 还有个局部命名空间就不说了

当python解释器遇到我们的import语句时 , import会将模块进行初始化 , 即会将模块中的内容执行一遍 , 既然执行 , 那么被import的模块的全局命名空间就创建成功了 , 并且会将这个创建成功的命名空间加载到使用import语句的本地的全局命名空间 . 于是我们就可以在本地使用被导入模块了

自定义模块my_module.py , 文件名my_module.py , 模块名my_module

```python
在模块my_module.py下
---------------文件内容----------------
|  print('from the my_module.py')    |
|  def read():                       |
|    print('in the module.py read')  | 
--------------------------------------
在当前文件test.py下
---------------文件内容----------------
|  import my_module                  |
|  my_module.read()                  |
--------------------------------------
# 执行test.py文件,打印结果
'''
# 执行了my_module.py的print语句
from the my_module.py
# 成功调用my_module.py中的read函数
in the module.py read
'''
```

import语句是可以在程序中的任意位置使用的 , 且针对同一个模块import多次时 , 为了防止你重复导入 , python进行了如下优化 : 第一次导入后就将模块名加载到内存了 , 后续的import语句仅是对已经加载大内存中的模块对象增加一次引用 , 不会重新执行模块内的语句 

import多次同以模块

```python
在模块my_module.py下
---------------文件内容----------------
|  print('from the my_module.py')    |
|  def read():                       |
|    print('in the module.py read')  | 
--------------------------------------
在当前test.py文件下
---------------文件内容----------------
|  import my_module                  |
|  import my_module                  |
|  import my_module                  |
|  my_module.read()                  |
--------------------------------------
# 执行test.py文件,打印结果
'''
# 仅执行了一次my_module.py中的print语句
from the my_module.py
# 成功调用my_module.py中的read函数
in the module.py read
'''
```

我们可以从sys.modules中找到当前已经加载的模块 , sys.modules是一个字典 , 内部包含模块名与模块对象的映射 ,该字典决定了导入模块时是否需要重新导入 

每个模块的命名空间都是相互独立的 , 这样我们在编写自己的模块时 , 就不用担心我们定义在自己模块中全局变量在被导入时 , 与使用者的同名全局变量冲突

***ps:模块中的内容使用 :` 模块名 .函数或者变量或者类  `来进行调用***

总结

首次导入模块时python会做三件事

1. 为源文件(如my_module模块) 创建新的命名空间 , 在my_module中定义的函数和方法若是使用到了globals() 时访问的就是这个命名空间
2. 在新创建的命名空间执行模块中包含的代码 , 如上例中执行了模块中的print语句 , 并加载了函数
3. 创建名字my_module 来引用该命名空间 , 使用my_module.名字的方式访问my_module.py文件中定义的名字 , 且名字与test.py文件中的名字来自两个完全不同的地方

## import ... as ... 🍀

为模块取名

根据用户需求选择额不同的sql(数据库)功能

```python
# 在mysql.py中
def sqlparse():
    print('from mysql sqlparse')
```

```python
# 在oracle.py中
def sqlparse():
    print('from oracle sqlparse')
```

```python
# 在test.py中
db_type = input('Please choice the database >>').strip()
if db_type == 'mysql':
    import mysql as db
elif db_type == 'oracle':
    import oracle as db
```

一行导入多个模块

```python
import sys,os,re
```

## from ... import ... 🍀

相当于import , 同样会执行一遍my_module文件 , 同样也会创建命名空间 , 但是from .. . import ... 是将my_module中的名字直接导入到当前的命名空间 , 也就意味着可以直接调用 , 而不用像import那样 , 利用 my_module *.* 名字 来进行调用

两种方式对比

```python
# import方式
import my_module
# 模块名 + '.' + 函数名进行调用
my_module.read()
# from...import...方式
from my_module import read
# 直接用函数名调用
read()
```

PS : 利用from...import...方式进行导入 , 一般用来指定导入模块中的某一部分 , 或者方便使用 , 还有一个特殊的导入 from ... import * (作用是导入模块中的所有内容 , 但是有弊端) 

as

```python
from my_module import read as r
```

多行

```python
from my_module import (read1,
                      read2,
                      read3)
```

## from ... import * 🍀

from my_module import \* 会将my_module 中的所有的不是以下划线 ' _ ' 开头的名字都导入到当前位置 , 在大部分情况下我们python程序不应该使用这种导入方式 , 因为你无法知道 \* 导入了什么名字 , 很有可能会覆盖掉你已经定义过的名字 , 而且可读性极其的差

在my_module.py中新增一行

```python
# 这样在另外一个文件中用from my_module import * 就能导入列表中规定的两个名字
__all__ = ['money' , 'read1']
```

## if \_\_name\_\_ == '\_\_main\_\_' 🍀

所有的模块都有一个内置属性 \_\_name\_\_ , 可以用来查看模块名

在当前文件执行时会返回' \__main__ ', 如果不在当前文件执行那么就会返回所执行的模块名

```python
# my_module.py中
print(__name__)
# 执行my_module.py
执行结果: __main__
```

```python
# test.py中
import my_modlue
# 执行 test.py 
执行结果: my_module
```

所以利用\__name__ 属性 , 我们就可以实现 , 模块可以自己执行 , 也可以导入到别的模块中执行 , 并且他不会执行 **两次 **

```python
# my_module.py中
def main():
    print('we are in %s' % __name__)
# 如果在当前文件下就会执行
if __name__ == '__main__':
    main()
```

```python
# test.py中 , 执行test.py
# 解释from语句时 , 并不会执行my_module中的main()
from my_module import main
# 执行main()
main()
执行结果：we are in my_module
# 结果显示只执行了一次main()
```













