# Python之路 - Tuple对象
<!-- TOC -->

- [Python之路 - Tuple对象](#python之路---tuple对象)
    - [介绍  🍀](#介绍--🍀)
    - [PyTupleObject  🍀](#pytupleobject--🍀)
    - [创建与维护](#创建与维护)
    - [设置元素  🍀](#设置元素--🍀)
    - [对象缓冲池  🍀](#对象缓冲池--🍀)

<!-- /TOC -->
**欢迎收藏交流 , 如需转载 , 请注明出处**
## 介绍  🍀

Python中的`tuple`与`str`一样 , 都属于不可变对象 , 即其所维护的数据在对象创建之后就不能再改变了

直接看PyTupleObject吧

## PyTupleObject  🍀

`Python-2.7\Include\tupleobject.h:`

```C
24:typedef struct {
25:    PyObject_VAR_HEAD
26:    PyObject *ob_item[1];
27:
28:    /* ob_item contains space for 'ob_size' elements.
29:     * Items must normally not be NULL, except during construction when
30:     * the tuple is not yet visible outside the function that builds it.
31:     */
32:} PyTupleObject;
```

通过上面的代码清单 , 我们可以看到 , PyTupleObject除了是一个不可变对象之外 , 它还是一个变长对象 ; 而`ob_item` 则为指向元素列表的指针 

通过前面的整理 , 对于这些再熟悉不过了

## 创建与维护

PyTupleObject对象的创建同其他对象一样 , 其是通过`PyTuple_New`来创建的

`Python-2.7\Objects\tupleobject.c`

```C
 48:PyObject *
    PyTuple_New(register Py_ssize_t size)
    {
        register PyTupleObject *op;
        Py_ssize_t i;
     	// 大小为负数
        if (size < 0) {
            PyErr_BadInternalCall();
            return NULL;
        }
    #if PyTuple_MAXSAVESIZE > 0
     	// 如果是空元组,直接取free_list第一个返回
        if (size == 0 && free_list[0]) {
            op = free_list[0];
            Py_INCREF(op);
    #ifdef COUNT_ALLOCS
            tuple_zero_allocs++;
    #endif
            return (PyObject *) op;
        }
     	// 缓冲池可用
        if (size < PyTuple_MAXSAVESIZE && (op = free_list[size]) != NULL) {
            free_list[size] = (PyTupleObject *) op->ob_item[0];
            numfree[size]--;
    #ifdef COUNT_ALLOCS
            fast_tuple_allocs++;
    #endif
            /* Inline PyObject_InitVar */
    #ifdef Py_TRACE_REFS
            Py_SIZE(op) = size;
            Py_TYPE(op) = &PyTuple_Type;
    #endif
            _Py_NewReference((PyObject *)op);
        }
     	// 缓冲池不可用
        else
    #endif
        {
            // 通过传入的size参数计算需要的内存总量
            Py_ssize_t nbytes = size * sizeof(PyObject *);
            /* Check for overflow */
            if (nbytes / sizeof(PyObject *) != (size_t)size ||
                (nbytes > PY_SSIZE_T_MAX - sizeof(PyTupleObject) - sizeof(PyObject *)))
            {
                return PyErr_NoMemory();
            }
			// 创建PyTupleObject对象
            op = PyObject_GC_NewVar(PyTupleObject, &PyTuple_Type, size);
            if (op == NULL)
                return NULL;
        }
     	// 初始化每个元素
        for (i=0; i < size; i++)
            op->ob_item[i] = NULL;
    #if PyTuple_MAXSAVESIZE > 0
     	// 第一次分配时将空数组放入缓冲池的第一个位置
        if (size == 0) {
            free_list[0] = op;
            ++numfree[0];
            Py_INCREF(op);          /* extra INCREF so that this is never freed */
        }
    #endif
    #ifdef SHOW_TRACK_COUNT
        count_tracked++;
    #endif
        _PyObject_GC_TRACK(op);
        return (PyObject *) op;
108:}
```

分析 : 

- 我们不难发现 , PyTuple_New与PyList_New有很多相同之处 , 首先这个函数同样接受一个size参数 , 也就是我们在创建时指定PyTupleObject对象的初始元素个数 , 不同的地方在于两种对象在计算需要的内存总量的时机不同
- 随后检查缓冲池是否可用 , 如果可用 , 那么不用多说 ; 如果缓冲池不可用 , 那么现在才计算所需内存总量 , 而在PyList_New中 , 无论缓冲池是否可用都会计算其所需内存总量
- 缓冲池不可用之后 , 接下来就是创建PyTupleObject对象了 , 再然后初始化每个元素
- 最后的一步 , 则是将空元组放入缓冲池的第一位置 , 在整个Python的执行过程中 , 这个操作只会执行一次

而对于缓冲池`free_list` , 如下 : 

`Python-2.7\Objects\tupleobject.c`

```C
 7:#ifndef PyTuple_MAXSAVESIZE
 8:#define PyTuple_MAXSAVESIZE     20  /* Largest tuple to save on free list */
 9:#endif
10:#ifndef PyTuple_MAXFREELIST
11:#define PyTuple_MAXFREELIST  2000  /* Maximum number of tuples of each size to save */
12:#endif
13:
14:#if PyTuple_MAXSAVESIZE > 0
15:/* Entries 1 up to PyTuple_MAXSAVESIZE are free lists, entry 0 is the empty
16:   tuple () of which at most one instance will be allocated.
17:*/
```

通过定义我们可以看到 , PyTupleObject对象缓冲池中维护的最大个数为2000 , 但是注意 , 不是所有的元组都会放入缓冲池 , 不用想也知道 , 这肯定是有一个界限的 , 也就是要小于`PyTuple_MAXSAVESIZE`的 , 从上面我们知道 , 这个值为20 , 也就是说只有`tuple`长度小于20的PyTupleObject才能被放入缓冲池

并且缓冲池的第一个位置是留给`()`的 (有且仅有一个) , 也就是空元组 ; 对于空元组它是在PyTupleObject对象创建时就已经被放入缓冲池了的 , 而其他的PyTupleObject对象什么时候会放入缓冲池中 , 与PyListObject对象也是一样的 , 就是在对象被销毁时 , 这一点同前面的篇章一样 , 放在最后来说

## 设置元素  🍀


## 对象缓冲池  🍀

`Python-2.7\Objects\tupleobject.c`

```C
210:static void
    tupledealloc(register PyTupleObject *op)
    {
        register Py_ssize_t i;
        register Py_ssize_t len =  Py_SIZE(op);
        PyObject_GC_UnTrack(op);
        Py_TRASHCAN_SAFE_BEGIN(op)
        if (len > 0) {
            i = len;
            while (--i >= 0)
                Py_XDECREF(op->ob_item[i]);
    #if PyTuple_MAXSAVESIZE > 0
            if (len < PyTuple_MAXSAVESIZE &&
                numfree[len] < PyTuple_MAXFREELIST &&
                Py_TYPE(op) == &PyTuple_Type)
            {
                op->ob_item[0] = (PyObject *) free_list[len];
                numfree[len]++;
                free_list[len] = op;
                goto done; /* return */
            }
    #endif
        }
        Py_TYPE(op)->tp_free((PyObject *)op);
    done:
        Py_TRASHCAN_SAFE_END(op)
236:}
```





















