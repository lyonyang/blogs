# Python之路 - List对象

**欢迎收藏交流 , 如需转载 , 请注明出处**
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

PyListObject采用的内存管理策略和C++中`vector`采取的内存管理策略是一样的 , 它并不是存了多少东西就申请对应大小的内存 , 因为这样的策略显然是低效的 , 而我们使用列表就是为了用户方便用户频繁地插入或删除元素 , 所以 , 在每一次需要申请内存的时候 , `PyListObject`总会申请一大块内存 , 这时申请的总内存的大小记录在`allocated`中 , 而其实际被使用了的内存的数量记录在了`ob_size`中

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
        // 检查是否会发生溢出
        if ((size_t)size > PY_SIZE_MAX / sizeof(PyObject *))
            return PyErr_NoMemory();
        // 计算需要使用的内存总量
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
- 在创建时 , 首先计算需要使用的内存总量 , 因为`PyList_New`指定的仅仅是元素的个数 , 而不是元素实际将占用的内存空间 , 在这里 , Python会检查指定的元素个数是否会大到使所需内存数量产生溢出的程度 , 并根据判断结果做出相应的操作
- 检查缓冲池是否可用
- 为维护对象申请内存空间 , 维护对象与PyListOjbect对象本身通过`ob_item`建立了连接


当Python创建了新的`PyListObject`对象之后 , 会立即根据调用`PyList_New`时传递的size参数创建`PyListObject`对象所维护的元素列表 , 其中每一个元素都被初始化为`NULL` 

在完成了`PyListObject`对象及维护的列表的创建之后 , Python会调整该`PyListObject`对象 , 用于维护元素列表中元素数量的`ob_size`和`allocated`两个变量

对于缓冲池`free_list`中的对象个数 , 我们可以在源码中找到 , `free_list`最多会维护80个`PyListObject`对象

`Python-2.7\Objects\listobject.c` 

```C
94:#ifndef PyList_MAXFREELIST
95:#define PyList_MAXFREELIST 80
96:#endif
97:static PyListObject *free_list[PyList_MAXFREELIST];
98:static int numfree = 0;
```

`Python-3.5.4\Objects\listobject.c` 

```C
95:#ifndef PyList_MAXFREELIST
96:#define PyList_MAXFREELIST 80
97:#endif
98:static PyListObject *free_list[PyList_MAXFREELIST];
99:static int numfree = 0;
```



## 设置元素  🍀

在我们创建第一个`PyListObject`对象时 , 这时候缓冲池是不可用的 , 于是会调用`PyObject_GC_New`在系统堆上创建一个新的`PyListObject`对象 , 假如我们创建一个包含6个元素的`PyListObject` , 那么创建成功之后 , 这个对象的`ob_size`为6 , `allocated`为6 , 而`ob_item`则是指向这些元素的指针

 而当我们设置元素时 , 如现有一个列表`la = [1, 2, 3]`  , 当我们执行`la[0] = 4`时 , 在Python内部 , 会调用`PyList_SetItem`来完成这个动作 ; 首先Python会进行类型检查 , 随后会进行索引的有效性检查 , 当这两者都通过后 , 将新设置的元素指针放到指定的位置 , 然后调整引用计数 , 将这个位置原来存放的对象的引用计数减1 , 源码如下 : 

`Python-2.7\Objects\listobject.c` 

```C
198:int
    PyList_SetItem(register PyObject *op, register Py_ssize_t i,
                   register PyObject *newitem)
    {
        register PyObject *olditem;
        register PyObject **p;
        if (!PyList_Check(op)) {
            Py_XDECREF(newitem);
            PyErr_BadInternalCall();
            return -1;
        }
        if (i < 0 || i >= Py_SIZE(op)) {
            Py_XDECREF(newitem);
            PyErr_SetString(PyExc_IndexError,
                            "list assignment index out of range");
            return -1;
        }
        p = ((PyListObject *)op) -> ob_item + i;
        olditem = *p;
        *p = newitem;
        Py_XDECREF(olditem);
        return 0;
220:}
```

`Python-3.5.4\Objects\listobject.c` 

```C
215:int
    PyList_SetItem(PyObject *op, Py_ssize_t i,
                   PyObject *newitem)
    {
        PyObject *olditem;
        PyObject **p;
        if (!PyList_Check(op)) {
            Py_XDECREF(newitem);
            PyErr_BadInternalCall();
            return -1;
        }
        if (i < 0 || i >= Py_SIZE(op)) {
            Py_XDECREF(newitem);
            PyErr_SetString(PyExc_IndexError,
                            "list assignment index out of range");
            return -1;
        }
        p = ((PyListObject *)op) -> ob_item + i;
        olditem = *p;
        *p = newitem;
        Py_XDECREF(olditem);
        return 0;
237:}
```

在两个版本中 , 没有变化



## 插入元素  🍀

设置元素和插入元素的动作是不同的 , 设置元素不会导致`ob_item`指向的内存发生变化 , 但是插入元素的动作则有可能使得`ob_item`指向的内存发生变化

Python内部通过调用`PyList_Insert`来完成元素的插入动作 , 而`PyList_Insert`实际上是调用了内部的`insl` , 如下 : 

`Python-2.7\Objects\listobject.c` 

```C
222:static int
    ins1(PyListObject *self, Py_ssize_t where, PyObject *v)
    {
        Py_ssize_t i, n = Py_SIZE(self);
        PyObject **items;
        if (v == NULL) {
            PyErr_BadInternalCall();
            return -1;
        }
        if (n == PY_SSIZE_T_MAX) {
            PyErr_SetString(PyExc_OverflowError,
                "cannot add more objects to list");
            return -1;
        }
		// 调整列表容量
        if (list_resize(self, n+1) == -1)
            return -1;
		// 确定插入点
        if (where < 0) {
            where += n;
            if (where < 0)
                where = 0;
        }
        if (where > n)
            where = n;
    	// 插入元素
        items = self->ob_item;
        for (i = n; --i >= where; )
            items[i+1] = items[i];
        Py_INCREF(v);
        items[where] = v;
        return 0;
    }

255:int
256:PyList_Insert(PyObject *op, Py_ssize_t where, PyObject *newitem)
    {
    	// 类型检查
        if (!PyList_Check(op)) {
            PyErr_BadInternalCall();
            return -1;
        }
        return ins1((PyListObject *)op, where, newitem);
263:}
```

`Python-3.5.4\Objects\listobject.c` 

```C
239:static int
    ins1(PyListObject *self, Py_ssize_t where, PyObject *v)
    {
        Py_ssize_t i, n = Py_SIZE(self);
        PyObject **items;
        if (v == NULL) {
            PyErr_BadInternalCall();
            return -1;
        }
        if (n == PY_SSIZE_T_MAX) {
            PyErr_SetString(PyExc_OverflowError,
                "cannot add more objects to list");
            return -1;
        }
		// 调整列表容量
        if (list_resize(self, n+1) == -1)
            return -1;
		// 确定插入点
        if (where < 0) {
            where += n;
            if (where < 0)
                where = 0;
        }
        if (where > n)
            where = n;
   		// 插入元素
        items = self->ob_item;
        for (i = n; --i >= where; )
            items[i+1] = items[i];
        Py_INCREF(v);
        items[where] = v;
        return 0;
    }

272:int
273:PyList_Insert(PyObject *op, Py_ssize_t where, PyObject *newitem)
    {
    	// 类型检查
        if (!PyList_Check(op)) {
            PyErr_BadInternalCall();
            return -1;
        }
        return ins1((PyListObject *)op, where, newitem);
280:}
```

在`insl`中 , 为了完成元素的插入工作 , 首先必须保证`PyListObject`对象有足够的内存来容纳我们期望插入的元素 , 这一步是通过`insl`中的`list_resize`函数来实现的 , 正是这个函数改变了`PyListObject`所维护的`PyObject *` 列表的大小

`Python-2.7\Objects\listobject.c` 

```c
24:static int
   list_resize(PyListObject *self, Py_ssize_t newsize)
   {
       PyObject **items;
       size_t new_allocated;
       Py_ssize_t allocated = self->allocated;

       /* Bypass realloc() when a previous overallocation is large enough
          to accommodate the newsize.  If the newsize falls lower than half
          the allocated size, then proceed with the realloc() to shrink the list.
       */
       // 不需要重新申请内存
       if (allocated >= newsize && newsize >= (allocated >> 1)) {
           assert(self->ob_item != NULL || newsize == 0);
           Py_SIZE(self) = newsize;
           return 0;
       }

       /* This over-allocates proportional to the list size, making room
        * for additional growth.  The over-allocation is mild, but is
        * enough to give linear-time amortized behavior over a long
        * sequence of appends() in the presence of a poorly-performing
        * system realloc().
        * The growth pattern is:  0, 4, 8, 16, 25, 35, 46, 58, 72, 88, ...
        */
       // 计算重新申请的内存大小
       new_allocated = (newsize >> 3) + (newsize < 9 ? 3 : 6);

       /* check for integer overflow */
       if (new_allocated > PY_SIZE_MAX - newsize) {
           PyErr_NoMemory();
           return -1;
       } else {
           new_allocated += newsize;
       }

       if (newsize == 0)
           new_allocated = 0;
       // 扩展列表
       items = self->ob_item;
       if (new_allocated <= ((~(size_t)0) / sizeof(PyObject *)))
           // 最终调用C中的realloc
           PyMem_RESIZE(items, PyObject *, new_allocated);
       else
           items = NULL;
       if (items == NULL) {
           PyErr_NoMemory();
           return -1;
       }
       self->ob_item = items;
       Py_SIZE(self) = newsize;
       self->allocated = new_allocated;
       return 0;
73:}
```

同样的 , 在`Python-3.5.4\Objects\listobject.c` 中的第25至74行为该函数的定义

在调整`PyListObject`对象所维护的列表的内存时 , Python分两种情况处理 : 

- `newsize < allocated && newsize > allocated/2` , 也就是说当插入后使用的实际内存大小要小于总内存大小 , 以及要大于总内存大小的一半时 , 就简单调整`ob_size`值 
- 其他情况 , 调用`realloc` , 重新分配空间

我们可以发现 , 对于第二种情况 , 比如`newsize < allocated/2` 时 , Python也会调用`realloc`来收缩列表的内存空间 , 不得不说这是物尽其用的设计



## 删除元素  🍀

以`list`对象方法`remove`为例 , 当我们使用`remove`方法时 , `PyListObject`中的`listremove`操作就会被激活

`Python-2.7\Objects\listobject.c` 

```C
2336:static PyObject *
     listremove(PyListObject *self, PyObject *v)
     {
         Py_ssize_t i; 

         for (i = 0; i < Py_SIZE(self); i++) {
             int cmp = PyObject_RichCompareBool(self->ob_item[i], v, Py_EQ);
             if (cmp > 0) {
                 if (list_ass_slice(self, i, i+1,
                                    (PyObject *)NULL) == 0)
                     Py_RETURN_NONE;
                 return NULL;
             }
             else if (cmp < 0)
                 return NULL;
         }
         PyErr_SetString(PyExc_ValueError, "list.remove(x): x not in list");
         return NULL;
2354:}
```

`Python-3.5.4\Objects\listobject.c` 第2197至2215见同上代码清单

首先Python会对整个列表进行遍历 , 在遍历`PyListObject`中所有元素的过程中 , 将待删除元素与`PyListObject`中的每个元素一一进行比较 , 比较操作是通过`PyObject_RichCompareBool`完成的 , 如果返回值大于0 , 则表示要删除的元素与列表中的元素匹配成功 , Python将立即调用`list_ass_slice`删除该元素

`Python-2.7\Objects\listobject.c` 

```C
607:/* a[ilow:ihigh] = v if v != NULL.	 // 不为空就替换
     * del a[ilow:ihigh] if v == NULL.   // 为空就删除
     *
     * Special speed gimmick:  when v is NULL and ihigh - ilow <= 8, it's
     * guaranteed the call cannot fail.
     */
    static int
    list_ass_slice(PyListObject *a, Py_ssize_t ilow, Py_ssize_t ihigh, PyObject *v)
    {
        ......
709:}
```

`Python-3.5.4\Objects\listobject.c` 第572至579见同上代码清单

如上 , 对于`list_ass_slice`其实是有两种语义的 , 即`replace`和`remove` ; 于是 , 在Python列表中删除元素我们还可以这样做 : 

```python
# Python 2.x & 3.x
>>> la = [1,2,3,4,5]
>>> la[1:3] = []
>>> la
[1, 4, 5]
```

对于`list`对象的`pop`方法 , 同样也是调用`list_ass_slice`来进行删除 , 源码位于`listobject.c`文件中


## 对象缓冲池  🍀

在`PyList_New`中我们见过一个`free_list` , 这就是`PyListObject`对象缓冲池 ; 但是我们在`PyList_New`中并没有看到缓冲池中的`PyListObject`对象的添加过程 , 这是因为缓冲池对象并不像前面的字符串对象或者整数对象一样 , 是在创建时添加的 , Python列表的缓冲池是在其销毁的时候添加的

`Python-2.7\Objects\listobject.c` 

```C
296:static void
    list_dealloc(PyListObject *op)
    {
        Py_ssize_t i;
        PyObject_GC_UnTrack(op);
        Py_TRASHCAN_SAFE_BEGIN(op)
        // 销毁PyListObject对象维护的元素列表
        if (op->ob_item != NULL) {
            /* Do it backwards, for Christian Tismer.
               There's a simple test case where somehow this reduces
               thrashing when a *very* large list is created and
               immediately deleted. */
            i = Py_SIZE(op);
            while (--i >= 0) {
                Py_XDECREF(op->ob_item[i]);
            }
            PyMem_FREE(op->ob_item);
        }
    	// 释放PyListObject自身
        if (numfree < PyList_MAXFREELIST && PyList_CheckExact(op))
            free_list[numfree++] = op;
        else
            Py_TYPE(op)->tp_free((PyObject *)op);
        Py_TRASHCAN_SAFE_END(op)
318:}
```

与`PyListObject`对象创建一样 , `PyListObject`对象的销毁也是分离的 , 首先销毁`PyListObject`对象所维护的元素列表 , 然后再释放`PyListObject`对象本身 ; 这样的工作无非是改变该对象的引用计数 , 然后再释放内存 , 但是我们发现 , 在释放`PyListObject`本身时 , Python会检查前面提到的这个缓冲池`free_list`

首先Python会查看其中缓存的`PyListObject`对象的数量是否已经满了 , 如果没有 , 就将该待删除的`PyListObject`对象放到缓冲池中 , 以备后用

注意 , 我们也已经发现了 , 添加进缓冲池的是`PyListObject`对象本身 , 而不包括它之前维护的元素列表 , 也就是说我们在创建新的`PyListObject`时 , Python会首先唤醒这些已经 "死去" 的`PyListObject` , 然后赋予它们新的元素列表 , 使其能够重新做 "人"

对于每次创建`PyListObject`对象时必须创建元素列表 , 这是Python为了避免过多的消耗系统内存 , 采取的时间换空间的做法

