# Python之路 - 函数进阶

## 嵌套函数  🍀

嵌套函数即函数里面再套一个函数 , 如下 : 

```python
# 全局变量name
name = "Lyon_1"
def func():
    # 第一层局部变量name
    name = "Lyon_2"
    print("第1层打印",name)
    
    #嵌套
    def func2():
        # 第二层局部变量name
        name = "Lyon_3"
        print("第2层打印", name)
        
        # 嵌套
        def func3():
            # 第三层局部变量
            name = "Lyon_4"
            print("第3层打印", name)
        # 调用内层函数
        func3()     
    # 调用内层函数
    func2()  
func()
print("最外层打印", name)
'''
执行结果:
第1层打印 Lyon_2
第2层打印 Lyon_3
第3层打印 Lyon_4
最外层打印 Lyon_1
'''
```

嵌套函数不能越级调用 , 也就是说我们不能在`func2` 的外部去调用`func3` , 当然反过来我们的代码就进入无限递归了

当然我们有时需要的就是在嵌套函数中 , 使用上一层的变量 , 那么我们可以使用`nonlocal` 语句

`nonlocal` 的作用就是改变变量的作用域 , 但是不会扩展到全局变量 , 即只能在函数内部改变 ; nonlocal声明之后 , 会从上层开始找并返回第一个变量 , 没找到则会报错

```python
def func(arg):
    n = arg
    def func1():
        n = 2
        def func2():
            nonlocal n      # n = 2
            n += 1
        func2()
        print(n)        # n = 3
    func1()
    print(n)
func(10)
'''
执行结果:
3
10
'''
```

## 高阶函数  🍀

高阶函数就是将一个函数以参数的形式传入另一个函数

```python
# 定义一个主函数,并设置一个参数func
def main_func(func):
	# 返回func的值
    return func

# 定义一个函数作为参数传入主函数
def func():
    # 返回"Lyon"给func()
    return "Lyon"

# res接收main_func的返回值,将func()的返回值作为参数传入main_func函数    
res = main_func(func())
print(res)
'''
执行结果:
Lyon
'''
```

## 闭包  🍀

闭包必须是内部定义的函数 (嵌套函数) , 该函数包含对外部作用域而不是全局作用域名字的引用

```python
def foo():
    # 局部变量name
    name = 'Lyon'
    # 内部定义的函数
    def bar():
        # 引用了外部定义的变量name,即内部函数使用外部函数变量,这一行为就叫闭包
        print("I am",name)
        return "In the bar"
    # 调用bar并打印结果
    print(bar())
    return "In the foo"
# 调用foo并打印结果
print(foo())
'''
执行结果:
I am Lyon
In the bar
In the foo
'''
```

在嵌套函数中 , 我们可以将函数作为参数 (高阶函数) 或者返回值进行传递 , 函数作为一个值可以赋给变量 , 如下 : 

```python
def decorator(func):
    """func变量在inner函数外部"""
    print("I am decorator")
    def inner():
        print("I am inner")
        # 内部函数引用外部变量func,而func是一个函数对象,因此我们可以进行调用,此处闭包
        func()
    # 内部调用inner函数
    inner()
    # 返回inner,函数名 → 内存地址
    return inner

# decorator函数的参数函数
def decorator_arg():
    print("I am decorator_arg")
    # 返回decorator_arg,函数名 → 内存地址
    return decorator_arg
# result接收的是inner函数名
result = decorator(decorator_arg)
print('-------------------')
# 实际调用的是嵌套函数中内部的inner函数
result()
'''
执行结果:
I am decorator
I am inner
I am decorator_arg
-------------------
I am inner
I am decorator_arg
'''
"""
说明:
从本例子可以看出我们利用闭包,
打破了嵌套函数不能越级调用的规则,
实现了从外部调用内部函数
"""
```

所以利用闭包我们可以实现两种需求 :

- 在不修改源代码的情况下给函数增加功能
- 为某个函数的参数进行提前赋值

### 添加功能  🍀

如果我们以相同的变量名去覆盖函数名 , 修改上述代码 , 如下 : 

```python
def decorator(func):
    def inner():
        print("I am decorator")
        func()
    # 此处删去inner调用    
    return inner
def func():
    print("I am func")
    return func
# func变量名覆盖了func()的函数名
func = decorator(func)
# 实际调用inner()
func()
'''
执行结果:
I am decorator
I am func
'''
"""
说明:
通过对函数名进行覆盖,使我们的func变成了inner,
而原来的func已经成为了inner的一部分,
"""
```

通过定义了变量`decorator`  , 使其原来的函数`decorator()` 被覆盖 , 也就是说我们实现了在不修改`func()` 函数的情况下 , 为`func()` 函数新添加了一个功能 , 当然上述例子中的功能仅仅是打印一句 "I am decorator"

当然我们还可以这样 : 

```python
def func():
    print("I am func")
    return 
def decorator(func):
    print("I am decorator")
    func()
    return decorator
func = decorator(func)
'''
执行结果:
I am decorator
I am func
'''
# 此版本调用方式不同,所以一般不使用
```

闭包方式加参数版 : 

```python
def decorator(func):
    # 此处将原始func参数进行打包
    def inner(*args,**kwargs):
        print("I am decorator")
        # 此处将原始func参数进行拆包返还
        func(*args,**kwargs)
    return inner
def func(*args,**kwargs):
    print("I am func")
    print(args,kwargs)
    return func
func = decorator(func)
# inner(*args,**kwargs)
func( )
```

### 提前赋值  🍀

```python
def func():
    name = "Lyon"
    def inner():
        print(name)
    return inner
func = func()
# 调用之前name的值已经传入inner中
func()
"""
为什么要提前赋值?
因为如果我们将name定义到inner内部,那么只要inner一执行完毕,Python解释器就会把name释放
如果我们要执行一万次这样的操作,那么Python解释器就需要如此申请和释放一万次,会造成内存浪费
"""
```

一道面试题的翻译版本

```python
def func():
    l = []
    for i in range(10):
        # inner函数并没有进行调用,但是for循环已经执行完毕,此时i=9
        def inner(x):
            return i + x
        l.append(inner)
    return l
res = func()
print(res[0](10))
print(res[1](10))
print(res[2](10))
print(res[3](10))
'''
执行结果:
19
19
19
19
'''
"""
说明:
这里虽然结果都为19,但是由for循环生成的10个函数却不是同一个函数,
在执行时,i的值通过绑定的方式进入每一个函数,直到for循环执行完毕,
i的值固定在9,等你再调用时就全为9了
"""
```

面试题原版

```python
# 知识点:列表生成式,匿名函数,闭包
s = [lambda x: x + i for i in range(10)]
print(s[0](10))
print(s[1](10))
print(s[2](10))
print(s[3](10))
```

对于闭包 , 我们可以使用`__closure__` 属性查看闭包函数中引用变量的取值 , `__closure__` 里包含了一个元组 , 这个元组中的每个元素是`cell` 类型的对象 , 默认为None

```python
def func():
    name = "Lyon"
    def inner():
        print(name)
    return inner
# 内部inner
print(func().__closure__)
'''
执行结果:
(<cell at 0x0000023A0F6BB888: str object at 0x0000023A0F1A8B20>,)
'''
```

## 装饰器  🍀

装饰器即给原来的函数进行装饰的工具

装饰器由函数去生成 , 用于装饰某个函数或者方法 (类中的说法) , 它可以让这个函数在执行之前或者执行之后做某些操作

装饰器其实就是上一节闭包中的添加功能实现 , 不过使用闭包太过麻烦 , 所以Python就创造出一个语法糖来方便我们使用

语法糖 : 指那些没有给计算机语言添加新功能 , 而只是对人类来说更"甜蜜"的语法 , 语法糖主要是为程序员提供更实用的编码方式 , 提高代码的可读性 , 并有益于更好的编码风格

语法糖如下 : 

```python
# 装饰器函数
def decorator(func):
    def inner():
        func()
	return inner
# 语法糖,@ 函数名
@decorator     
# 被装饰函数
def func():
	pass
```

该语法糖只是将我们闭包中最后自己处理的部分进行处理了 , 如下 : 

```python
@decorator
	↓ 等价
func = decorator(func)
```

另一种一般不使用的方式 : 

```python
# 装饰器函数
def decorator(func):
	return func()
# 语法糖,@ 函数名
@decorator     
# 被装饰函数
def func():
	pass
```

实例

```python
def decorator(func):
    def inner():
        print("I am decorator")
        func()   
    return inner
@decorator    # → func = decorator(func)
def func():
    print("I am func")
    return func
func()
'''
执行结果:
I am decorator
I am func
'''
```

多个装饰器装饰同一个函数

```python
def decorator1(func):
    def inner():
        return func()
    return inner

def decorator2(func):
    def inner():
        return func()
    return inner

@decorator1
@decorator2
def func():
    print("I am func")
func()
```

被装饰函数带有参数

```python
def decorator(func):
    def inner(*args,**kwargs):
        return func(*args,**kwargs)
    return inner

@decorator
def func(name):
    print("my name is %s" % name)
func("Lyon")
```

带参数的装饰器

```python
F = False
def outer(flag):
    def decorator(func):
        def inner(*args,**kwargs):
            if flag:
                print('before')
                ret = func(*args,**kwargs)
                print('after')
            else:
                ret = func(*args, **kwargs)
            return ret
        return inner
    return decorator

@outer(F)      # outer(F) = decorator(func)
def func():
    print('I am func')
```

我们利用装饰器虽然功能达到了 , 但是注意原函数的元信息却没有赋值到装饰器函数内部 , 比如函数的注释信息 , 如果我们需要将元信息也赋值到装饰器函数内部 , 可以使用functools模块中的`wraps()`方法 , 如下 :

```python
import functools
def outer(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        print(inner.__doc__)
        return func()
    return inner
@outer
def func():
    """
    I am func
    """
    return None
func()
```

