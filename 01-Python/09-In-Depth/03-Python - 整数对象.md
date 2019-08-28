# Python之路 - 整数对象

**欢迎收藏交流 , 如需转载 , 请注明出处**
## 介绍  🍀

在Python的应用程序中 , 整数的使用非常地广泛

这就意味着整数对象的创建和销毁肯定是非常的频繁的 , 并且我们知道Python中采用了引用计数机制 , 即一个整数类型的变量`ob_refcnt` , 这样Python中对于整数对象的创建和销毁会更加的疯狂 , 这样的执行效率明显我们是无法接受的 , 更何况Python已经背负了人们对其执行效率的不满 , 所以Python中大量采用了内存对象池的技术

整数对象必然也使用了内存对象池技术 , 也就是整数对象池 , 当然我们应该从整数对象的创建开始说起 , 以及Python 2.x中与Python 3.x两个版本之间的差异

## 整数类型  🍀

**Python 2.x中的整数类型**

在Python 2.x中有两种整数类型 , 一种是`int` 也就是我们通常说的整型 , 另一种是`long`也就是长整型 , 根据两种对象的源码 , 我们可以知道 , `int` (PyIntObject) 属于定长对象 , 而`long` (PyLongObject) 属于变长对象

对于`int` , 当其进行运算时 , 如果值溢出 , 那么Python将会将值自动转为`long`类型 , 如下 : 

```python
# python 2.x
>>> n = 2147483647
>>> type(n)
<type 'int'>
# 加法溢出
>>> n = n + 1
>>> n
2147483648L
>>> type(n)
<type 'long'>
>>> n = -2147483647
>>> type(n)
<type 'int'>
# 减法溢出
>>> n = n - 2
>>> n
-2147483649L
>>> type(n)
<type 'long'>
```

但是`long`就不会出现这种溢出情况了 , 因为`long`是一个变长对象 , 当空间不够存放这个数字值 , 加空间就是了 , 无非是从1Byte 到2 Byte的过程 , 以此类推 

**Python 3.x中的整数类型**

在Python 3.x中 , 只有`long`了 , 我们所见到的`int`实际上就是`long` , 根据源码的注释所说 , 大概意思就是对于未来而言 , `long`比`int`好 , 并且在Python 3.x的[官方文档](https://docs.python.org/3.5/c-api/long.html)中 , 第一句就说明了 : 

```
All integers are implemented as “long” integer objects of arbitrary size.
```

还有一点值得注意的就是 , 在3.x的源码中 , 已经没有`intobject.h`这个文件了 , 而只有`longobject.h`  , 我们可以在`Python-3.5.4\Objects\longobject.c`中看到`long`的类型信息 : 

```C
5179:PyTypeObject PyLong_Type = {
     PyVarObject_HEAD_INIT(&PyType_Type, 0)
     "int",                                      /* tp_name */
     offsetof(PyLongObject, ob_digit),           /* tp_basicsize */
     sizeof(digit),                              /* tp_itemsize */
     long_dealloc,                               /* tp_dealloc */
     0,                                          /* tp_print */
     0,                                          /* tp_getattr */
     0,                                          /* tp_setattr */
     0,                                          /* tp_reserved */
     long_to_decimal_string,                     /* tp_repr */
     &long_as_number,                            /* tp_as_number */
     0,                                          /* tp_as_sequence */
     0,                                          /* tp_as_mapping */
     (hashfunc)long_hash,                        /* tp_hash */
     0,                                          /* tp_call */
     long_to_decimal_string,                     /* tp_str */
     PyObject_GenericGetAttr,                    /* tp_getattro */
     0,                                          /* tp_setattro */
     0,                                          /* tp_as_buffer */
     Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE |
         Py_TPFLAGS_LONG_SUBCLASS,               /* tp_flags */
     long_doc,                                   /* tp_doc */
     0,                                          /* tp_traverse */
     0,                                          /* tp_clear */
     long_richcompare,                           /* tp_richcompare */
     0,                                          /* tp_weaklistoffset */
     0,                                          /* tp_iter */
     0,                                          /* tp_iternext */
     long_methods,                               /* tp_methods */
     0,                                          /* tp_members */
     long_getset,                                /* tp_getset */
     0,                                          /* tp_base */
     0,                                          /* tp_dict */
     0,                                          /* tp_descr_get */
     0,                                          /* tp_descr_set */
     0,                                          /* tp_dictoffset */
     0,                                          /* tp_init */
     0,                                          /* tp_alloc */
     long_new,                                   /* tp_new */
     PyObject_Del,                               /* tp_free */
5220:};
```

注意 : 在此文件中还有一个`long_as_number` 域 , 其中定义了一个对象作为数值对象时所有可选的操作 , 其中2.7中一共有39个函数指针 , 3.5.2中一共有34个函数指针 , 每一个函数指针都代表着一种可选的操作 , 包括加法 , 减法 , 乘法 , 模运算等等 ; 具体行数见`5142-5176` 

**创建方式**

对于整数对象的创建 , 其途径都定义在`intobject.c`或者`longobject.c`中 , 方式都不止一种 , 例如创建`int`就有以下3种方式 : 

1. 从long值创建 , `PyInt_FromLong(long ival)`
2. 从Py_UNICODE对象生成 , `PyInt_FromUnicode(Py_UNICODE *s, int length, int base)`
3. 从字符串生成 , `PyInt_FromString(char *s, char **pend, int base)`

而对于创建`long`方法就更多了 , 这些创建方法都定义在`Python\Objects\`目录下对应的`.c`文件中


## 小整数对象池  🍀

在实际编程中 , 数值比较小的整数 , 比如 1, 2, 29等 , 可能在程序中会非常频繁地使用 ; 在Python中 , 所有的对象都存货在系统堆上 , 也就是说 , 如果没有特殊的机制 , 对于这些频繁使用的小整数对象 , Python将一次又一次使用malloc在堆上申请空间 , 并且不厌其烦地一次次free释放空间 , 这样的操作会严重影响Python的整体性能

所以Python中对于小整数对象使用了**对象池技术** , 也就是Python会直接将小整数对象缓存在内存中 , 并将其指针存放在`small_ints`中 , 这个小整数集合的范围无论是在Python 2.x 还是在Python 3.x , 其范围都设定在[-5, 257)  , 源码如下 : 

`Python-2.7\Objects\intobject.c`

```C
67:#ifndef NSMALLPOSINTS
68:#define NSMALLPOSINTS           257
69:#endif
70:#ifndef NSMALLNEGINTS
71:#define NSMALLNEGINTS           5
72:#endif
73:#if NSMALLNEGINTS + NSMALLPOSINTS > 0
/* References to small integers are saved in this array so that they
   can be shared.
   The integers that are saved are those in the range
   -NSMALLNEGINTS (inclusive) to NSMALLPOSINTS (not inclusive).
*/
79:static PyIntObject *small_ints[NSMALLNEGINTS + NSMALLPOSINTS];
```

`Python-3.5.4\Objects\longobject.c`

```C
12:#ifndef NSMALLPOSINTS
13:#define NSMALLPOSINTS           257
14:#endif
15:#ifndef NSMALLNEGINTS
16:#define NSMALLNEGINTS           5
17:#endif

25:#if NSMALLNEGINTS + NSMALLPOSINTS > 0
/* Small integers are preallocated in this array so that they
   can be shared.
   The integers that are preallocated are those in the range
   -NSMALLNEGINTS (inclusive) to NSMALLPOSINTS (not inclusive).
*/
31:static PyLongObject small_ints[NSMALLNEGINTS + NSMALLPOSINTS];
```

**小整数池测试**

```python
# Python 2.7
>>> a = 1
>>> id(a)
87319208L
>>> b = 1
>>> id(b)
87319208L

# Python 3.5.3
>>> a = 1
>>> id(a)
1852703184
>>> b = 1
>>> id(b)
1852703184
```

超出小整数集合的整数对象 , 内存地址就不一样了 , 这一点可以自己尝试

对于小整数集合的范围我们是可以修改的 , 但是修改的方法非常原始 , 那就是修改Python的源码然后重新编译

注意 : **小整数对象池**中完全地缓存其对象 , 也就是说在执行我们的程序之前**小整数对象池**就已经激活


## 通用整数对象池  🍀

小整数对象池解决了小整数频繁的使用问题 , 但是我们并不能保证大整数就不会被频繁的使用 , 所以对于这些整数 , Python运行环境将提供一块内存空间 , 供这些大整数轮流使用 , 结构体如下 : 

`Python-2.7\Objects\intobject.c` 

```C
33:#define BLOCK_SIZE      1000    /* 1K less typical malloc overhead */
34:#define BHEAD_SIZE      8       /* Enough for a 64-bit pointer */
35:#define N_INTOBJECTS    ((BLOCK_SIZE - BHEAD_SIZE) / sizeof(PyIntObject))

37:struct _intblock {
38:    struct _intblock *next;
39:    PyIntObject objects[N_INTOBJECTS];
40:};

42:typedef struct _intblock PyIntBlock;

44:static PyIntBlock *block_list = NULL;
45:static PyIntObject *free_list = NULL;
```

在上述结构体中 , `N_INTOBJECTS`表示所维护的对象的个数 , 在32位的系统上 , 一个`int`类型所需要的内存为12bytes , 所以可以计算出这个值应该是82 , 这一个值我们也可以通过修改源码进行修改

而`PyIntBlock`的单向列表通过`block_list`维护 , 每一个block中都维护了一个`PyIntObject`数组 , 这就是真正用于存储被缓存的`PyIntObject`对象的内存 , 而对于这个内存中的空闲内存则是由单向链表`free_list`进行管理 ; 最开始时这两个指针都指向一个空值 (NULL)

在Python 3.5.4中 , 我没有找到如同2.7一样的源码 , 但是我们可以通过两个版本的实验发现 , 通用对象池机制是一样的 :

```python
# Python 2.x
>>> id(257),id(258),id(259)
(81956248L, 81956224L, 81956200L)
>>> n = 258
>>> id(n)
81956248L

# Python 3.x
>>> id(257),id(258),id(259)
(1910529789904, 1910534766192, 1910534766096)
>>> n = 258
>>> id(n)
1910529789904
```

在进行实验时 , 走了很多弯路 , 有兴趣的话可以自己尝试 , 下面是上面实验的结果总结 : 

1. 申请完内存之后 , Python解释器就再也不会返回内存给操作系统了 , 就算对象被销毁
2. 创建大整数对象时 , 会到堆里面找最近的那一块空内存 , 注意堆里面存储数据是由高到低进行存储的
3. 也就是说 , 通用整数对象池机制所做的优化就是 , **解决了内存的频繁开辟问题**

注意 : 如果第一块空间满了 , 那么就会往第二块进行存储 ; 


## 添加和删除  🍀

通过使用`PyInt_FromLong` API为例 , 创建一个整数对象的过程如下 : 

`Python-2.7\Objects\intobject.c` 

```C
 87:PyInt_FromLong(long ival)
 88:{
 89:   register PyIntObject *v;
 90:#if NSMALLNEGINTS + NSMALLPOSINTS > 0
   	/* 尝试使用小整数对象池 */
   
 91:   if (-NSMALLNEGINTS <= ival && ival < NSMALLPOSINTS) {
 92:       v = small_ints[ival + NSMALLNEGINTS];
 93:       Py_INCREF(v);
 94:#ifdef COUNT_ALLOCS
 95:       if (ival >= 0)
 96:           quick_int_allocs++;
 97:       else
 98:           quick_neg_int_allocs++;
 99:#endif
100:        return (PyObject *) v;
101:    }
102:#endif
  	 /* 为通用整数对象池申请新的内存空间 */
  
103:    if (free_list == NULL) {
104:        if ((free_list = fill_free_list()) == NULL)
105:            return NULL;
106:    }
107:    /* Inline PyObject_New */
108:    v = free_list;
109:    free_list = (PyIntObject *)Py_TYPE(v);
110:    PyObject_INIT(v, &PyInt_Type);
111:    v->ob_ival = ival;
112:    return (PyObject *) v;
113:}
```

`Python-3.5.4\Objects\longobject.c` 中`25行至296行` 可以查看到关于Python 3中的一些处理

```C
37:get_small_int(sdigit ival)
   {
       PyObject *v;
       assert(-NSMALLNEGINTS <= ival && ival < NSMALLPOSINTS);
       v = (PyObject *)&small_ints[ival + NSMALLNEGINTS];
       Py_INCREF(v);
   #ifdef COUNT_ALLOCS
       if (ival >= 0)
           quick_int_allocs++;
       else
           quick_neg_int_allocs++;
   #endif
       return v;
50:}
51:#define CHECK_SMALL_INT(ival) \
    do if (-NSMALLNEGINTS <= ival && ival < NSMALLPOSINTS) { \
        return get_small_int((sdigit)ival); \
54:    } while(0)

231:PyLong_FromLong(long ival)
   { 
  	   ......
239:   CHECK_SMALL_INT(ival);
       ......
296:}
```

也就是说整数对象的创建会通过两步来完成 : 

1. 如果小整数对象池机制被激活 (默认就已激活) , 则尝试使用小整数对象池
2. 如果不能使用小整数对象池 , 则使用通用的整数对象池

对于整数对象的实现大概核心就是这些东西了 , 关于通用对象池的创建 , 可以通过源码或者 , 《Python源码剖析》一书进行探索

