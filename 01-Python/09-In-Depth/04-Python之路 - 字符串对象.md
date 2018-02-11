# Python之路 - 字符串对象
<!-- TOC -->

- [Python之路 - 字符串对象](#python之路---字符串对象)
    - [介绍  🍀](#介绍--🍀)
    - [PyStringObject  🍀](#pystringobject--🍀)
    - [PyString_Type  🍀](#pystring_type--🍀)
    - [创建PyStringObject对象  🍀](#创建pystringobject对象--🍀)
    - [intern机制  🍀](#intern机制--🍀)
        - [PyString_InternInPlace  🍀](#pystring_interninplace--🍀)
        - [特殊的引用计数  🍀](#特殊的引用计数--🍀)

<!-- /TOC -->
## 介绍  🍀

在前面有提到过 "定长对象" 和 "变长对象" , 这是一种对对象的二分法

当然不止这一种 , 还有一种就是 "可变对象(mutable)" 和 "不可变对象(immutable)" , 这种二分法是根据对象维护数据的可变性来进行区分的 , 在Python的官方文档中也是有说到的

可变对象维护的数据在对象被创建后还能再变化 , 比如一个`list`被创建后 , 可以向其中添加元素或删除元素 , 这些操作都会改变其维护的数据 ; 而不可变对象所维护的数据在对象创建之后就不能再改变了 , 比如Python中的`string`和`tuple` , 他们都不支持添加或删除的操作

**Python 2.x 与 Python 3.x**

```python
# Python 2.7
>>> name = 'lyon'
>>> type(name)
<type 'str'>
>>> name.decode('utf-8')
u'lyon'
>>> uname = u'lyon'
>>> type(uname)
<type 'unicode'>

# Python 3.5.2
>>> name = 'lyon'
>>> type(name)
<class 'str'>
>>> name.decode('utf-8')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'str' object has no attribute 'decode'
>>> uname = u'lyon'
>>> type(uname)
<class 'str'>
```

在进行对比两种版本的差异前 , 我们需要知道在它们中有哪些字符串类型 : 

- Python 3.x中 , 有3种字符串类型 : 
  - `str` , 表示`Unicode`文本 (8位的和更宽的)
  - `bytes` , 表示二进制数据
  - `bytearray` , 是bytes的一种可变的变体
- Python 2.x中 , 有2中字符串类型 : 
  - `str` , 表示8位文本和二进制数据
  - `unicode` , 表示宽字符`Unicode`文本

虽然在2中没有`bytesarray`  , 但是在Python 2.6 及之后的版本都可以使用`bytesarray`

**总体差异 :** 

在Python 2.x 与 Python 3.x中 , 字符串的实现主要体现在 , Python 3.x中将Python 2.x中常规的`str`和`Unicode`字符串整合到了一个单独的类型`str`中 ,  以支持常规的和`Unicode`文本 ; 这样的处理使得Python在编码处理方面更加的方便

接下来就来分析Python中的字符串对象了

## PyStringObject  🍀

在Python中 , `PyStringObject`是对字符串对象的实现 , `PyStringObject` 是一个拥有可变长度内存的对象 , 比如 : `"Lyon"` 和 `"KennethReitz"` 这两个字符串对象所需要的内存空间明显是不一样的

同时 , `PyStringObject` 对象又是一个不可变对象 , 即当创建了一个`PyStringObject`对象之后 , 该对象内部维护的字符串就不能再被改变了 , 这一点特性使得`PyStringObject`对象可以作为`dict`的键 , 但是同时也使得一些字符串的操作效率大大降低 , 比如多个字符串的连接操作

`PyStringObject`对象的定义如下 : 

`Python-2.7\Include\stringobject.h :`

```C
35:typedef struct {
36:    PyObject_VAR_HEAD  /* 在前面的篇章已经介绍过了,变长对象宏 */
37:    long ob_shash;
38:    int ob_sstate;
39:    char ob_sval[1];

41:    /* Invariants:
42:     *     ob_sval contains space for 'ob_size+1' elements.
43:     *     ob_sval[ob_size] == 0.
44:     *     ob_shash is the hash of the string or -1 if not computed yet.
45:     *     ob_sstate != 0 iff the string object is in stringobject.c's
46:     *       'interned' dictionary; in this case the two references
47:     *       from 'interned' to this object are *not counted* in ob_refcnt.
48:     */
49:} PyStringObject;
```

定义说明 :

1. `PyObject_VAR_HEAD`中有一个`ob_size`变量保存着对象中维护的可变长度内存的大小

2. `ob_shash`变量的作用是缓存该对象的hash值 , 这样可以避免每一次都重新计算该字符串对象的hash值 , 如果一个`PyStringObject`对象还没有被计算过hash值 , 那么`ob_shash`的初始值是`-1`

   这个hash值在后期`dict`类型中发挥了巨大的作用

3. `ob_sstate`变量标记了该对象是否已经过`intern`机制的处理 , `intern`机制见下文 , 预存的字符串的hash值与`intern`机制将Python虚拟机的执行效率提升了20%

4. `ob_sval`在定义中虽然是一个字符的字符数组 , 但是`ob_sval`实际上是作为一个字符指针指向一段内存的 , 这段内存保存着这个字符串对象所维护的实际字符串 , 而这段内存的实际长度(字节) , 正式通过`ob_size`来维护的 , 这就是变长对象的实现机制 , 比如一个字符串对象 "Lyon" , `ob_size`的值就是4

在Python 3.x中 , 遗留的字符串定义在`unicodeobject.h`中 , 不另行说明了

## PyString_Type  🍀

如下是`PyStringObject`的类型对象的定义 : 

`Python-2.7\Include\stringobject.c :`

```C

3800:PyTypeObject PyString_Type = {
        PyVarObject_HEAD_INIT(&PyType_Type, 0)
        "str",
        PyStringObject_SIZE,
        sizeof(char),
		......
        string_repr,                                /* tp_repr */
        &string_as_number,                          /* tp_as_number */
        &string_as_sequence,                        /* tp_as_sequence */
        &string_as_mapping,                         /* tp_as_mapping */
        (hashfunc)string_hash,                      /* tp_hash */
        0,                                          /* tp_call */
		......
        &PyBaseString_Type,                         /* tp_base */
		......
        string_new,                                 /* tp_new */
        PyObject_Del,                               /* tp_free */
3842:};
```

对于类型对象就无需多说了 , 在前面的篇章也已经介绍过了 , 这里值得注意的是 , `tp_itemsize`和`ob_size`共同决定了应该额外申请的内存之总大小是多少 , `tp_itemsize`指明了由变长对象保存的元素的单位长度 , 这里就是单个字符在内存中的长度

`tp_as_number` , `tp_as_sequence` , `tp_as_mapping` 三个域都被设置了 , 表示`PyStringObject`对数值操作 , 序列操作和映射操作都支持

## 创建PyStringObject对象  🍀

Python 2.7 提供了两个接口 : `PyString_FromString` 和 `PyString_FromStringAndSize` 

`Python-2.7\Include\stringobject.c :`

**PyString_FromString**

```C
119:PyString_FromString(const char *str)
    {
        register size_t size;
        register PyStringObject *op;
	    // 判断字符串长度
        assert(str != NULL);
        size = strlen(str);
        if (size > PY_SSIZE_T_MAX - PyStringObject_SIZE) {
            PyErr_SetString(PyExc_OverflowError,
                "string is too long for a Python string");
            return NULL;
        }
    
        // 处理null string
        if (size == 0 && (op = nullstring) != NULL) {
    #ifdef COUNT_ALLOCS
            null_strings++;
    #endif
            Py_INCREF(op);
            return (PyObject *)op;
        }
    
        // 处理字符
        if (size == 1 && (op = characters[*str & UCHAR_MAX]) != NULL) {
    #ifdef COUNT_ALLOCS
            one_strings++;
    #endif
            Py_INCREF(op);
            return (PyObject *)op;
        }

        /* Inline PyObject_NewVar */
        op = (PyStringObject *)PyObject_MALLOC(PyStringObject_SIZE + size);
        if (op == NULL)
            return PyErr_NoMemory();
        PyObject_INIT_VAR(op, &PyString_Type, size);
        op->ob_shash = -1;
        op->ob_sstate = SSTATE_NOT_INTERNED;
        Py_MEMCPY(op->ob_sval, str, size+1);
        /* share short strings */
        if (size == 0) {
            PyObject *t = (PyObject *)op;
            PyString_InternInPlace(&t);
            op = (PyStringObject *)t;
            nullstring = op;
            Py_INCREF(op);
        } else if (size == 1) {
            PyObject *t = (PyObject *)op;
            PyString_InternInPlace(&t);
            op = (PyStringObject *)t;
            characters[*str & UCHAR_MAX] = op;
            Py_INCREF(op);
        }
        return (PyObject *) op;
169:}
```

传给`PyString_FromString`的参数必须是一个指向以`NUL('\0')` 结尾的字符串的指针

根据定义我们知道 , 在创建`PyStringObject`时 : 

- 首先会检查该字符串数组的长度 , 如果字符数组的长度大于`PY_SSIZE_T_MAX`  , 那么Python将不会创建对应的`PyStringObject`对象 , `PY_SSIZE_T_MAX`是一个与平台相关的值 , 在`WIN32`系统下 , 该值为`2147483647`  , 即2GB 
- 接下来检查传入的字符串是不是一个空串 , 对于空串 , Python并不是每一次都会创建相应的`PyStringObject` ; Python运行时有一个`PyStringObject`对象指针`nullstring`专门负责处理空的字符数组 , 如果第一次在一个空字符串基础上创建`PyStringObject` , 由于`nullstring`指针被初始化为NULL , 所以iPython会为这个字符建立一个`PyStringObject`对象 , 将这个对象通过`intern`机制进行共享 , 然后将`nullstring`指向这个被共享的对象 , 以后再创建空字符串就直接返回`nullstring`的引用了
- 如果不是创建空字符串对象 , 那么就申请内存 , 创建`PyStringObject`对象 ; 处理申请字符串本身所需要的内存外 , 还会申请额外的内存 , 存放了其他的属性 , 以字符数组`"Python"`为例 , 如下图


![PyStringObject内存布局](http://oux34p43l.bkt.clouddn.com/PyStringObject内存布局.png)


**PyString_FromStringAndSize**

```C
 61:PyString_FromStringAndSize(const char *str, Py_ssize_t size)
    {
        register PyStringObject *op;
        if (size < 0) {
            PyErr_SetString(PyExc_SystemError,
                "Negative size passed to PyString_FromStringAndSize");
            return NULL;
        }
        if (size == 0 && (op = nullstring) != NULL) {
    #ifdef COUNT_ALLOCS
            null_strings++;
    #endif
            Py_INCREF(op);
            return (PyObject *)op;
        }
        if (size == 1 && str != NULL &&
            (op = characters[*str & UCHAR_MAX]) != NULL)
        {
    #ifdef COUNT_ALLOCS
            one_strings++;
    #endif
            Py_INCREF(op);
            return (PyObject *)op;
        }

        if (size > PY_SSIZE_T_MAX - PyStringObject_SIZE) {
            PyErr_SetString(PyExc_OverflowError, "string is too large");
            return NULL;
        }

        /* Inline PyObject_NewVar */
        op = (PyStringObject *)PyObject_MALLOC(PyStringObject_SIZE + size);
        if (op == NULL)
            return PyErr_NoMemory();
        PyObject_INIT_VAR(op, &PyString_Type, size);
        op->ob_shash = -1;
        op->ob_sstate = SSTATE_NOT_INTERNED;
        if (str != NULL)
            Py_MEMCPY(op->ob_sval, str, size);
        op->ob_sval[size] = '\0';
        /* share short strings */
        if (size == 0) {
            PyObject *t = (PyObject *)op;
            PyString_InternInPlace(&t);
            op = (PyStringObject *)t;
            nullstring = op;
            Py_INCREF(op);
        } else if (size == 1 && str != NULL) {
            PyObject *t = (PyObject *)op;
            PyString_InternInPlace(&t);
            op = (PyStringObject *)t;
            characters[*str & UCHAR_MAX] = op;
            Py_INCREF(op);
        }
        return (PyObject *) op;
116:}
```

`PyString_FromStringAndSize` 的操作和`PyString_FromString`几乎一样 , 只有一点 , `PyString_FromString`传入的参数必须是以`NUL('\0')` 结尾的字符数组的指针 , 而`PyString_FromStringAndSize`则没有这个要求 , 因为通过传的`size`参数就可以确定需要拷贝的字符的个数

## intern机制  🍀

从上面两种创建方式的源码中发现 , 无论是`PyString_FromString`还是`PyString_FromStringAndSize` , 当字符数组的长度为0或1时 , 需要进行一个特别的操作 : `PyString_InternInPlace` , 这就是字符串的`intern`机制 , 也就是上面代码中`share short strings` 注释下的代码 

```C
 /* share short strings */
if (size == 0) {
    PyObject *t = (PyObject *)op;
    PyString_InternInPlace(&t);
    op = (PyStringObject *)t;
    nullstring = op;
    Py_INCREF(op);
} else if (size == 1 && str != NULL) {
    PyObject *t = (PyObject *)op;
    PyString_InternInPlace(&t);
    op = (PyStringObject *)t;
    characters[*str & UCHAR_MAX] = op;
    Py_INCREF(op);
}
return (PyObject *) op;
```

字符串对象的`intern`机制的目的是 : 对于被共享之后的字符串 , 比如`"Ruby"` , 在整个Python的运行期间 , 系统中都只有唯一的一个与字符串`"Ruby"`对应的 `PyStringObject`对象

当判断两个字符串对象是否相同时 , 如果它们都被共享了 , 那么只需要检查它们对应的`PyObject * `是否相同就可以了 , 这个机制节省了空间 , 如下 : 

```python
# Python 2.7
>>> str1 = 'lyon'
>>> str2 = 'lyon'
>>> id(str1)
79116928L
>>> id(str2)
79116928L

# Python 3.5.2
>>> str1 = 'lyon'
>>> str2 = 'lyon'
>>> id(str1)
2767446375480
>>> id(str2)
2767446375480
```

这个例子的创建过程 : 

1. 因为` 'lyon'` 对象不存在 , 所以调用接口创建`PyStringObject`对象 (创建时经过`intern`机制处理) 
2. Python在查找系统中记录的已经被`intern`机制处理了的`PyStringObject` 对象 (上一步中同样会进行查找) , 发现`'lyon'`字符数组对应的`PyStringObject`已经存在 , 于是返回该对象的引用返回

### PyString_InternInPlace  🍀

我们已经知道了创建字符串对象时进行了特殊的操作`PyString_InternInPlace` , 其源码如下 : 

```C
4712:void
     PyString_InternInPlace(PyObject **p)
     {
         register PyStringObject *s = (PyStringObject *)(*p);
         PyObject *t;
    
    	 // 对PyStringObject进行类型和状态检查
         if (s == NULL || !PyString_Check(s))
             Py_FatalError("PyString_InternInPlace: strings only please!");
         /* If it's a string subclass, we don't really know what putting
            it in the interned dict might do. */
         if (!PyString_CheckExact(s))
             return;
         if (PyString_CHECK_INTERNED(s))
             return;
    
    	 // 创建记录经intern机制处理后的PyStringObject的dict
         if (interned == NULL) {
             interned = PyDict_New();
             if (interned == NULL) {
                 PyErr_Clear(); /* Don't leave an exception */
                 return;
             }
         }
    
    	 // 检查PyStringObject对象s是否存在对应的intern后的PyStrinObject对象
         t = PyDict_GetItem(interned, (PyObject *)s);
         if (t) {
             
             // 调整引用计数
             Py_INCREF(t);
             Py_DECREF(*p);
             *p = t;
             return;
         }

    	 // 在interned中记录检查PyStringObject对象s
         if (PyDict_SetItem(interned, (PyObject *)s, (PyObject *)s) < 0) {
             PyErr_Clear();
             return;
         }
         /* The two references in interned are not counted by refcnt.
            The string deallocator will take care of this */
    	 // 调整引用计数
         Py_REFCNT(s) -= 2;
    
         // 调整s中的intern状态标志
         PyString_CHECK_INTERNED(s) = SSTATE_INTERNED_MORTAL;
4748:}
```

`PyString_InternInPlace` 首先会进行一系列检查 : 

- 检查传入的对象是否是一个`PyStringObject`对象 , `intern`机制只能应用在`PyStringObject`对象上 , 甚至对于它的派生类对象系统都不会应用`intern`机制
- 检查传入的`PyStringObject`对象是否已经被`intern`机制处理过

在代码中 , 我们可以清楚的看到 , `intern`机制的核心在于`interned` , 它指向一个由`PyDict_new`创建的对象 , 也就是一个字典 , 也就是说`intern`机制的关键就是在系统中有一个存在映射关系的集合 , 它的名字叫做`interned` , 这个集合里面记录了被`intern`机制处理过的

### 特殊的引用计数  🍀



