# Python之路 - Dict对象
<!-- TOC -->

- [Python之路 - Dict对象](#python之路---dict对象)
    - [介绍  🍀](#介绍--🍀)
    - [散列表  🍀](#散列表--🍀)
    - [PyDictObject  🍀](#pydictobject--🍀)
    - [创建与维护  🍀](#创建与维护--🍀)
    - [元素搜索  🍀](#元素搜索--🍀)

<!-- /TOC -->
## 介绍  🍀

为了刻画某种元素之间的对应关系 , 现代编程语言通常都在语言级或标准库中提供某种关联式的容器 ; 关联容器的设计总会极大地关注键的搜索效率 , 因为我们希望根据我们手中已有的某个元素来快速获得与之有某种联系的另一元素

在Python中同样提供关联式容器 , 即PyDictObject 对象 , 与`map`不同的是 , PyDictObject对搜索的效率要求极其苛刻 , 这也是因为PyDictObject对象在Python本身的实现中被大量采用 ; 比如Python会通过PyDictObject来建立执行Python字节码的运行环境 , 其中会存放变量名和变量值的元素对 , 通过查找变量名获得变量值 , 因此PyDictObject采用的是散列表 (hash table) , 因为理论上 , 在最优情况下 , 散列表能提供`O(1)`复杂度的搜索效率

## 散列表  🍀

散列表的基本思想 , 是通过一定的函数将需搜索的键值映射为一个整数 , 将这个整数视为索引值去访问某片连续的区域

对散列表这种数据结构的采用是以加速键的搜索过程为终极目标的 , 所以 , 将元素映射为整数的过程对于Python中`dict`的实现就显得尤为关键 ; 用于映射的函数称为散列函数 (hash function) , 映射后的值称为元素的散列值 (hash value) , 在散列表的实现中 , 所选择的散列函数的优劣直接决定所实现的散列表的搜索效率的高低

在使用散列表的过程中 , 不同的对象经过散列函数的作用 , 可能被映射为相同的散列值 , 这就是散列冲突

根据研究表明 , 当散列表的装载率大于2/3时 , 散列冲突发生的概率就会大大增加

解决散列冲突的方法有很多种 , 在Python中采用的是开放定址法

当产生散列冲突时 , Python会通过一个二次探测函数`f` , 计算下一个候选位置`addr` , 如果位置`addr`可用 , 则可将待插入元素放到位置`addr` ; 如果位置`addr`不可用 , 则Python会再次使用探测函数`f` , 获得下一个候选位置 , 以此依次寻找下去

最后 , 这些位置会形成一个`"冲突探测链"(或简称探测序列)` , 而当我们要删除某条探测链上的某个元素时 , 按照探测链会发生什么样的情况 ; 假如这条链的首元素位置为`a` , 尾元素的位置为`c` , 现在需要删除中间的某个位置`b`上的元素 , 如果直接将位置`b`上的元素删除 , 则会导致探测链的断裂 , 于是探测函数在探测时将再也不能到达位置`c`了 , 所以删除某条探测链上的元素时不能进行真正的删除 , 而是进行一种 "伪删除" 操作 , 必须要让该元素还存在于探测链上

在Python中 , 这种伪删除是在PyDictObject对象中实现的

## PyDictObject  🍀

在Python2.7中 , 关联容器的一个(键 , 值)元素对称为一个`entry`或`slot`

`Python-2.7\Include\dictobject.h`

```C
50:typedef struct {
       /* Cached hash code of me_key.  Note that hash codes are C longs.
        * We have to use Py_ssize_t instead because dict_popitem() abuses
        * me_hash to hold a search finger.
        */
       Py_ssize_t me_hash;
       PyObject *me_key;
       PyObject *me_value;
58:} PyDictEntry;
```

在PyDictEntry中 , `me_hash`域存储的是`me_key`的散列值 , 利用一个域来记录这个散列值可以避免每次查询的时候都要重新计算一遍散列值

在Python中 , 在一个PyDictObject对象生存变化的过程中 , 其中的entry会在不同的状态间转换 ; PyDictObject中entry可以在3种状态之间转换 : Unused , Active , Dummy

- Unused : 当一个entry的`me_key`和`me_value`都为NULL时 , entry处于Unused态 ; 表明目前该entry中并没有存储(key , value)对 , 而且在此之前 , 也没有存储过它们 , 这时每一个entry在初始化时的状态 , 并且也只有在Unused态下 , entry的`me_key`域才会为NULL
- Active : 当entry中存储了一个(key , value)对时 , entry便转到了Active态 , 在Active态下 , `me_key`和`me_value`都不能为NULL 
- Dummy : 当entry中存储的(key , value)对被删除后 , entry的状态不能直接从Active态转为Unused态 , 因为这样会导致冲突探测链的中断 , 所以entry中的`me_key`将指向dummy对象 , 从而entry进入Dummy态 , 这就是"伪删除"技术 ; 当Python沿着某条冲突链搜索时 , 如果发现一个entry处于Dummy态 , 说明目前该entry虽然是无效的 , 但是其后的entry可能是有效的 , 是应该被搜索的 , 这样就保证了冲突探测链的连续性


在Python中 , 关联容器是通过PyDictObject对象来实现的 ,  而一个PyDictObject

对象实际上是一大堆entry的集合 : 

`Python-2.7\Include\dictobject.h`

```C
70:typedef struct _dictobject PyDictObject;
   struct _dictobject {
       PyObject_HEAD
       Py_ssize_t ma_fill;  /* # Active + # Dummy */
       Py_ssize_t ma_used;  /* # Active */

       /* The table contains ma_mask + 1 slots, and that's a power of 2.
        * We store the mask instead of the size because the mask is more
        * frequently needed.
        */
       Py_ssize_t ma_mask;

       /* ma_table points to ma_smalltable for small tables, else to
        * additional malloc'ed memory.  ma_table is never NULL!  This rule
        * saves repeated runtime null-tests in the workhorse getitem and
        * setitem calls.
        */
       PyDictEntry *ma_table;
       PyDictEntry *(*ma_lookup)(PyDictObject *mp, PyObject *key, long hash);
       PyDictEntry ma_smalltable[PyDict_MINSIZE];
90:};
```

定义说明 : 

- ma_fill , `ma_fill`域中维护着从PyDictObject对象创建开始直到现在 , 曾经及正处于Active态的entry个数 , 而`ma_used`则维护着当前正处于Active态的entry的数量
- 在定义的最后 , 有一个名为`ma_smalltable`的PyDictEntry数组 , 这个数组意味着当创建一个PyDictObject对象时 , 至少有`PyDict_MINSIZE`个entry被同时创建 , 在`dictobject.h`中 , 这个值被设定为8 , 这个值被认为时通过大量的实验得出的最佳值 ; 它既不会态浪费内存空间 , 又能很好地满足Python内部大量使用PyDictObject的环境的需求
- ma_table , ma_table域是关联对象的关键所在 , 它将指向一片作为PyDictEntry集合的内存的开始位置 , 当一个PyDictObject对象是一个比较小的dict时 (entry数量少于8) , ma_table域将指向`ma_smalltable` , 而当PyDictObject中的entry数量超过8个时 , 将会申请额外的内存空间 , 并将ma_table指向这块空间 , 这样 , 无论何时 , ma_table域都不会为NULL , 那么在程序运行时就不需要一次又一次的检查`ma_table`的有效性了 , 因为`ma_table`总是有效的 , 这两种`ma_table`见下图
- ma_mask , PyDictObject中的`ma_mask`记录了一个PyDictObject对象中所拥有的entry数量

![ma_table](http://oux34p43l.bkt.clouddn.com/ma_table.png?imageMogr2/blur/1x0/quality/75|watermark/2/text/bHlvbi55YW5nQHFxLmNvbQ==/font/YXBhcmFqaXRh/fontsize/560/fill/Izk0ODI4Mg==/dissolve/100/gravity/SouthEast/dx/10/dy/10)

## 创建与维护  🍀

Python内部通过PyDict_New来创建一个新的dict对象

`Python-2.7\Include\dictobject.c`

```C
210:#define INIT_NONZERO_DICT_SLOTS(mp) do {                                \
        (mp)->ma_table = (mp)->ma_smalltable;                               \
    	// PyDict_MINSIZE定义在dictobject.h中,默认值为8
        (mp)->ma_mask = PyDict_MINSIZE - 1;                                 \
        } while(0)                                                          \
																		   
    #define EMPTY_TO_MINSIZE(mp) do {                                       \
        memset((mp)->ma_smalltable, 0, sizeof((mp)->ma_smalltable));        \
        (mp)->ma_used = (mp)->ma_fill = 0;                                  \
        INIT_NONZERO_DICT_SLOTS(mp);                                        \
219:} while(0)

220:/* Dictionary reuse scheme to save calls to malloc, free, and memset */
    #ifndef PyDict_MAXFREELIST
    #define PyDict_MAXFREELIST 80
    #endif
    static PyDictObject *free_list[PyDict_MAXFREELIST];
226:static int numfree = 0;
......
240:PyObject *
    PyDict_New(void)
    {
        register PyDictObject *mp;
    	// 自动创建dummy对象
        if (dummy == NULL) { /* Auto-initialize dummy */
            dummy = PyString_FromString("<dummy key>");
            if (dummy == NULL)
                return NULL;
    #ifdef SHOW_CONVERSION_COUNTS
            Py_AtExit(show_counts);
    #endif
    #ifdef SHOW_ALLOC_COUNT
            Py_AtExit(show_alloc);
    #endif
    #ifdef SHOW_TRACK_COUNT
            Py_AtExit(show_track);
    #endif
        }
        if (numfree) {
            // 使用缓冲池
            mp = free_list[--numfree];
            assert (mp != NULL);
            assert (Py_TYPE(mp) == &PyDict_Type);
            _Py_NewReference((PyObject *)mp);
            if (mp->ma_fill) {
                EMPTY_TO_MINSIZE(mp);
            } else {
                /* At least set ma_table and ma_mask; these are wrong
                   if an empty but presized dict is added to freelist */
                INIT_NONZERO_DICT_SLOTS(mp);
            }
            assert (mp->ma_used == 0);
            assert (mp->ma_table == mp->ma_smalltable);
            assert (mp->ma_mask == PyDict_MINSIZE - 1);
    #ifdef SHOW_ALLOC_COUNT
            count_reuse++;
    #endif
        } else {
            // 创建PyDictObject对象
            mp = PyObject_GC_New(PyDictObject, &PyDict_Type);
            if (mp == NULL)
                return NULL;
            EMPTY_TO_MINSIZE(mp);
    #ifdef SHOW_ALLOC_COUNT
            count_alloc++;
    #endif
        }
        mp->ma_lookup = lookdict_string;
    #ifdef SHOW_TRACK_COUNT
        count_untracked++;
    #endif
    #ifdef SHOW_CONVERSION_COUNTS
        ++created;
    #endif
        return (PyObject *)mp;
293:}
```

在定义的开始部分我们可以发现 , 自动创建`dummy`对象 , 这个`dummy`对象竟然时一个PyStringObject对象 , 实际上 , 它仅仅时用来作为一种指示标志 , 表明该entry曾被使用过 , 且探测序列下一个位置的entry有可能时有效的 , 从而防止探测序列中断

如果不使用缓冲池 , 创建时将调用`EMPTY_TO_MINSIZE`  , 将`ma_smalltable`清零 , 同时设置`ma_size`和`ma_fill` , 初始时 , 这两个变量都为0 , 随后调用`INIT_NONZERO_DICT_SLOTS` , 其功能是将`ma_table`指向`ma_smalltable` , 并设置`ma_mask`为7

在创建过程的最后 , 将`lookdict_string`赋给了`ma_lookup` , 这个`ma_lookup`指定了PyDictObjec在entry集合中搜索某一特定entry时需要进行的动作 , 在`ma_lookup`中 , 包含了散列函数和发生冲突时二次探测函数的具体实现 , 它时PyDictObject的搜索策略

PyDictObject缓冲池见下文

## 元素搜索  🍀

Python为PyDictObject对象提供了两种搜索策略 , lookdict和lookdict_string , 但是实际上 , 这两种策略使用的相同的算法 , lookdict_string只是对lookdict的一种针对PyStringObject对象的特殊形式 , 这是因为以PyStringObject对象作为PyDictObject对象中entry的键在Python中应用非常广泛 

`Python-2.7\Include\dictobject.h`

```C
319:static PyDictEntry *
    lookdict(PyDictObject *mp, PyObject *key, register long hash)
    {
        register size_t i;
        register size_t perturb;
        register PyDictEntry *freeslot;
        register size_t mask = (size_t)mp->ma_mask;
        PyDictEntry *ep0 = mp->ma_table;
        register PyDictEntry *ep;
        register int cmp;
        PyObject *startkey;
		// 散列,定位冲突探测链的第一个entry
331:    i = (size_t)hash & mask;
        ep = &ep0[i];
    	// entry处于Unused态
        if (ep->me_key == NULL || ep->me_key == key)
            return ep;
		// entry处于Dummy态
        if (ep->me_key == dummy)
337:        freeslot = ep;
        else {
            // 检查Active态entry
            if (ep->me_hash == hash) {
                startkey = ep->me_key;
                Py_INCREF(startkey);
                cmp = PyObject_RichCompareBool(startkey, key, Py_EQ);
                Py_DECREF(startkey);
                if (cmp < 0)
                    return NULL;
                if (ep0 == mp->ma_table && ep->me_key == startkey) {
                    if (cmp > 0)
                        return ep;
                }
                else {
                    /* The compare did major nasty stuff to the
                     * dict:  start over.
                     * XXX A clever adversary could prevent this
                     * XXX from terminating.
                     */
                    return lookdict(mp, key, hash);
                }
            }
            freeslot = NULL;
        }

        /* In the loop, me_key == dummy is by far (factor of 100s) the
           least likely outcome, so test for that last. */
    
    	// 寻找探测链上的下一个entry
        for (perturb = hash; ; perturb >>= PERTURB_SHIFT) {
            i = (i << 2) + i + perturb + 1;
            ep = &ep0[i & mask];
            // Unused态entry,搜索失败
            if (ep->me_key == NULL)
                return freeslot == NULL ? ep : freeslot;
            // 检查引用是否相同
            if (ep->me_key == key)
                return ep;
            // 检查值是否相同
            if (ep->me_hash == hash && ep->me_key != dummy) {
                startkey = ep->me_key;
                Py_INCREF(startkey);
                cmp = PyObject_RichCompareBool(startkey, key, Py_EQ);
                Py_DECREF(startkey);
                if (cmp < 0)
                    return NULL;
                if (ep0 == mp->ma_table && ep->me_key == startkey) {
                    if (cmp > 0)
                        return ep;
                }
                else {
                    /* The compare did major nasty stuff to the
                     * dict:  start over.
                     * XXX A clever adversary could prevent this
                     * XXX from terminating.
                     */
                    return lookdict(mp, key, hash);
                }
            }
            // 设置freeslot
            else if (ep->me_key == dummy && freeslot == NULL)
                freeslot = ep;
        }
        assert(0);          /* NOT REACHED */
        return 0;
396:}
```

PyDictObject中维护的entry的数量是有限的 , 而传入lookdict中的key的hash值却不一定在限定范围内 , 所以这就要求lookdict将hash值映射到某个entry上去 , lookdict采取的策略是 , 直接将hash值与entry的数量做一个`&`操作(见331行) , 该操作的结果就是entry的数量 , 也就是`ma_mask`

之所以命名为mask而不是size , 是因为`ma_mask`会被用来进行大量的`&`操作 , 所以entry数量相关的变量被命名为`ma_mask`

 `freeslot`指向一个指示失败且立即可用的entry : 

在搜索过程中 , 如果探测链中的某个位置上 , entry处于Dummy态 , 那么如果在这个序列中搜索不成功 , 就会返回这个处于Dummy态的entry , 这个`freeslot`正是用来指向探测序列中第一个处于Dummy态的entry (`me_value`为NULL); 如果探测序列并没有Dummy态entry , 搜索失败时 , `freeslot`则指向一个处于Unused态的entry , 同样是一个能指示失败且立即可用的entry

在元素搜索时 , 会先进行亮哥key的值检查 , 首先检查两个对象的hash值是否相同 , 如果不相同 , 就直接中断 ; 而如果相同 , 那么Python将通过PyObject_RichCompareBool进行比较 , 其原型如下 : 

```C
int PyObject_RichCompareBool(PyObject *v, PyObject *w, int op)
```

当`v op w`成立时 , 返回1 ; 不成立时 , 返回0 ; 如果在比较中发生了错误返回-1

在lookdict代码清单中 , 指定的Py_EQ , 表示进行相等比较操作





