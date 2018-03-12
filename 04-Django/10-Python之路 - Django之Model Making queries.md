# Python之路 - Django之Model Making queries

## 介绍  🍀

一旦我们建立好模型 , Django就会自动为我们生成一套数据库抽象的API , 可以让我们进行创建 , 检索 , 更新和删除对象 , 这篇文章主要阐述怎么去使用这些API

关于模型接口的完整细节见 , [data model reference](https://docs.djangoproject.com/en/1.11/ref/models/) 

我们首先建立好模型 , 该模型构成一个博客应用 : 

```python
from django.db import models

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Entry(models.Model):
    blog = models.ForeignKey(Blog)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    authors = models.ManyToManyField(Author)
    n_comments = models.IntegerField()
    n_pingbacks = models.IntegerField()
    rating = models.IntegerField()

    def __str__(self):              # __unicode__ on Python 2
        return self.headline
```

## 获取对象  🍀

从数据库获取对象 , 是通过模型中的[Manager](https://docs.djangoproject.com/en/1.11/topics/db/managers/#django.db.models.Manager) 构造出一个[QuerySet](https://docs.djangoproject.com/en/1.11/ref/models/querysets/) ; QuerySet表示从数据库中取出来的对象的集合 , 从SQL的角度来讲 , QuerySet与WHERE语句等价

Manager则是Django模型提供数据库查询操作的接口 , 在一个Django应用中 , 每个模型至少存在一个Manager , 默认情况下命名为`objects`  , 也就是说我们的模型Manager就是我们所使用的`objects` , 例如 :

```python
models.Blog.objects.all()
'''
models.Blog:model class
objects:Manager
all:QuerySet API
'''
```

注意 : Manager只能通过模型类访问 , 而不能通过模型的实例访问 , 目的是为了强制区分"表级别" 的操作和"记录级别" 的操作 ; 对于一个模型来说 , Manager是QuerySet的主要来源

 ### 获取所有对象  🍀

可以使用Manager的`all()` 方法将一个表中的所有对象全部获取 

```python
# all()方法返回一个包含数据库表中的所有对象的QuerySet
all_entries = Entry.objects.all()
```

### 过滤器获取对象  🍀

`all()` 方法返回了一个包含数据库表中的所有记录的QuerySet , 但是通常情况下我们往往需要获取完整数据集的一个子集 , 即我们需要使用过滤器

```python
filter(**kwargs):
    """返回一个新的QuerySet,它包含满足查询参数的对象"""
exclude(**kwargs):
    """返回一个新的QuerySet,它包含不满足查询参数的对象"""
```

实例

```python
# 获取年份为2006的所有文章的QuerySet
Entry.objects.filter(pub_date_year=2006)
# 相当于
Entry.objects.all().filter(pub_date_year=2006)
```

### 链接过滤器  🍀

QuerySet的筛选结果本身还是QuerySet , 所以可以将筛选语句链接在一起 , 如下 : 

```python
Entry.objects.filter(
    headline__startswith='What'
).exclude(
    pub_date__gte=datetime.date.today()
).filter(
    pub_date__gte=datetime(2005, 1, 30)
)
```

### QuerySet唯一性  🍀

每次筛选一个QuerySet , 得到的都是全新的另一个QuerySet , 它和之前的QuerySet没有任何绑定关系 , 每次筛选都会创建一个独立的QuerySet , 它可以被存储及反复使用 , 如下 : 

```python
# 所有标题包含"what"开头的记录
q1 = Entry.objects.filter(headline__startswith="What")
# q1的子集,排除pub_date为今天的记录
q2 = q1.exclude(pub_date__gte=datetime.date.today())
# q1的子集,只选择pub_date为今天的记录
q3 = q1.filter(pub_date__gte=datetime.date.today())
'''
q1不会受筛选过程的影响
'''
```

### QuerySet惰性  🍀

QuerySet是惰性执行的 , 创建QuerySet不会带来任何数据的访问 , 类似于Python中的生成器 , 你可以将过滤器保持一整天 , 知道QuerySet需要取值时 , Django才会真正执行这个查询 , 如下 : 

```python
q = Entry.objects.filter(headline__startswith="What")
q = q.filter(pub_date__lte=datetime.date.today())
q = q.exclude(body_text__icontains="food")
# 此时才真正访问数据库
print(q)
```

### QuerySet切片  🍀

QuerySet是支持切片的 , 它等同于SQL的OFFSET和LIMIT语句

```python
# LIMIT 5,返回前5个对象
Entry.objects.all()[:5]
# OFFSET 5 LIMIT 5,返回第6至第10个
Entry.objects.all()[5:10]
```

但是QuerySet不支持负的索引 , 如 : `Entry.objects.all()[-1]` 

通常QuerySet的切片返回一个新的QuerySet , 它不会执行查询 , 但是如果使用Python切片语法中的` step` 参数 , 即步长 , 那么它将执行查询

### 获取单个对象  🍀

如需获取单个对象 , 可以使用Manager的`get()` 方法

```python
one_entry = Entry.objects.get(pk=1)
```

### 字段查询  🍀

字段查询是指如何指定SQL WHERE 子句的内容 , 通常使用过滤器的关键字参数指定

查询的关键字参数的基本形式是`field__lookuptype=value`  , 如下 : 

```python
Entry.objects.filter(pub_date__lte='2006-01-01')
# 翻译成SQL大体如下
SELECT * FROM blog_entry WHERE pub_date <='2006-01-01'
```

查询条件中指定的字段必须是模型字段的名称 ; 有一个例外 , 对于`ForeignKey` 你可以使用字段名加上`_id` 后缀 , 在这种情况下 , 该参数的值应该是外键的原始值 , 如下 : 

```python
Entry.objects.filter(blog_id=4)
```

数据库API支持大约二十种`lookuptype`  , 完整参考见 :  [field lookup reference](https://docs.djangoproject.com/en/1.11/ref/models/querysets/#field-lookups)

下面介绍几个常用的 :

- exact , 精确匹配

  ```python
  Entry.objects.get(headline__exact="Cat bites dog")
  # 对应SQL
  SELECT ... WHERE headline = 'Cat bites dog';
  # 如果关键字参数不包含双下划线,默认假定查询类型是exact,以下两条语句相等
  Blog.objects.get(id__exact=14)  # Explicit form
  Blog.objects.get(id=14)         # __exact is implied
  ```

- iexact , 大小写不敏感的匹配

  ```python
  # 将匹配标题为"Beatles Blog","beatles blog"甚至"BeAtlES blOG"的Blog
  Blog.objects.get(name__iexact="beatles blog")
  ```

- contains , 大小写敏感的包含关系测试

  ```python
  Entry.objects.get(headline__contains='Lennon')
  # 翻译成SQL
  SELECT ... WHERE headline LIKE '%Lennon%';
  '''
  这将匹配'Today Lennon honored',但不能匹配'today lennon honored'
  还有一个大小写不敏感版本,icontains
  '''
  ```

- startswith , endswith , 以 ... 开头 , 以 ... 结尾

更多详细字段类型会在下一篇文章中整理

### 跨表查询  🍀

Django提供了一种强大又直观的方式来"处理"查询中的关联关系 , 它在后台自动帮你处理JOIN

如果要进行跨表查询 , 只需要使用关联的模型字段的名称 , 并使用双下划线分隔 , 直至你想要的字段 , 如下 : 

```python
# 获取所有Blog表中name为'Beatles Blog'的Entry对象
Entry.objects.filter(blog__name='Beatles Blog')
```

这种跨越可以是任意深度的 , 它还可以反向工作 , 若要引用一个"反向"的关系 , 只需要使用该模型的小写的名称 , 如下 : 

```python
# 获取所有Entry表中headline包含'Lennon'的Blog对象
Blog.objects.filter(entry__headline__contains='Lennon')
```

如果在多个关联关系过滤而且其中某个中介模型没有满足过滤条件的值 , Django将把它当做一个空的(所有的值都为NULL) 但是合法的对象 , 这意味着不会有错误引发

```python
Blog.objects.filter(entry__authors__name='Lennon')
```

更多实例

```python
models.Tb1.objects.filter(id__lt=10, id__gt=1)   # 获取id大于1 且 小于10的值
models.Tb1.objects.filter(id__in=[11, 22, 33])   # 获取id等于11、22、33的数据
models.Tb1.objects.exclude(id__in=[11, 22, 33])  # not in
models.Tb1.objects.filter(id__range=[1, 2])      # 范围bettwen and
```

### F expressions  🍀

如果我们想将模型的一个字段与同一个模型的另外一个字段进行比较 , 可以使用`F()` 表达式

`F()` 返回的实例用作查询内部对模型字段的引用 , 然后可以在过滤器中使用这些引用来比较同一模型实例中两个不同字段的值 , 如下 : 

```python
from django.db.models import F
# 获取所有comments数目大于pingbacks的Entry对象,gt表示大于,将在下一篇QuerySet API中详细介绍
Entry.objects.filter(n_comments__gt=F('n_pingbacks'))
```

Django支持对`F()`对象使用加法 , 减法 , 乘法 , 除法 , 取模以及幂运算等算数操作 , 两个操作数可以都是常数和其他`F()` 对象 , 如下 : 

```python
# 查找comments数目比pingbacks两倍还多的Entry对象
Entry.objects.filter(n_comments__gt=F('n_pingbacks') * 2)
```

`F()` 对象同样可以使用双下划线进行跨表 

```python
# 获取author的名字与blog名字相同的Entry对象
Entry.objects.filter(authors_name=F('blog__name'))
```

对于date和date/time字段 , 可以给它们加上或减去一个`timedalta`对象 

```python
# 获取发布超过3天后被修改的所有Entry对象
from datetime import timedelta
Entry.objects.filter(mod_date__gt=F('pub_date') + timedelta(days=3))
```

`F()` 对象支持位操作`bitand()` , `bitor()` , `bitrightshift()` 和 `bitleftshift()` 

```python
F('somefield').bitand(16)
```

更多F表达式相关 :  [F expressions](https://docs.djangoproject.com/en/1.11/ref/models/expressions/#django.db.models.F) 

### 缓存与QuerySet  🍀

每个QuerySet都包含一个缓存来最小化对数据的访问 , 在一个新创建的QuerySet中 , 缓存为空 ; 首次对QuerySet进行求值 , 同时发生数据库查询 , Django将保存查询的结果到QuerySet的缓存中并返回明确请求的结果 , 我们需要考虑的是对QuerySet重用缓存的问题

如果QuerySet使用不当 , 它是会坑你的 , 如下 :

```python
# 查询后就释放缓存
print([e.headline for e in Entry.objects.all()])
# 查询后就释放缓存
print([e.pub_date for e in Entry.objects.all()])
'''
这两条语句意味着相同的数据库查询将执行两次,
显然倍增了数据库负载,
同时,还有可能两个结果列表并不一样,
因为两次请求期间有可能有新的Entry对象被添加进来或删除掉
'''
```

为了避免这个问题 , 我们只需保存QuerySet并重新使用它

```python
queryset = Entry.objects.all()
print([p.headline for p in queryset]) # Evaluate the query set.
print([p.pub_date for p in queryset]) # Re-use the cache from the evaluation.
```

**QuerySet不缓存**

QuerySet并不总是缓存它们的结果 , 当只对查询集的部分进行求值时会检查缓存 , 但是如果这部分不在缓存中 , 那么接下来查询返回的记录都将不会被缓存 ; 具体的说 , 这意味着使用切片或索引来约束查询集将不会进行缓存

实例1

```python
# 重复获取查询集对象中一个特定的索引将每次都查询数据库,不会进行缓存
queryset = Entry.objects.all()
print(queryset[5]) # Queries the database
print(queryset[5]) # Queries the database again
```

实例2

```python
# 已经对全部查询集求值过,则将检查缓存
queryset = Entry.objects.all()
[entry for entry in queryset] # Queries the database
print(queryset[5]) # Uses cache
print(queryset[5]) # Uses cache
```

下面是一些其它的例子 , 它们会使得全部的查询集被求值并填充到缓存中

```python
>>> [entry for entry in queryset]
>>> bool(queryset)
>>> entry in queryset
>>> list(queryset)
```

注意 : 简单地打印查询集不会填充缓存 , 因为`__repr__()` 调用只会返回全部查询集的一个切片

更多 :  [OR lookups examples](https://github.com/django/django/blob/master/tests/or_lookups/tests.py) 

Manager更多详细资料 : https://docs.djangoproject.com/en/1.11/topics/db/managers/

更多Making queries : https://docs.djangoproject.com/en/1.11/topics/db/queries/

Model API reference : https://docs.djangoproject.com/en/1.11/ref/models/

下一章将会对本章的一些内容进行说明 , 及`QuerySet API` 