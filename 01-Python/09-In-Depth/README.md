# The road to Python - In-Depth


<extoc></extoc>

## Python总体架构  🍀

Python总体分为三个部分 , 即文件组 , Python核心 (解释器) , 运行环境 , 如下 : 

```
   File Groups          Python Core			Runtime Environment
			INTERPRETER
+---------------+   +----------------+
| Core Modules  |   |    Scanner     |  ↓
+---------------+   +----------------+	    +--------------------------+
| Library       |   |    Parser      |  ↓   |  Object/Type Structures  |
+---------------+   +----------------+	    +--------------------------+
| User-defined  |   |    Compiler    |	↓   |  Memory Allocator        |
|    Modules    |   +----------------+	    +--------------------------+
+---------------+   |  Code Evauator |	↓   |  Current State of Python |
	            +----------------+	    +--------------------------+
```

## 源码组织  🍀

我们可以在Python官网中获取源码 , 即http://www.python.org

本目录下深入整理主要参考Python 2.7 与Python 3.5.4源码

参考书籍 : Python源码剖析——深度探索动态语言核心技术

Python 源码目录结构如下 : 

```
Python
├── Doc
├── Grammar
├── Include
├── Lib
├── Mac
├── Misc
├── Modules
├── Objects
├── Parser
├── PC
├── PCbuild
├── Programs
├── Python
└── Tools
```

主要说明 , 其中加粗部分为主要分析对象 :
 
 
**`Include`** : 该目录下包含了Python提供的所有头文件 , 如果用户需要自己用C或C++来编写自定义模块扩展Python , 那么就需要用到这里提供的头文件
 
 
`Lib` : 该目录包含了Python自带的所有标准库 , Lib中的库都是用Python语言编写的
 
 
`Modules` : 该目录中包含了所有用C语言编写的模块 , 比如random , cStringIO等 ; Modules中的模块时那些对速度要求非常严格的模块 , 而有一些对速度没有太严格要求的模块 , 比如os , 就是用Python编写的 , 并且放在Lib目录下
 
 
`Parser` : 该目录中包含了Python解释器中的Scanner和Parser部分 , 即对Python源代码进行词法分析和语法分析的部分 ; 除了这些 , Parser目录下还包含了一些有用的工具 , 这些工具能够根据Python语言的语法自动生成Python语言的词法和语法分析器 , 与YACC非常类似
 
 
**`Objects`** : 该目录中包含了所有Python的内建对象 , 包括整数 , list , dict等 , 同时 , 该目录还包括了Python在运行时需要的所有的内部使用对象的实现
 
 
`Python` : 该目录下包含了Pyton解释器中的Compiler和执行引擎部分 , 是Python运行的核心所在
 
 
`PCBuild` : 包含了VS使用的工程文件


