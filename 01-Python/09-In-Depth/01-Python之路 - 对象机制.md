# Python之路 - 对象机制  

**欢迎收藏交流 , 如需转载 , 请注明出处**
## 介绍  🍀

在Python中一切皆对象 

我们知道Python是用C语言设计出来的 , 而在Python中 , 对象就是C中的结构体在堆上申请的一块内存

对象是不能被静态初始化的 , 并且也不能在栈空间上生存 ; 唯一列外的就是类型对象 , Python中所有的内建类型对象 (如整数类型对象 , 字符串类型对象) 都是被静态初始化的

在Python中 , 一个对象一旦被创建 , 那么它在内存中的大小就固定不变了 , 这就意味着对于那些可变长度的数据对象 (如列表) , 只能在对象内维护一个指向一块可变大小的内存区域的指针

利用这种对象机制可以使由指针维护对象的工作变得非常的简单

## 对象机制的基石  🍀

Python中一切皆对象 , 而所有的对象都拥有一些相同的内容 , 其被定义在`PyObject`中

我们先对比源码 , 从源码目录`Python-2.7\Include\object.h`中 , 截取如下片段 :

```C
106:typedef struct _object {
107:    PyObject_HEAD      /*这个宏如下*/
108:} PyObject;


77:/* PyObject_HEAD defines the initial segment of every PyObject. */
78:#define PyObject_HEAD                 \
79:    _PyObject_HEAD_EXTRA              \
/* Py_ssize_t 是一个所占字节数与 size_t 相同的有符号的整数类型*/
80:    Py_ssize_t ob_refcnt;             \
81:    struct _typeobject *ob_type;


65:/* Define pointers to support a doubly-linked list of all live heap objects. */
66:#define _PyObject_HEAD_EXTRA            \
67:    struct _object *_ob_next;           \
68:    struct _object *_ob_prev;
```

从源码目录`Python-3.5.4\Include\object.h`中 , 截取如下片段 :

```C
106:typedef struct _object {
107:    _PyObject_HEAD_EXTRA     /* 与2.7相比没有发生任何实质性变化 */
108:    Py_ssize_t ob_refcnt;     
109:    struct _typeobject *ob_type;
110:} PyObject;


82:/* PyObject_HEAD defines the initial segment of every PyObject. */
83:#define PyObject_HEAD                   PyObject ob_base;


70:/* Define pointers to support a doubly-linked list of all live heap objects. */
71:#define _PyObject_HEAD_EXTRA            \
72:    struct _object *_ob_next;           \
73:    struct _object *_ob_prev;

75:#define _PyObject_EXTRA_INIT 0, 0,

78:#else
79:#define _PyObject_HEAD_EXTRA
```

 两个版本源码并没有什么真正意义上的改变 , 从中我们可以看出 , `PyObject`主要由`ob_refcnt` , `ob_type`  , `_PyObject_HEAD_EXTRA` 几个部分组成 , 而对于`_PyObject_HEAD_EXTRA` , 我们发现它只有在DEBUG模式下才不为空 , 所以我们可以将其忽略


### ob_refcnt  🍀

`ob_refcnt` 是内存管理机制的核心 , 它实现了基于`引用计数`的垃圾回收机制 , 例如 : 

对于某一个对象A , 当有一个新的`PyObject *` (对象指针) 引用该对象时 , A的引用计数 (ob_refcnt) 就会增加 ; 而当这个`PyObject *` 被删除时 , A的引用计数就会减少 , 并且当A的引用计数减少到0时 , A就可以从堆上被删除 , 以释放出内存供别的对象使用

`ob_refcnt`是一个32位的整型变量 , 这实际蕴含着Python所做的一个假设 , 即对一个对象的引用不会超过一个整型变量的最大值 , 这个假设如果不是恶意代码的话 , 明显是成立的

### ob_type  🍀

`ob_type`是对象类型的核心 , 源码中我们可以看到 , 它是一个指向`_typeobject`的结构体的指针 , 该结构体对应的是一种特殊的对象 , 它是用来指定一个对象类型的类型对象 , 也就是说`ob_type`所指向的位置存放着一个对象的类型信息

Python就是利用`ob_type`构造了对象类型的基石

`PyObject`中定义了所有Python对象中都必须有的内容 , 即`ob_refcnt`和`ob_type`  , 当然一个对象中肯定不止于这些 , 不同的对象中还保存了各自的特殊信息 , 于是才实现了各种基础数据类型


## 定长对象和变长对象  🍀

### 定长对象  🍀

我们把不包含可变长度数据的对象称为 "定长对象" , 并且定长对象在内存中所占的大小是一样的 , 比如我们的整数对象 , 内存中 1 和 100占用的内存大小都是`sizeof(PyIntObject)` 

你可能会将定长对象理解为 "不可变对象" , 但是实际上并不是这样 , 因为像Python的字符串 , 元组这两者都是 "不可变对象" , 但是他们却是 "变长对象" , 我们通过源码来看看Python中的整数对象 :

目录`Python-2.7\Include\intobject.h`中 , 截取如下片段 :

```C
23:typedef struct {
24:    PyObject_HEAD   /*PyObject对象宏 */
25:    long ob_ival;   /*PyIntObject的特殊信息*/
26:} PyIntObject;
```

如上 , 也就是说在Python 2.x中 , 整数对象都是定长对象 , 因为`PyIntObject`结构体中没有任何多余的内容 , 但是别忘了数字还有`Long`类型 , 而`Long`则是变长对象

源码如下 : 

`Python-2.7\Include\longintrepr.h`中 , 截取如下片段 :

```C
90:struct _longobject {
91:	PyObject_VAR_HEAD     /*变长对象基石*/
92:	digit ob_digit[1];    
93:};
```

注意 : 在Python 3.x中 , `Long`类型和`Int`类型合并到一起去了 , 我们在3.x中所看到的`Int`类型 , 实际上是`Long`  类型 , 关于数字类型将会在下一篇中整理

Python 3.x中这部分源码也在`logintrepr.h`中 , 分别在第89 - 92行

### 变长对象  🍀

上面已经说明了定长对象 , 变长对象则就是包含可变长度数据的对象

定长对象与变长对象的区别在于 : 定长对象占用的内存大小是一样的 , 而变长对象占用的大小不一样 , 实例如下 : 

```python
>>> a = 1
>>> type(a)
<type 'int'>
>>> a.__sizeof__()
24
>>> b = 100
>>> type(b)
<type 'int'>
>>> b.__sizeof__()
24
```

注意 : 字符串是变长对象 , Python2.7中源码如下 : 

```C
// Python2.7\Include\stringobject.h

35:typedef struct {
36:    PyObject_VAR_HEAD    /*变长对象基石*/
37:    long ob_shash;
38:    int ob_sstate;
39:    char ob_sval[1];
  /* 省略注释 */
49:} PyStringObject;
```

实例说明

```python
# env : Python 2.x
>>> a = "lyon"
>>> b = "lyonyang"
>>> a.__sizeof__()
37
>>> b.__sizeof__()
41
```


### PyVarObject  🍀

`PyVarObject`就是Python中变长对象的基石 , 上面的`PyStringObject`中我们已经见过了, 那么继续翻源码 : 

`Python-2.7\Include\object.h : `

```C
110:typedef struct {
111:    PyObject_VAR_HEAD
112:} PyVarObject;

/* PyObject_VAR_HEAD defines the initial segment of all variable-size
 * container objects.  These end with a declaration of an array with 1
 * element, but enough space is malloc'ed so that the array actually
 * has room for ob_size elements.  Note that ob_size is an element count,
 * not necessarily a byte count.
 */
96:#define PyObject_VAR_HEAD               \
97:    PyObject_HEAD                       \
98:    Py_ssize_t ob_size; /* Number of items in variable part */
```

`Python-3.5.4\Include\object.h : `

```C
112:typedef struct {
113:    PyObject ob_base;   /* 等价于PyObject_HEAD */
114:    Py_ssize_t ob_size; /* Number of items in variable part */
115:} PyVarObject;
```

版本2.7 与 3.5.4无变化 , 我们可以看出 , PyVarObject其实就是在PyObject上的一个扩展而已 , 而这个扩展就是在PyVarObject中多出了一个`ob_size`变量 , 这是一个整型变量 , 该变量记录的是变长对象中一共容纳了多少个元素

注意 : 变长对象通常都是容器 , 并且`ob_size`指明的是所容纳元素的个数 , 而不是字节的数量 , 比如一个列表中有5个元素 , 那么`ob_size`的值就是5

所以对于判断Python底层实现的对象是否是变长对象 , 只需查看其定义中是否具有`ob_size`属性


## 类型对象  🍀

上面已经提到过了在`PyObject`中有一个`ob_type`指针 , 它指向对象的类型信息 , 这样在分配内存空间时 , 就可以根据`ob_type`所指向的信息来决定对象申请多大的空间

`ob_type`指向结构体`_typeobject` , 如下 : 

`Python-2.7\Include\object.h :`

```C
324:typedef struct _typeobject {
325:    PyObject_VAR_HEAD
326:    const char *tp_name; /* For printing, in format "<module>.<name>" */
327:    Py_ssize_t tp_basicsize, tp_itemsize; /* For allocation */
329:	/* Methods to implement standard operations */
  		...
338:    /* Method suites for standard classes */
  		...
344:	/* More standard operations (here for binary compatibility) */
  		...
411:} PyTypeObject;
```

`Python-3.5.4\Include\object.h : `

```C
343:typedef struct _typeobject {
344:    PyObject_VAR_HEAD
345:    const char *tp_name; /* For printing, in format "<module>.<name>" */
346:    Py_ssize_t tp_basicsize, tp_itemsize; /* For allocation */

348:    /* Methods to implement standard operations */
		...
358:    /* Method suites for standard classes */
		...
364:    /* More standard operations (here for binary compatibility) */

432:} PyTypeObject;
```

同样 , 在版本2.7 与 3.5.4之间不能存在差异

我们可以将该结构体主要分为4个部分 : 

1. 类型名 , 即`tp_name` , 主要是Python内部以及调试的时候使用
2. 创建该类型对象时分配内存空间大小的信息 , 即 `tp_basicsize` , `tp_itemsize` 
3. 与该类型对象相关联的操作信息 , 可以通过源码进行详查
4. 类型的类型信息

由于在PyObject的定义中包含了PyTypeObject , 我们可以认为PyObject对象是继承了PyTypeObject对象 , 而PyTypeObject则是最原始的抽象

因为在实际的Python中确实如此 : object类 (即PyObject) 的基类就是type类 (即PyTypeObject)

我们用Python简单描述 : 

```python
>>> isinstance(object, type)
True
```

并且由于Python对外提供了C API , 以及Python本身就是用C写成的 , 所以Python内部也大量使用了这些API

Python中的API分为两种 :

1. 范型API , 或者称为AOL (Abstract Object Layer) , 这类API都具有诸如Pyobject_***的形式 , 可以应用于任何Python对象上
2. 类型相关API  , 或者称为COL (Concrete Object Layer) , 这类API通常只能作用在某一种类型的对象上 , 对于Python内建对象 , 都提供了这样一组API , 诸如PyInt_Type

所以对于Python中的内建类型对象 , 可以利用以上两种API进行创建 : 

1. 范型API : `PyObject *intobj = PyObject_New(PyObject, &PyInt_Type)` 
2. 类型API : `PyObject *intobj = PyInt_FromLong(10)`

注意 : 我们经常所见到的`<type 'int'>`中的 `int` 代表的就是Python内部的`PyInt_Type` 

**总结 :**

通过这一篇文章我们已经理清了Python对象机制中的核心定义

以下从上往下依次扩展

PyTypeObject     - - 类型对象基石

PyObject              - - 对象基石

PyVarObject        - - 变长对象基石



