# Python之路 - 对象的创建

**欢迎收藏交流 , 如需转载 , 请注明出处**
## 介绍  🍀

上一篇关于Python中对象实现中我们知道 , 创建一个对象Python提供了两种API , 即范型API和类型API

而在对象真正创建时 , Python为我们使用的是类型API

因为如果使用范型API , 那么意味着Python要提前为我们准备好`PyObject_New` 这一系列的API , 对于创建内置类型的对象这并没有问题 , 但是如果对于创建用户自定义的类型这样就非常的不明智了 , 因为需要提前创建好诸多的`_New`对象 

## 创建对象  🍀

我们定义一个类 , 通过这个自定义类来说明Python对象的创建流程

```python
# Python对象的基石,即PyObject
class object():
    pass

# 自定义类
class MyObject(object):
    pass
```

**创建object对象**

在分析自定义类型的对象创建之前 , 我们需要分析一下object对象是如何创建的 , 虽然我们在实际中是不会也不需要去创建object对象的 , 但是这有利于我们下一步的分析 : 

![创建object对象](http://oux34p43l.bkt.clouddn.com/创建object对象.png?imageMogr2/blur/1x0/quality/75|watermark/2/text/bHlvbi55YW5nQHFxLmNvbQ==/font/YXBhcmFqaXRh/fontsize/560/fill/Izk0ODI4Mg==/dissolve/100/gravity/SouthEast/dx/10/dy/10)

object对象的创建 : 如上图 , 创建object对象首先调用类型API (PyBaseObject_Type) , 并且会首先调用API中的`tp_new` , 因为这里是创建object , 所以`tp_new`中不会为NULL

**创建自定义对象**

无论是Python 2.x还是3.x , Python中所有的类都是以`object`类为基础的 , 也就是说所有的类都继承了`object`类 , 所以自定义类型对象的创建流程如下 : 

![创建myobject对象](http://oux34p43l.bkt.clouddn.com/创建myobject对象.png?imageMogr2/blur/1x0/quality/75|watermark/2/text/bHlvbi55YW5nQHFxLmNvbQ==/font/YXBhcmFqaXRh/fontsize/560/fill/Izk0ODI4Mg==/dissolve/100/gravity/SouthEast/dx/10/dy/10)

无论是自定义对象的创建还是object对象的创建 , 其创建对象的流程都是一样的 : 

1. 首先都会调用其类型API中的`tp_new`  ,  如果我们自定义类型中`tp_new`为NULL , 那么它将通过`tp_base`指定的基类继续去寻找`tp_new` , 直到找到`tp_new`为止 , 不要担心会找不到 , Python中所有的类都继承了object类 , 而object类中是一定有`tp_new`的
2. 在找到`tp_new`之后会回到原点拿取`tp_basicsize` , 这里面记录了该对象应该占用内存大小的信息 , 拿取后申请内存完成创建 , 返回一个新对象
3. 拿到新对象我们对新对象进行初始化

通过这三大步 , 一个对象的创建基本就完成了

站在Python的角度来看 , `tp_new`对应的就是特殊操作符中的`__new__`方法 , 此方法返回一个对象实例 , `tp_init	` 对应的就是特殊操作符中的`__init__`方法 , 当我们创建一个类时一般都会对`__init__`方法进行重载以达到我们的目标

当然`PyBaseObject_Type`并不是类型对象的终点 , 在其之上还存在着一个`PyType_Type`

更多关于类型对象的信息详见上一篇 , 其中定义了对象的行为


## 类型的类型  🍀

我们知道PyObject中有一个 `ob_type`指针 , 记录着PyObject的类型信息 , 但是这个结构体也是一个对象 , 就是上一篇中所说的类型对象PyTypeObject

既然是对象 , 那么就肯定有类型 ,  而这个类型就是PyType_Type

`Python-2.7\Objects\typeobject.c`

```C
2730:PyTypeObject PyType_Type = {
     PyVarObject_HEAD_INIT(&PyType_Type, 0)
     "type",                                     /* tp_name */
     sizeof(PyHeapTypeObject),                   /* tp_basicsize */
     sizeof(PyMemberDef),                        /* tp_itemsize */
     (destructor)type_dealloc,                   /* tp_dealloc */
     0,                                          /* tp_print */
     0,                                          /* tp_getattr */
     0,                                          /* tp_setattr */
     0,                                  /* tp_compare */
     (reprfunc)type_repr,                        /* tp_repr */
     0,                                          /* tp_as_number */
     0,                                          /* tp_as_sequence */
     0,                                          /* tp_as_mapping */
     (hashfunc)_Py_HashPointer,                  /* tp_hash */
     (ternaryfunc)type_call,                     /* tp_call */
     0,                                          /* tp_str */
     (getattrofunc)type_getattro,                /* tp_getattro */
     (setattrofunc)type_setattro,                /* tp_setattro */
     0,                                          /* tp_as_buffer */
     Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC |
         Py_TPFLAGS_BASETYPE | Py_TPFLAGS_TYPE_SUBCLASS,         /* tp_flags */
     type_doc,                                   /* tp_doc */
     (traverseproc)type_traverse,                /* tp_traverse */
     (inquiry)type_clear,                        /* tp_clear */
     type_richcompare,                                           /* tp_richcompare */
     offsetof(PyTypeObject, tp_weaklist),        /* tp_weaklistoffset */
     0,                                          /* tp_iter */
     0,                                          /* tp_iternext */
     type_methods,                               /* tp_methods */
     type_members,                               /* tp_members */
     type_getsets,                               /* tp_getset */
     0,                                          /* tp_base */
     0,                                          /* tp_dict */
     0,                                          /* tp_descr_get */
     0,                                          /* tp_descr_set */
     offsetof(PyTypeObject, tp_dict),            /* tp_dictoffset */
     type_init,                                  /* tp_init */
     0,                                          /* tp_alloc */
     type_new,                                   /* tp_new */
     PyObject_GC_Del,                            /* tp_free */
     (inquiry)type_is_gc,                        /* tp_is_gc */
2772:};
```

在Python 3.5.4中内容是一样就不列出了 , 行数3328-3369

所有的对象中的类型对象都是由PyType_Type对象进行创建的 , 包括PyObject , 如下 : 

```python
>>> object.__class__
<class 'type'>
>>> int.__class__
<class 'type'>
>>> class A(object):
...     pass
...
>>> A.__class__
<class 'type'>
>>> type.__class__
<class 'type'>
>>>
```

通过这一实验 , 我们可以知道其实所有类的祖宗实际上是`type` , 也就是`PyType_Type` , 所以它在Python中被称为 metaclass(元类) 

我们发现就算是`type`类竟然也是由`type` (PyType_Type)产生的 , 就像在type类中成了一个 "圈一样" , 自己引用自己 , 事实上确实是这样 , 同样以上一小节的例子进行说明 , 如下图 : 

![object_type_relation](http://oux34p43l.bkt.clouddn.com/object_type_relation.png?imageMogr2/blur/1x0/quality/75|watermark/2/text/bHlvbi55YW5nQHFxLmNvbQ==/font/YXBhcmFqaXRh/fontsize/560/fill/Izk0ODI4Mg==/dissolve/100/gravity/SouthEast/dx/10/dy/10)

也就是说PyType_Type中的`ob_type`指针最终指向了自己本身

这些基本上就是Python对象的创建流程了 , 但是注意对于Python内部的类型 , 创建时可能存在一些差异 , 但是这些差异并不会影响我们分析的结果

**总结 :** 

这一篇主要整理了对象创建的流程 , 以及对类型对象的整理

1. `tp_new`对应到C++中 , 可以视为`new`操作符 , Python中则是`__new__`操作符
2. `tp_init`则是Python中的`__init__` 也就是类的构造函数 , 功能就是对创建的新对象进行初始化
3. Python中一切皆对象 , 类型也是对象 ; 对象必然具有类型 , PyType_Type是类型对象的创造者
4. PyType_Type的类型就是其本身

