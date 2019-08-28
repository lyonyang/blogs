# Python之路 - 异常处理

## 介绍  🍀

在我们写程序时难免会出现错误 , 一种为语法错误 , 即为python解释器的语法检测都通不过的错误 , 这种错误只能我们在程序执行前就处理好 . 另一种为逻辑错误 , 这是我们在程序设计时所出现的错误 , 也就是我们通常所说的bug 

在编程过程中为了增加友好性 , 在程序出现bug时一般不会将错误信息显示给用户 , 而是显示一个提示错误的页面

基本语法

```python
try:
    pass
except Exception as e:
    pass
# except: 默认就为Exception
```

实例

```python
try:0
    # 用户输入
    num = input("Please input the number:")
    # 遇到无法int的对象就用except进行捕获
    int(num)
# 利用ValueError来捕获错误,并将捕获的错误返回给e     
except ValueError as e:
    # 打印捕获信息
    print(e)
'''
执行结果: 
Please input the number:Lyon
invalid literal for int() with base 10: 'Lyon'
'''
```

PS : 在try代码块中只要出现异常 , 那么代码块中异常后面的代码就不会执行了

## 异常种类  🍀

Python中的异常种类非常多 , 上述中说了个ValueError只能处理值错误 , 当我们需要处理其他的错误时 , 就需要对症下药了 , 并且异常其实也是class , 并且所有的异常都继承了BaseException类

常用异常

| 异常名称              | 说明                                       |
| ----------------- | ---------------------------------------- |
| ValueError        | 传入无效的参数                                  |
| AttributeError    | 与对象的属性相关                                 |
| IOError           | 输入/输出操作失败 , 基本上是无法打开文件                   |
| ImportError       | 无法引入模块或包 , 基本上是路径问题或名称错误                 |
| IndentationError  | 缩进错误                                     |
| IndexError        | 下标索引超出范围 , 即索引不存在                        |
| KeyError          | 字典中不存在该key                               |
| KeyboardInterrupt | 用户中断执行 , 即被Ctrl + C                      |
| NameError         | 变量还未声明/初始化                               |
| SyntaxError       | 语法错误                                     |
| TypeError         | 传入对象类型与要求的不符合                            |
| UnboundLocalError | 试图访问一个还未被设置的局部变量，基本上是由于另有一个同名的全局变量，导致你以为正在访问它 |
| ValueError        | 传入无效的参数                                  |

继承关系与其他异常

```python
# 所有异常都继承自BaseException类
BaseException 
 +-- SystemExit
 +-- KeyboardInterrupt
 +-- GeneratorExit
 +-- Exception
      +-- StopIteration
      +-- StopAsyncIteration
      +-- ArithmeticError
      |    +-- FloatingPointError
      |    +-- OverflowError
      |    +-- ZeroDivisionError
      +-- AssertionError
      +-- AttributeError
      +-- BufferError
      +-- EOFError
      +-- ImportError
           +-- ModuleNotFoundError
      +-- LookupError
      |    +-- IndexError
      |    +-- KeyError
      +-- MemoryError
      +-- NameError
      |    +-- UnboundLocalError
      +-- OSError
      |    +-- BlockingIOError
      |    +-- ChildProcessError
      |    +-- ConnectionError
      |    |    +-- BrokenPipeError
      |    |    +-- ConnectionAbortedError
      |    |    +-- ConnectionRefusedError
      |    |    +-- ConnectionResetError
      |    +-- FileExistsError
      |    +-- FileNotFoundError
      |    +-- InterruptedError
      |    +-- IsADirectoryError
      |    +-- NotADirectoryError
      |    +-- PermissionError
      |    +-- ProcessLookupError
      |    +-- TimeoutError
      +-- ReferenceError
      +-- RuntimeError
      |    +-- NotImplementedError
      |    +-- RecursionError
      +-- SyntaxError
      |    +-- IndentationError
      |         +-- TabError
      +-- SystemError
      +-- TypeError
      +-- ValueError
      |    +-- UnicodeError
      |         +-- UnicodeDecodeError
      |         +-- UnicodeEncodeError
      |         +-- UnicodeTranslateError
      +-- Warning
           +-- DeprecationWarning
           +-- PendingDeprecationWarning
           +-- RuntimeWarning
           +-- SyntaxWarning
           +-- UserWarning
           +-- FutureWarning
           +-- ImportWarning
           +-- UnicodeWarning
           +-- BytesWarning
           +-- ResourceWarning
```

为什么要说继承关系 , 因为在使用except是 , 它不但捕获该异常 , 还会把该异常类的子类也全部捕获

 所以我们把 ` Exception` 也叫做万能异常 ,  因为除了SystemExit , KeyboardInterrupt 和 GeneratorExit 三个异常之外 , 其余所有异常基本都为Exception的子类

## 异常其他结构  🍀

多分支

```python
name = 'Lyon'
try:
    int(name)
except IndexError as e:
    print(e)
except KeyError as e:
    print(e)
# ValueError捕获成功
except ValueError as e:
    print(e)
# 执行结果:invalid literal for int() with base 10: 'Lyon'
```

else

```python
num = '1'
try:
   int(num)
except ValueError as e:
    print(e)
# 与for..else 和 while...else类似,没被打断就执行
else:
    print('没有异常就执行我')
# 执行结果: 没有异常就执行我
```

finally

```python
num = 'Lyon'
try:
   int(num)
except ValueError as e:
    print(e)
else:
    print('没有异常就执行我')
finally:
    print('不管怎么样都执行我')
'''
执行结果:
invalid literal for int() with base 10: 'Lyon'
不管怎么样都执行我
'''
```

## 主动触发异常  🍀

raise

```python
try:
    raise TypeError('类型错误')
except Exception as e:
    print(e)
# 执行结果: 类型错误
```

## 自定义异常  🍀

通过继承BaseException来实现

```python
class LyonException(BaseException):
    def __init__(self,msg):
        self.msg = msg
    def __str__(self):
        return self.msg
try:
    # 主动触发异常
    raise LyonException('你就是错了,别问为什么')
# 捕获LyonException
except LyonException as e:
    print(e)
# 执行结果: 你就是错了,别问为什么    
```

## 断言  🍀

断定条件成立 , 不成立就出现AssertionError异常

```python
try:
    # 断定1等于1
    assert 1 == 1
    print('第一个断言成功就执行')
    assert 2 == 1
    print("第二个断言失败不执行")
# 捕获AssertionError异常
except Exception:
    print("抓到你了")
'''
执行结果:
第一个断言成功就执行
抓到你了
'''
```



***注意 :***

​	不要在任何地方都使用try...except , 因为它本身就是你附加给你程序的一种异常处理的逻辑 , 与你的主要的工作是没有关系的 , 这种东西加多了 , 会导致你的代码可读性变差 , 只有在有些异常无法与之的情况下 , 才应该使用try...except , 其他的逻辑错误应该尽量自行修正













