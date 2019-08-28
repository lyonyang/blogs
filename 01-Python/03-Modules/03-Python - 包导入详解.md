# Python之路 - 包导入详解

## 介绍  🍀

为了帮助组织模块并提供命名层次结构 , Python有一个概念 : 包

包就相当于一个文件系统的目录 , 模块相当于目录中的文件 , 也就是说所有的包都时模块 , 但不是所有的模块都是包

包只是一种特殊的模块 , 具体来说 , 包含`__path__` 属性的任何模块都被视为包

所有模块都有一个名称 , 子包名与他们的父包名由点隔开 , 类似于Python的标准属性访问语法

Python定义了两种类型的包 , 即 [regular packages](https://docs.python.org/3/glossary.html#term-regular-package) 和  [namespace packages](https://docs.python.org/3/glossary.html#term-namespace-package) , 我们通常使用的就是regular packages , 对于namespace packages可通过上述链接进行学习

## 常规包  🍀

常规包时传统的包 , 因为它们存在于Python 3.2 及更早的版本中 ; 常规包通常实现为包含`__init__.py` 文件的目录 

当我们导入常规包时 , 这个`__init__.py`文件会被隐式执行 (这意味着我们应该在`__init__.py` 文件中完成我们的导入 , 即初始化包) , 它定义的对象被绑定到包命名空间中 ; Python会在导入时为模块添加一些其他属性 , 如下 : 

```python
parent/
    __init__.py
    one/
        __init__.py
    two/
        __init__.py
    three/
        __init__.py
'''
导入parent.one将隐式执行parent/__init__.py和parent/one/__init__.py
随后导入parent.two或parent.three将执行parent/two/__init__.py和parent/three/__init__.py
'''
```

在我们使用`import`导入文件时 , 产生命名空间的名字来源于文件 , `import packages`产生的命名空间的名字同样来源于文件 , 即包下的`__init__.py` , 导入包本质就是在导入该文件

注意 : 在Python 3中 , 即使包下没有`__init__.py`文件 , `import packages`仍然不会报错 , 而在Python 2中 , 包下一定要有该文件 , 否则`import packages`就会抛出异常 

## 导入包  🍀

glance包

```python
glance/                   
├── __init__.py      
├── api                  
│   ├── __init__.py   __all__ = ['policy','versions'] 
│   ├── policy.py
│   └── versions.py
├── cmd               __all__ = ['manage']    
│   ├── __init__.py
│   └── manage.py    
└── db                __all__ = ['models']              
    ├── __init__.py
    └── models.py
```

### import  🍀

```python
import glance.db.models
glance.db.models.register_models('mysql') 
```

### from ... import ...  🍀

```python
# import后接的必须是明确的模块或者方法或者类或者变量,否则会抛出异常
from glance.db import models
models.register_models('mysql')
from glance.db.models import register_models
register_models('mysql')
```

### 绝对导入与相对导入  🍀

我们的glance包时写给别人用的 , 但是在glance包内部也会有彼此之间互相导入的需求 , 那么就有了绝对导入和相对导入两种方式 : 

绝对导入 : 以`glance`作为起始

相对导入 : 用`.`或者`..` 的方式最为起始 , 只能在一个包中使用 , 即包内目录

我们在`glance/api/version.py`中导入`glance/cmd/manage.py`

glance/api/version.py 下

```python
# 绝对导入
from glance.cmd import manage
manage.main()
# 相对导入,一个点表示当前目录,两个点表示上一层
from ..cmd import manage
manage.main()
```

绝对导入

```python
glance/                   
├── __init__.py      from glance import api
                             from glance import cmd
                             from glance import db
├── api                  
│   ├── __init__.py  from glance.api import policy
                              from glance.api import versions
│   ├── policy.py
│   └── versions.py
├── cmd                 from glance.cmd import manage
│   ├── __init__.py
│   └── manage.py
└── db                   from glance.db import models
    ├── __init__.py
    └── models.py
```

相对导入

```python
glance/                   
├── __init__.py      from . import api  #.表示当前目录
                     from . import cmd
                     from . import db
├── api                  
│   ├── __init__.py  from . import policy
                     from . import versions
│   ├── policy.py
│   └── versions.py
├── cmd              from . import manage
│   ├── __init__.py
│   └── manage.py    from ..api import policy   
                     #..表示上一级目录，想再manage中使用policy中的方法就需要回到上一级glance目录往下找api包，从api导入policy
└── db               from . import models
    ├── __init__.py
    └── models.py
```
### 单独导入  🍀

单独导入包时不会导入包中所有包含的所有子模块 , 如 :

```python
import glance
glance.cmd.manage.main()
'''
执行结果:
AttributeError: module 'glance' has no attribute 'cmd'
'''
```

上述导入会隐式执行`__init__.py` , 所以我们可以让这个文件来初始化 , 如下 : 

```python
# glance/__init__.py
from . import cmd
# glance/cmd/__init__.py
from . import manage
```

关于导入系统 : https://docs.python.org/3/reference/import.html