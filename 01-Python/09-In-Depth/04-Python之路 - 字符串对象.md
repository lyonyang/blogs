# Python之路 - 字符串对象
<!-- TOC -->

- [Python之路 - 字符串对象](#python之路---字符串对象)
    - [介绍  🍀](#介绍--🍀)
    - [PyStringObject  🍀](#pystringobject--🍀)
    - [PyString_Type  🍀](#pystring_type--🍀)
    - [创建PyStringObject对象  🍀](#创建pystringobject对象--🍀)

<!-- /TOC -->
## 介绍  🍀

在前面有提到过 "定长对象" 和 "变长对象" , 这是一种对对象的二分法

当然不止这一种 , 还有一种就是 "可变对象(mutable)" 和 "不可变对象(immutable)" , 这种二分法是根据对象维护数据的可变性来进行区分的 , 在Python的官方文档中也是有说到的

可变对象维护的数据在对象被创建后还能再变化 , 比如一个`list`被创建后 , 可以向其中添加元素或删除元素 , 这些操作都会改变其维护的数据 ; 而不可变对象所维护的数据在对象创建之后就不能再改变了 , 比如Python中的`string`和`tuple` , 他们都不支持添加或删除的操作

**Python 2.x 与 Python 3.x**

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

未完待续 ...