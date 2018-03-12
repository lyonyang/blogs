# Python之路 - 函数

## 介绍  🍀

函数是组织好的 , 可重复使用的 , 用来实现单一 , 或相关联功能的代码段

函数能提高应用的模块性 , 和代码的重复利用率 , 比如我们一直使用的`print()`  , `input()`  等等 , 都是函数

如下我们写了一个用户认证程序 ; 而现在我们又需要写一个用户管理系统 , 管理系统中有很多的功能 , 比如添加用户 , 删除用户 , 查询用户 , 修改用户 ; 但是这些功能必须先通过用户认证程序才能使用 , 明显我们不可能在每一个功能前加上一段用户认证代码 , 因为这将大大增加我们的重复代码

那么为了解决这个问题我们就可以将用户认证功能封装到一个函数之中 , 而后续我们如果需要使用这个函数仅需调用即可 , 着就是函数的魅力所在 , 当然更多的还是通过下面进一步了解函数

## 语法  🍀

```python
# 自定义函数,function_name为函数名
def function_name():
    """注释"""
    
    '''
    功能代码块
    '''
    # 返回值,一般都具有返回值,当然也不可以不设定
    return result
```

简单实例

```python
def hello():
    print("Hello Lyon!")
    return None
```

**注意 :** 上述仅为定义函数 , 函数并不会执行 , 只有当函数被调用时 , 函数内部代码才会执行

## 函数调用  🍀

函数调用通过*函数名*后加`()` 进行调用 , 如下 :

```python
# 定义函数
def hello():
    print("Hello Lyon!")
    return None
# 调用函数
hello()
```

既然函数调用是通过函数名后加括号 , 在这个固定语法之中前者函数名有是什么? 如下 : 

```python
# 定义函数
def hello():
    print("Hello Lyon!")
    return None
# 打印函数名
print(hello)
'''
执行结果:
<function func at 0x000001D7E3FF7F28>
'''
```

我们可以发现 , 函数名打印出来的是一个内存地址 , 由此不难理解 : 

**函数名相当于一个变量 , 而变量的值就是该函数本身所在的内存地址 ; 也就是说函数名实际上就是一个指针 , 它与函数本身存在一个映射关系**

## 参数说明  🍀

**形参 :** 变量只有在被调用时才分配内存单元 , 在调用结束时 , 即刻释放所分配的内存单元 ; 因此 , 形参只在函数内部有效 , 函数调用结束返回主调用函数后则不能再使用该形参变量

**实参 : **可以是常量、变量、表达式、函数等 , 无论实参是何种类型的量 , 在进行函数调用时 , 它们都必须有确定的值 , 以便把这些值传送给形参 ; 因此应预先用赋值 , 输入等办法使参数获得确定值

```python
# 定义函数func
def func(argument1,argument2):    # argument1与argument2都为形参,形式参数
    print(argument1,argument2)
    
# 调用函数func
func("Hello", "Lyon")             # Hello和Lyon都是实参,实际参数
'''
执行结果:
Hello Lyon
'''
```

**位置参数 :** 即参数必须以正确的顺序传入函数 , 传入的数量必须和声明的一样 , 不一样就报错

```python
# 用户登录验证
def login(username,password):
    if username == "Lyon" and password == "123456":
        print("Login successfully!")
    else:
        print("Login failed!")
# 进行调用
login("Lyon","123456")       
# 进行调用
login("Lyon","78910JkQ")       
'''
执行结果:
Login successfully!
Login failed!
'''
```

### 默认参数  🍀

调用时不指定就以默认值传入 , 指定则按指定值传入

```python
# 同时定义位置参数和默认参数
def add_userinfo(name,age,province="北京"):
  	return name,province
# 位置参数必填,默认参数可选
add_userinfo("Lyon",18)
'''
执行结果:
('Lyon', '北京')
'''
```

注：通过默认参数，我们就算不传参数也不会报错 , 即`province` 默认为`"北京"` 

### 关键字参数  🍀

正常情况下 , 给函数传参数的时候要按照顺序传 , 如果不想按照顺序就可以使用关键参数

```python
def add_userinfo(name,age,province="北京"):
  	return name,province
add_userinfo("Lyon",province="湖北",age=18)
# 注意关键参数不用按照顺序传入,但是关键参数必须写在位置参数后面
```

### 非固定参数  🍀

当我们想要传入多个参数 , 但是我们又不确定的时候就可以使用非固定参数 ; 非固定参数有两个 , 一个 `*args (元组形式)`  以及 `**kwargs (字典形式) ` 

```python
# 设定两个非固定参数
def main(*args,**kwargs):
	# 打印args,以及args的类型
    print(args,type(args))
    # 打印kwargs,以及kwargs的类型
    print(kwargs,type(kwargs))
# 调用
main((1,2,3,4),{1:2,3:4})
```

对于非固定参数 , 其主要在于`*` 号 , `*` 号的作用是进行打包与解包 :

- 一个`*` 号 , 则表示打包成元组或者将元组进行解包 , 过程如下 : 

  ```python
  def main(n,*args):
  	return args
  # 传递参数,第一个参数被认为是位置参数n,余后参数*号将会对其进行打包成元组,但参数形式必须符合元组规范
  result = main(1,2,3,4,5)
  print(result)
  '''
  执行结果:
  (2, 3, 4, 5)
  '''
  '''
  额外说明:
  传递参数时,*号将参数封装成一个元组,即元组args
  '''
  ```

- 两个`**` 号 , 则表示打包成字典或者将字典进行解包 , 过程如下 : 

  ```python
  def main(**kwargs):
  	return kwargs
  # 传递参数,**号将会对其进行打包成字典,但参数形式必须符合字典规范,即必须key-value
  result = main(n2=2,n3=3,n4=4)
  print(result)
  '''
  执行结果:
  {'n4': 4, 'n2': 2, 'n3': 3}
  '''
  '''
  额外说明:
  传递参数时,**号将参数封装成一个字典,即字典kwargs
  '''
  ```

- 两者的解包如下 :

  ```python
  # 进行打包
  def main(*args,**kwargs):      # 参数状态:(1,2,3,4,5){'n1':1,'n2':2,'n3'=3}
      # 进行解包
      return (*args),{**kwargs}  # 参数状态:1,2,3,4,5,n1=1,n2=2,n3=3
  result = main(1,2,3,4,5,n1=1,n2=2,n3=3)
  print(result)
  '''
  执行结果:
  (1, 2, 3, 4, 5, {'n2': 2, 'n3': 3, 'n1': 1})
  '''
  # 解包补充
  '''只要是可迭代对象我们都可以对其进行解包,如下'''
  mytuple = (1,2,3,4,5,6,7)
  # _为占位符,*c打包成列表
  a,_,b,*c,d = mytuple
  print(a)
  print(b)
  print(c)
  print(d)
  '''
  执行结果:
  1
  3
  [4, 5, 6]
  7
  '''
  ```

### 参数顺序及组合  🍀

**参数顺序**

在函数头部 (定义参数) :  一般参数 → 默认参数 →  非固定参数`*args` →  非固定参数`**kwargs` 

在函数调用中 (传递参数) : 位置参数 → 关键字参数 →  默认参数 →  非固定参数`*args` →  非固定参数`**kwargs`

**参数组合** 

在我们使用过程中 , 如果没有非固定参数 , 那么我们的关键参数或者默认参数可以用关键字进行传递 ; 如果有非固定参数 , 必须按照位置参数的方式进行传递

默认参数和非固定参数`*args`位置可以进行调换 , 调换后默认参数传递需要加上关键字

## 全局与局部变量  🍀

局部变量：只在函数内部起作用的变量

全局变量：在整个程序中都起作用

```python
# 全局变量name
name = "Lyon"
def func(name):
    print(name)
    # 局部变量name
    name = "Kenneth"  
    print(name)
# 调用函数
func(name)
print(name)
'''
执行结果:
Lyon
Kenneth
Lyon
'''
```

总结 : 全局变量**作用域**是整个程序 , 局部变量**作用域**是定义该变量的子程序 ; 当全局变量与局部变量同名时 : 在定义局部变量的子程序内 , 局部变量起作用 ; 在其他地方全局变量起作用

**global语句 : **可以将局部变量变成全局变量 , 在函数内部变量前加上 global 即可如 : `global name`  

## return语句  🍀

`return` 语句用于返回函数的执行结果 , 比如操作类函数一般都不需要返回值 , 当然可由我们的需要自己进行设定

不使用`return` 即返回None , 没有返回值

我们函数在执行过程中如果遇到return语句 , 就会结束并返回结果

```python
def sum( arg1, arg2 ):
	# 返回2个参数的和
	total = arg1 + arg2
	print("两数之和:",total)
	return total
	# 上一步函数就已经结束,不会往下执行
	print("已经返回!")
# 调用sum函数
total = sum( 10, 20 )
'''
执行结果:
两数之和: 30
'''
```
如果我们返回函数名

```python
def func():
    print("I am Lyon")
    # 返回func,函数名 → 内存地址
    return func
# result1接收返回值func函数名
result1 = func()
# 返回一个函数对象
print(result1)
# 可以继续调用
result2 = result1()
print(result2)
result2()
'''
执行结果:
I am Lyon
<function func at 0x0000013C309B7F28>
I am Lyon
<function func at 0x0000013C309B7F28>
I am Lyon
'''
```

这是一处妙用 , 当然在单层函数中作用不明显 , 下一章的《Python之路 - 函数进阶》中的闭包可以让你体会魅力之所在