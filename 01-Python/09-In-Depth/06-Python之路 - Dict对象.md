# Python之路 - Dict对象
<!-- TOC -->

- [Python之路 - Dict对象](#python之路---dict对象)
    - [介绍  🍀](#介绍--🍀)
    - [散列表  🍀](#散列表--🍀)
    - [PyDictObject  🍀](#pydictobject--🍀)

<!-- /TOC -->
## 介绍  🍀

为了刻画某种元素之间的对应关系 , 现代编程语言通常都在语言级或标准库中提供某种关联式的容器 ; 关联容器的设计总会极大地关注键的搜索效率 , 因为我们希望根据我们手中已有的某个元素来快速获得与之有某种联系的另一元素

在Python中同样提供关联式容器 , 即`PyDictObject` 对象 , 与`map`不同的是 , `PyDictObject`对搜索的效率要求极其苛刻 , 这也是因为`PyDictObject`对象在Python本身的实现中被大量采用 ; 比如Python会通过`PyDictObject`来建立执行Python字节码的运行环境 , 其中会存放变量名和变量值的元素对 , 通过查找变量名获得变量值 , 因此`PyDictObject`采用的是散列表 (hash table) , 因为理论上 , 在最优情况下 , 散列表能提供`O(1)`复杂度的搜索效率

## 散列表  🍀

散列表的基本思想 , 是通过一定的函数将需搜索的键值映射为一个整数 , 将这个整数视为索引值去访问某片连续的区域

对散列表这种数据结构的采用是以加速键的搜索过程为终极目标的 , 所以 , 将元素映射为整数的过程对于Python中`dict`的实现就显得尤为关键 ; 用于映射的函数称为散列函数 (hash function) , 映射后的值称为元素的散列值 (hash value) , 在散列表的实现中 , 所选择的散列函数的优劣直接决定所实现的散列表的搜索效率的高低

在使用散列表的过程中 , 不同的对象经过散列函数的作用 , 可能被映射为相同的散列值 , 这就是散列冲突

根据研究表明 , 当散列表的装载率大于2/3时 , 散列冲突发生的概率就会大大增加

解决散列冲突的方法有很多种 , 在Python中采用的是开放定址法

当产生散列冲突时 , Python会通过一个二次探测函数`f` , 计算下一个候选位置`addr` , 如果位置`addr`可用 , 则可将待插入元素放到位置`addr` ; 如果位置`addr`不可用 , 则Python会再次使用探测函数`f` , 获得下一个候选位置 , 以此依次寻找下去

最后 , 这些位置会形成一个`"冲突探测链"(或简称探测序列)` , 而当我们要删除某条探测链上的某个元素时 , 按照探测链会发生什么样的情况 ; 假如这条链的首元素位置为`a` , 尾元素的位置为`c` , 现在需要删除中间的某个位置`b`上的元素 , 如果直接将位置`b`上的元素删除 , 则会导致探测链的断裂 , 于是探测函数在探测时将再也不能到达位置`c`了 , 所以删除某条探测链上的元素时不能进行真正的删除 , 而是进行一种 "伪删除" 操作 , 必须要让该元素还存在于探测链上

在Python中 , 这种伪删除是在`PyDictObject`对象中实现的

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

在`PyDictEntry`中 , `me_hash`域存储的是`me_key`的散列值 , 利用一个域来记录这个散列值可以避免每次查询的时候都要重新计算一遍散列值

在Python中 , 在一个`PyDictObject`对象生存变化的过程中 , 其中的entry会在不同的状态间转换 ; `PyDictObject`中entry可以在3种状态之间转换 : Unused , Active , Dummy

- Unused : 当一个entry的`me_key`和`me_value`都为NULL时 , entry处于Unused态 ; 表明目前该entry中并没有存储(key , value)对 , 而且在此之前 , 也没有存储过它们 , 这时每一个entry在初始化时的状态 , 并且也只有在Unused态下 , entry的`me_key`域才会为NULL
- Active : 当entry中存储了一个(key , value)对时 , entry便转到了Active态 , 在Active态下 , `me_key`和`me_value`都不能为NULL 
- Dummy : 当entry中存储的(key , value)对被删除后 , entry的状态不能直接从Active态转为Unused态 , 因为这样会导致冲突探测链的中断 , 所以entry中的`me_key`将指向dummy对象 , 从而entry进入Dummy态 , 这就是"伪删除"技术 ; 当Python沿着某条冲突链搜索时 , 如果发现一个entry处于Dummy态 , 说明目前该entry虽然是无效的 , 但是其后的entry可能是有效的 , 是应该被搜索的 , 这样就保证了冲突探测链的连续性

`Python-3.5.4\Include\dictobject.h`



