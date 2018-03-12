# Python之路 - Python基础

## Hello World  🍀

学一门语言基本都是从Hello World开始的 , 如下一个最简单的Hello World程序

```python
Python 3.5.2 (v3.5.2:4def2a2901a5, Jun 25 2016, 22:18:55) [MSC v.1900 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> print("Hello World")
Hello World
>>>
```

此为Python 3.5.2版本 , 上述代码为在Windows环境命令行中执行 , 即以管理员身份运行 "命令提示符"

```python
# 已添加环境变量
C:\Windows\system32>python
```

Python 2.7.x 版本的Hello World程序

```python
Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:53:40) [MSC v.1500 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> print "Hello World"
Hello World
>>>
```

当然使用`Python shell` 仅仅适合处理一些非常简单的小程序 , 对于比较复杂 , 代码量稍微大一点的就不适合了



## 变量  🍀

变量用于存储在计算机程序中被引用和操作的信息

变量可能被明确为是能表示可变状态、具有存储空间的抽象(如在Java和Visual Basic中) , 变量的唯一目的是在内存中标记和存储数据 , 这些数据可以在整个程序中使用

声明变量

```python
# 声明一个变量name,并绑定值"Lyon"
name = "Lyon"
# 同时为多个变量赋值
a = b = c = 1
```

Python变量定义的规则 : 

1. 变量名只能是 字母、数字或者下划线的任意组合

2. 变量名的第一个字符不能是数字

3. 以下关键字不能声明为变量名 , 属于Python中的保留字and

   | and      | exec    | not    |
   | -------- | ------- | ------ |
   | assert   | finally | or     |
   | break    | for     | pass   |
   | class    | from    | print  |
   | continue | global  | raise  |
   | def      | if      | return |
   | del      | import  | try    |
   | elif     | in      | while  |
   | else     | is      | with   |
   | except   | lambda  | yield  |

## 行和缩进  🍀

Python 与其他语言最大的区别就是 , Python 的代码块不使用大括号 `{}` 来控制类 , 函数以及其他逻辑判断 ,  Python 最具特色的就是用缩进来写模块

缩进的空白数量是可变的 , 但是所有代码块语句必须包含相同的缩进空白数量 , 这个必须严格执行

```python
if True:
    print "True"
else:
  print "False"
'''
执行会出现错误提醒:
IndentationError: unexpected indent
'''
```

`IndentationError: unexpected indent` 错误是Python编译器在告诉你 , 你的文件里格式有问题 , 可能是tab和空格没对齐的问题

还有`IndentationError: unindent does not match any outer indentation level` 错误表明 , 你使用的缩进方式不一致 , 有的是 tab 键缩进 , 有的是空格缩进 , 改为一致即可。

因此 , 在 Python 的代码块中必须使用相同数目的行首缩进空格数

建议你在每个缩进层次使用 **单个制表符** 或 **两个空格** 或 **四个空格** , 切记不能混用

## 多行语句  🍀

Python语句中一般以新作为为语句的结束符

但是我们可以使用斜杠 ` \ ` 将一行的语句分为多行显示 , 如下 :

```python
total = item_one + \
        item_two + \
        item_three
```

语句中包含 [], {} 或 () 括号就不需要使用多行连接符 , 如下实例 : 

```python
days = ['Monday', 'Tuesday', 'Wednesday',
        'Thursday', 'Friday']
```

**同一行使用多条语句**

Python可以在同一行中使用多条语句 , 语句之间使用分号 `;`  分割 , 如下 :

```python
#!/usr/bin/python
import sys; x = 'runoob'; sys.stdout.write(x + '\n')
```

## 字符串  🍀

Python 可以使用引号( **'** )、双引号( **"** )、三引号( **'''** 或 **"""** ) 来表示字符串 , 引号的开始与结束必须的相同类型的

其中三引号可以由多行组成 , 编写多行文本的快捷语法 , 常用于文档字符串 , 在文件的特定地点 , 被当做注释

```python
word = 'word'
sentence = "This is a sentence"
paragraph = """This is a paragraph
			   Contains multiple statements"""
```

## 注释  🍀

Python中单行注释采用 ` # ` 开头

```python
# 第一个注释
print("Hello,Python")  # 第二个注释
```

Python中多行注释采用三个单引号 ` ''' ` 或三个双引号 `""" ` 

```python
'''
这是多行注释，使用单引号。
这是多行注释，使用单引号。
这是多行注释，使用单引号。
'''
"""
这是多行注释，使用双引号。
这是多行注释，使用双引号。
这是多行注释，使用双引号。
"""
```

## 字符编码  🍀

Python解释器在加载 `.py` 文件中的代码时 , 会对内容进行编码 (默认ASCII)

然而ASCII是无法处理中文的 , 所以如果我们的代码中出现了中文 , 那么需要在代码的顶端加上一句声明

```python
#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
第一行,为脚本语言指定解释器
第二行,告诉Python解释器,用utf-8编码来进行编码
'''
```

## 用户输入  🍀

当我们需要用户自己输入信息时 , 就可以使用`input` 语句 , 如下 : 

```python
# 让用户进行输入,并用变量name接收用户输入的值
name = input("Please input your name:")
```

上述代码 , 会一直等待用户输入 , 直到用户按回车键后才会退出

## 输出  🍀

当我们需要让控制台输出一些我们想要的信息时 , 可以使用`print` 语句 , 在Hello World里我们已经见到了

```python
#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Author:Lyon
x="a"
y="b"
# 换行输出
print(x)
print(y)
print('---------')
# 不换行输出
print(x,)
print(y,)
# 不换行输出
print(x,y)
'''
执行结果:
a
b
---------
a b a b
'''
```

## 数据类型  🍀

我们知道在变量创建时 , 会在内存中开辟一个空间 , 用来存放变量的值 , 而这些变量的值可以是各种各样的类型 ,  如 : 数字 , 字符串 , 列表 , 元组 , 字典 , 集合等等

**数字类型**

1. int (整型)

   整数的大小范围由计算机字长确定

2. long (长整型)

   跟C语言不同 , Python的长整数没有指定位宽 , 即 : Python没有限制长整数数值的大小 , 但实际上由于机器内存有限 , 我们使用的长整数数值不可能无限大

   注意 , 自从Python 2.2 起 , 如果整数发生溢出 , Python会自动将整数数据转换为长整数 , 所以如今在长整数数据后面不加字母 L 也不会导致严重后果了

3. float (浮点型)

   浮点数用来处理实数 , 即带有小数的数字 , 类似于C语言中的double类型 , 占8个字节(64位) , 其中52位表示底 , 11位表示指数 , 剩下的一位表示符号

4. complex (复数)

   复数由实数部分和虚数部分组成，一般形式为x+yh，其中的x是复数的实数部分，y是复数的虚数部分，这里的x和y都是实数

注 : Python中存在整数小数字池 : -5~257 , 在此范围的整数数字共享

**布尔值**

即真或假 , 1或0

更多数据类型 , 后续文章中详细整理

## 数据运算  🍀

算术运算符

| 运算符  | 描述                        | 实例                                       |
| ---- | ------------------------- | ---------------------------------------- |
| +    | 加 - 两个对象相加                | a + b 输出结果 30                            |
| -    | 减 - 得到负数或是一个数减去另一个数       | a - b 输出结果 -10                           |
| *    | 乘 - 两个数相乘或是返回一个被重复若干次的字符串 | a * b 输出结果 200                           |
| /    | 除 - x除以y                  | b / a 输出结果 2                             |
| %    | 取模 - 返回除法的余数              | b % a 输出结果 0                             |
| **   | 幂 - 返回x的y次幂               | a**b 为10的20次方 ,  输出结果 100000000000000000000 |
| //   | 取整除 - 返回商的整数部分            | 9//2 输出结果 4 , 9.0//2.0 输出结果 4.0          |

比较运算符

| 运算符  | 描述                                       | 实例                         |
| ---- | ---------------------------------------- | -------------------------- |
| ==   | 等于 - 比较对象是否相等                            | (a == b) 返回 False          |
| !=   | 不等于 - 比较两个对象是否不相等                        | (a != b) 返回 True           |
| <>   | 不等于 - 比较两个对象是否不相等                        | (a <> b) 返回 True这个运算符类似 != |
| >    | 大于 - 返回x是否大于y                            | (a > b) 返回 False           |
| <    | 小于 - 返回x是否小于y , 所有比较运算符返回1表示真 , 返回0表示假<br />这分别与特殊的变量True和False等价 , 注意 , 这些变量名的大写 | (a < b) 返回 True            |
| >=   | 大于等于	- 返回x是否大于等于y。                       | (a >= b) 返回 False          |
| <=   | 小于等于 - 返回x是否小于等于y。                       | (a <= b) 返回 True           |

赋值运算符

| 运算符   | 描述       | 实例                           |
| ----- | -------- | ---------------------------- |
| =     | 简单的赋值运算符 | c = a + b 将 a + b 的运算结果赋值为 c |
| +=    | 加法赋值运算符  | c += a 等效于 c = c + a         |
| -=    | 减法赋值运算符  | c -= a 等效于 c = c - a         |
| *=    | 乘法赋值运算符  | c *= a 等效于 c = c * a         |
| /=    | 除法赋值运算符  | c /= a 等效于 c = c / a         |
| %=    | 取模赋值运算符  | c %= a 等效于 c = c % a         |
| \*\*= | 幂赋值运算符   | c \*\*= a 等效于 c = c \*\* a   |
| //=   | 取整除赋值运算符 | c //= a 等效于 c = c // a       |

位运算符

| 运算符  | 描述                                       | 实例                                       |
| ---- | ---------------------------------------- | ---------------------------------------- |
| &    | 按位与运算符 : 参与运算的两个值 , 如果两个相应位都为1 , 则该位的结果为1 , 否则为0 | (a & b) 输出结果 12  , 二进制解释 :  0000 1100    |
| \    | 按位或运算符 : 只要对应的二个二进位有一个为1时 , 结果位就为1       | (a  丨 b) 输出结果 61  , 二进制解释 :  0011 1101   |
| ^    | 按位异或运算符 : 当两对应的二进位相异时 , 结果为1             | (a ^ b) 输出结果 49  , 二进制解释 :  0011 0001    |
| ~    | 按位取反运算符 : 对数据的每个二进制位取反 , 即把1变为0 , 把0变为1  , ~x 类似于 -x-1 | (~a ) 输出结果 -61  , 二进制解释 :  1100 0011 , 在一个有符号二进制数的补码形式 |
| <<   | 左移动运算符 : 运算数的各二进位全部左移若干位 , 由 << 右边的数字指定了移动的位数 , 高位丢弃 , 低位补0 | a << 2 输出结果 240 , 二进制解释 :  1111 0000     |
| >>   | 右移动运算符 : 把">>"左边的运算数的各二进位全部右移若干位 , >> 右边的数字指定了移动的位数 | a >> 2 输出结果 15  , 二进制解释 :  0000 1111     |

逻辑运算符

| 运算符  | 逻辑表达式   | 描述                                       | 实例                    |
| ---- | ------- | ---------------------------------------- | --------------------- |
| and  | x and y | 布尔"与" - 如果 x 为 False , x and y 返回 False , 否则它返回 y 的计算值 | (a and b) 返回 20       |
| or   | x or y  | 布尔"或"	- 如果 x 是非 0 , 它返回 x 的值 , 否则它返回 y 的计算值 | (a or b) 返回 10        |
| not  | not x   | 布尔"非" - 如果 x 为 True , 返回 False  , 如果 x 为 False , 它返回 True | not(a and b) 返回 False |

成员运算符

| 运算符    | 描述                                 | 实例                                |
| ------ | ---------------------------------- | --------------------------------- |
| in     | 如果在指定的序列中找到值返回 True , 否则返回 False   | x 在 y 序列中 , 如果 x 在 y 序列中返回 True   |
| not in | 如果在指定的序列中没有找到值返回 True , 否则返回 False | x 不在 y 序列中 , 如果 x 不在 y 序列中返回 True |

身份运算符

| 运算符    | 描述                        | 实例                                       |
| ------ | ------------------------- | ---------------------------------------- |
| is     | is 是判断两个标识符是不是引用自一个对象     | **x is y ** , 类似 **id(x) == id(y)** , 如果引用的是同一个对象则返回 True , 否则返回 False |
| is not | is not 是判断两个标识符是不是引用自不同对象 | **x is not y**  ,  类似 **id(a) != id(b) , 如果引用的不是同一个对象则返回结果 True , 否则返回 False |

运算符优先级表 , 从上到下优先级依次增高

| Operator                                 | Description                              |
| ---------------------------------------- | ---------------------------------------- |
| [`lambda`](https://docs.python.org/3/reference/expressions.html?highlight=operator%20precedence#lambda) | Lambda expression                        |
| [`if`](https://docs.python.org/3/reference/compound_stmts.html#if) – [`else`](https://docs.python.org/3/reference/compound_stmts.html#else) | Conditional expression                   |
| [`or`](https://docs.python.org/3/reference/expressions.html?highlight=operator%20precedence#or) | Boolean OR                               |
| [`and`](https://docs.python.org/3/reference/expressions.html?highlight=operator%20precedence#and) | Boolean AND                              |
| [`not`](https://docs.python.org/3/reference/expressions.html?highlight=operator%20precedence#not) `x` | Boolean NOT                              |
| [`in`](https://docs.python.org/3/reference/expressions.html?highlight=operator%20precedence#in), [`not in`](https://docs.python.org/3/reference/expressions.html?highlight=operator%20precedence#not-in), [`is`](https://docs.python.org/3/reference/expressions.html?highlight=operator%20precedence#is), [`is not`](https://docs.python.org/3/reference/expressions.html?highlight=operator%20precedence#is-not), `<`, `<=`, `>`, `>=`, `!=`, `==` | Comparisons, including membership tests and identity tests |
| `丨`                                      | Bitwise OR                               |
| `^`                                      | Bitwise XOR                              |
| `&`                                      | Bitwise AND                              |
| `<<`, `>>`                               | Shifts                                   |
| `+`, `-`                                 | Addition and subtraction                 |
| `*`, `@`, `/`, `//`, `%`                 | Multiplication, matrix multiplication, division, floor division, remainder [[5\]](https://docs.python.org/3/reference/expressions.html?highlight=operator%20precedence#id21) |
| `+x`, `-x`, `~x`                         | Positive, negative, bitwise NOT          |
| `**`                                     | Exponentiation [[6\]](https://docs.python.org/3/reference/expressions.html?highlight=operator%20precedence#id22) |
| `await` `x`                              | Await expression                         |
| `x[index]`, `x[index:index]`, `x(arguments...)`, `x.attribute` | Subscription, slicing, call, attribute reference |
| `(expressions...)`, `[expressions...]`, `{key: value...}`, `{expressions...}` | Binding or tuple display, list display, dictionary display, set display |

## if ... else  🍀

场景一 : 用户登录验证

```python
# 导入getpass模块
import getpass
# 等待用户输入
name = input("请输入用户名：")
# 等待用户输入密码,密码不可见
password = getpass.getpass("请输入密码：")
# 如果用户密码正确,执行如下
if name =="Lyon" and password =="yang":
    print("欢迎你!")
# 否则执行如下
else：
    print("用户名或密码错误")
```

场景二 : 猜年龄游戏

```python
# 定义一个年龄
age =21 
# 用户输入
user_input = int(input("input your guess num:"))
if user_input == age:
    print("Congratulations, you got it !")
elif user_input < age:
    print("Oops,think bigger!")
else:
    print("think smaller!")
```

## for循环  🍀

循环10次

```python
for i in range(10):
    print("loop:", i )
'''
执行结果:
loop: 0
loop: 1
loop: 2
loop: 3
loop: 4
loop: 5
loop: 6
loop: 7
loop: 8
loop: 9
'''
```

小于5就跳入下一次循环

```python
for i in range(10):
    if i<5:
        continue
    print("loop:"i)
```

## while循环  🍀

写一个死循环

```python
count = 0
while True：
    print("你是风儿我是沙，缠缠绵绵走天涯",count)
    count +=1
```