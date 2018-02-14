# Python之路 - List对象  🍀
<!-- TOC -->

- [Python之路 - List对象  🍀](#python之路---list对象--🍀)
    - [介绍  🍀](#介绍--🍀)
    - [PyListObject  🍀](#pylistobject--🍀)
    - [创建与维护  🍀](#创建与维护--🍀)

<!-- /TOC -->
## 介绍  🍀

元素的一个群是一个非常重要的抽象概念 , 我们可以将符合某一特性的一堆元素聚集为一个群

群的概念对于编程语言十分重要 , C语言就内建了数组的概念 , 每一种实现都为某种目的的元素聚集或元素访问提供极大的方便

`PyListObject`是Python提供的对列表的抽象 , 它可以支持对元素的插入 , 删除 , 添加等操作 , 所以它是一个可变对象

## PyListObject  🍀

`Python-2.7\Include\listobject.h` 

```C
22:typedef struct {
23:    PyObject_VAR_HEAD
24:    /* Vector of pointers to list elements.  list[0] is ob_item[0], etc. */
25:    PyObject **ob_item;
26:
27:    /* ob_item contains space for 'allocated' elements.  The number
28:     * currently in use is ob_size.
29:     * Invariants:
30:     *     0 <= ob_size <= allocated
31:     *     len(list) == ob_size
32:     *     ob_item == NULL implies ob_size == allocated == 0
33:     * list.sort() temporarily sets allocated to -1 to detect mutations.
34:     *
35:     * Items must normally not be NULL, except during construction when
36:     * the list is not yet visible outside the function that builds it.
37:     */
38:    Py_ssize_t allocated;
39:} PyListObject;
```

分析 : 

- PyObject_VAR_HEAD , Python中的列表是一个变长对象
- PyObject **ob_item , `ob_item`为指向元素列表的指针 , 实际上 , Python中的`list[0]` 就是`ob_item[0]`
- Py_ssize_t allocated , 与`PyListObject`对象的内存管理有关

实际上 , 在`PyObject_VAR_HEAD`中的`ob_size`和`allocated` 都和`PyListObject`对象的内存管理有关 : 

PyListObject采用的内存管理策略和C++中`vector`采取的内存管理策略是一样的 , 它并不是存了多少东西就申请对应大小的内存 , 因为这样的策略显然是低效的 , 而我们使用列表就是为了用户方便用户频繁地插入或删除元素 , 所以 , 在每一次需要申请内存的时候 , `PyListObject`总会申请一大块内存 , 这时申请的总内存的大小记录在`allocated`中 , 而其实实际被使用了的内存的数量记录在了`ob_size`中

假如有一个能容纳10个元素的列表已经装入了5个元素 , 那么这个列表的`ob_size`就是5 , 而`allcoated`则是10

即 : `0 <= ob_size <= allocated`

在`Python-3.5.4\Include\listobject.h`的22至40行 , 我们可以找到相同的代码 , 也就是说2.7与3.5.4的这一部分是没有区别的 

## 创建与维护  🍀

在之前对于Python对象创建方式已有说明 , 为了创建一个列表 , Python只提供了唯一的一条途径 , 就是`PyList_New`

`Python-2.7\Objects\listobject.c` 

```C
112:PyObject *
    PyList_New(Py_ssize_t size)
    {
        PyListObject *op;
        size_t nbytes;
    #ifdef SHOW_ALLOC_COUNT
        static int initialized = 0;
        if (!initialized) {
            Py_AtExit(show_alloc);
            initialized = 1;
        }
    #endif

        if (size < 0) {
            PyErr_BadInternalCall();
            return NULL;
        }
        /* Check for overflow without an actual overflow,
         *  which can cause compiler to optimise out */
        if ((size_t)size > PY_SIZE_MAX / sizeof(PyObject *))
            return PyErr_NoMemory();
        nbytes = size * sizeof(PyObject *);
        if (numfree) {
            
            // 缓冲池可用
            numfree--;
            op = free_list[numfree];
            _Py_NewReference((PyObject *)op);
    #ifdef SHOW_ALLOC_COUNT
            count_reuse++;
    #endif
        } else {
            
            // 缓冲池不可用
            op = PyObject_GC_New(PyListObject, &PyList_Type);
            if (op == NULL)
                return NULL;
    #ifdef SHOW_ALLOC_COUNT
            count_alloc++;
    #endif
        }
    
    	// 为对象中维护的元素列表申请空间
        if (size <= 0)
            op->ob_item = NULL;
        else {
            op->ob_item = (PyObject **) PyMem_MALLOC(nbytes);
            if (op->ob_item == NULL) {
                Py_DECREF(op);
                return PyErr_NoMemory();
            }
            memset(op->ob_item, 0, nbytes);
        }
        Py_SIZE(op) = size;
        op->allocated = size;
        _PyObject_GC_TRACK(op);
        return (PyObject *) op;
163:}
```

分析 : 

- 这个函数接受一个size参数 , 也就是我们可以在创建时指定`PyListObject`对象的初始元素个数
- ​
