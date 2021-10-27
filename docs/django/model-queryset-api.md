# Django - Model QuerySet API








<extoc></extoc>

## 介绍

我们知道Django中存在着大量的接口 , 而跟QuerySet 就是一个Model相关的接口 , 它建立在 [model](https://docs.djangoproject.com/en/1.11/topics/db/models/) 和 [database query](https://docs.djangoproject.com/en/1.11/topics/db/queries/) 指南的基础上 , 而这两个指南已经在前面的文章整理完成了 , 但是对于QuerySet API的整理还不完全

本篇中依然会使用在上一篇中使用的例子

上一篇中我们已经知道 , 当我们不对`QuerySet` 进行求值时 , 它会像生成器一样 , 不做任何反应

`QuerySet` 求值有以下方法 : 

- 迭代 , `QuerySet` 是可迭代的 , 它在首次迭代查询集时会对数据库进行查询 , 实例如下 : 

  ```python
  for e in Entry.objects.all():
      print(e.headline)
  '''
  这两条语句虽然可以验证在数据库中是否至少存在一条记录,但是使用exists()方法会更高效
  '''
  ```

- 切片 , 如 [Limiting QuerySets](https://docs.djangoproject.com/en/1.11/topics/db/queries/#limiting-querysets) 中说的那样 , 可以使用Python的序列切片语法对一个`QuerySet` 进行切片 ; 一个未求值的`QuerySet` 进行切片通常返回另一个未求值的`QuerySet` , 但是如果使用"step"参数 , Django 将执行数据库查询并返回一个列表 ; 对一个已经求值的`QuerySet` 进行切片将返回一个列表

  注意 : 虽然对未求值的`QuerySet` 进行切片返回另一个未求值的`QuerySet` , 但是却不可以进一步修改它 , 比如添加更多的filter , 或者修改排序的方式 , 因为这将不太好翻译成SQL而且含义也不清晰

- Pickling/Caching , 序列化将读取数据库 , 下节介绍

- repr() , 当对`QuerySet` 调用`repr()` 时 , 将对它求值 ; 这是为了在Python交互式解释器中方便显示结果

- len() , 当对`QuerySet` 调用`len()` 时 , 将对它求值 , 返回一个查询集的长度

  注意 : 如果确定集合中记录的数量 , 而不需要实际的数据对象 , 那么使用SQL语句的`SELECT COUNT(*)`效率会更高 , 为此Django提供了一个`count()` 方法 

- list() , 当对`QuerySet` 调用`list()` 将强制对它求值

- bool() , 测试布尔值 , 例如使用`bool()` , and , or 或者if语句将导致查询集的执行

## Pickling QuerySet

如果你pickle一个`QuerySet` , 它将在pickle之前强制将所有的结果加载到内存中 ; pickle通常用于缓存之前 , 并且当缓存的查询集重新加载时 , 你希望结果已经存在随时准备使用 ; 不过注意 , pickle的数据只是pickle时的 , 也就是说pickle的数据不是即时的

如果此后你只想pickle必要的信息来重新创建`QuerySet` , 可以使用如下方式 : 

```python
import pickle
query = pickle.loads(s)     # Assuming 's' is the pickled string.
qs = MyModel.objects.all()
qs.query = query            # Restore the original 'query'.
```

query是一个不透明的对象 , 它表示查询的内部构造 , 不属于公开的API

注意 : `QuerySet` 的pickle在不同的Django版本中是不保证兼容的 , 所以pickle不可用于归档的长期策略

## QuerySet API

```python
class QuerySet(model=None, query=None, using=None):
    """
    通常,当你与QuerySet交互时,都是通过链接过滤器来使用它
    为了实现这一功能,大多数QuerySet方法都返回新的QuerySet
    QuerySet类有两个公共属性:
    ordered:如果QuerySet是排好序的则为True,如有一个order_by()子句或者模型有默认的排序;否则为False
    db:如果现在执行,则返回将使用的数据库
    """
```

`QuerySet` 存在query参数是为了让具有特殊查询用途的子类如`GeoQuerySet` 可以重新构造内部的查询状态 , 这个参数的值是查询状态的不透明的表示 , 不是一个公开的API

QuerySet API 中有非常多的方法供我们使用 , 分为如下几种 : 

- 返回新的QuerySet
- 不返回新的QuerySet
- field查找
- 聚合函数

## 返回QuerySet

Django提供了一系列的QuerySet筛选方法 , 用于改变QuerySet返回的结果类型或者SQL查询执行的方式

### filter()

```python
filter(**kwargs):
    """
    返回一个新的QuerySet,它包含满足查询参数的对象
    **kwargs:应该满足字段查询中的格式,在底层的SQL语句中,多个参数通过AND连接
    """
```

### exclude()

```python
exclude(**kwargs):
    """
    返回一个新的QuerySet,它包含不满足给定查询参数的对象
    **kwargs:应该满足字段查询中的格式,在底层的SQL语句中,多个参数通过AND连接,然后所有的内容放入NOT()中
    """
```

实例

```python
Entry.objects.exclude(pub_date__gt=datetime.date(2005, 1, 3)).exclude(headline='Hello')
# 对应的SQL
SELECT ...
WHERE NOT pub_date > '2005-1-3'
AND NOT headline = 'Hello'
```

### annotate()

```python
annotate(*args,**kwargs):
    """
    使用提供的查询表达式注释QuerySet中的每个对象,表达式可以是简单的值,对模型上字段的应用,
    对与QuerySet中对象相关的对象进行计算的聚合表达式
    *args,**kwargs:每个参数都是一个注释,它将添加到返回的QuerySet中的每个对象
    """
```

实例

```python
'''我们正在操作一个Blog对象列表,你可能想知道每个Blog有多少Entry'''
>>> from django.db.models import Count
>>> q = Blog.objects.annotate(Count('entry'))
# The name of the first blog
>>> q[0].name
'Blogasaurus'
# The number of entries on the first blog
>>> q[0].entry__count       # Blog模型本身没有定义entry__count属性
42
```

控制Annotation的名称

```python
>>> q = Blog.objects.annotate(number_of_entries=Count('entry'))
# The number of entries on the first blog, using the name provided
>>> q[0].number_of_entries
42
```

### order_by()

```python
order_by(*fields):
    """
    对QuerySet进行指定排序;默认情况下,QuerySet返回的结果是由模型的元数据中的排序选项指定的
    *fields:指定排序的字段
    """
```

实例

```python
# 先按照pub_date降序排列,然后再按照headline升序排序
Entry.objects.filter(pub_date__year=2005).order_by('-pub_date', 'headline')
'''
"-",负号表示降序;升序是隐含的,随机可以使用"?"
'''
# 这种方式查询可能耗费资源而且很慢,取决于使用的数据库
Entry.objects.order_by('?')
```

使用跨表 , 即双下划线 : 

```python
Entry.objects.order_by('blog__name', 'headline')
```

如果排序的字段与另外一个模型关联 , Django将使用关联的模型的默认排序 , 或者如果没有指定`Meta.ordering` 将通过关联的模型的主键排序 , 如下 :

```python
Entry.objects.order_by('blog')
# 与上面相同
Entry.objects.order_by('blog__id')
# Blog设置ordering=['name'],第一个QuerySet等同于
Entry.objects.order_by('blog__name')
```

### reverse()

```python
reverse():
    """翻转,即反向排序"""
```

实例

```python
# 获取QuerySet中最后五个元素
my_queryset.reverse()[:5]
# 注意QuerySet应该已经定义排序,否则reverse将无效
```

### distinct()

```python
distinct(*fields):
    """
    返回一个在SQL查询中使用SELECT DISTINCT的新QuerySet,它将去除查询结果中重复的行
    """
```

默认情况下 , QuerySet不会去除重复的行 ; 在实际应用中这一般不是个问题 , 但是如果查询跨越多张表 , 当对QuerySet求值时就可能得到重复的结果 , 这时候我们就应该使用`distinct()` 

注意 : `order_by()` 调用中的任何字段都将包含在SQL的SELECT列中 , 与`distinct()` 一起使用时可能导致无法预料的后果 ; 总之使用`distiinct()` 时 , 一定要注意相关模型的排序

### values()

```python
values(*fields,**expressinos):
    """
    返回一个QuerySet字典,每个字典表示一个对象,键对应于模型对象的属性名称
    """
```

实例

```python
# This list contains a Blog object.
>>> Blog.objects.filter(name__startswith='Beatles')
<QuerySet [<Blog: Beatles Blog>]>

# This list contains a dictionary.
>>> Blog.objects.filter(name__startswith='Beatles').values()
<QuerySet [{'id': 1, 'name': 'Beatles Blog', 'tagline': 'All the latest Beatles news.'}]>
```

SELECT接收可选的位置参数`*fields` , 它指定values()应该限制哪些字段 ; 如果指定字段 , 每个字典将只包含指定字典的键/值 , 如果没有指定字段 , 每个字典将包含数据库中所有字段的键和值 , 如下 :

```python
>>> Blog.objects.values()
<QuerySet [{'id': 1, 'name': 'Beatles Blog', 'tagline': 'All the latest Beatles news.'}]>
>>> Blog.objects.values('id', 'name')
<QuerySet [{'id': 1, 'name': 'Beatles Blog'}]>
```

采用关键字参数`**expressions` , 这些参数传递给`annotate()` :

```python
>>> from django.db.models.functions import Lower
>>> Blog.objects.values(lower_name=Lower('name'))
<QuerySet [{'lower_name': 'beatles blog'}]>
```

### values_list()

```python
value_list(*fields,flat=False):
    """
    与values()类似,只是在迭代时返回的是元组而不是字典
    flat:如果为True表示返回的结果是单个值而不是元组
    如果有多个字段,传递flat将发生错误
    """
```

实例

```python
>>> Entry.objects.values_list('id').order_by('id')
<QuerySet[(1,), (2,), (3,), ...]>

>>> Entry.objects.values_list('id', flat=True).order_by('id')
<QuerySet [1, 2, 3, ...]>
```

### dates()

```python
dates(field,kind,order='ASC'):
    """
    返回一个QuerySet,其为一个包含datetime.date对象的列表;date对象在QuerySet中表示特定类型的所有可用时间
    field:DateField名称
    kind:应为year,month,day
    	-year,返回对应该字段的所有不同年份值的list
    	-month,返回字段的所有不同年/月值的list
    	-day,返回字段的所有不同年/月/日值的list
    order:指定排序方式,默认为ASC,即升序还可设置为DESC,即为降序
    """
```

实例

```python
>>> Entry.objects.dates('pub_date', 'year')
[datetime.date(2005, 1, 1)]
>>> Entry.objects.dates('pub_date', 'month')
[datetime.date(2005, 2, 1), datetime.date(2005, 3, 1)]
>>> Entry.objects.dates('pub_date', 'day')
[datetime.date(2005, 2, 20), datetime.date(2005, 3, 20)]
>>> Entry.objects.dates('pub_date', 'day', order='DESC')
[datetime.date(2005, 3, 20), datetime.date(2005, 2, 20)]
>>> Entry.objects.filter(headline__contains='Lennon').dates('pub_date', 'day')
[datetime.date(2005, 3, 20)]
```

### datetimes()

```python
datetimes(field_name,kind,order='ASC',tzinfo=None):
    """
    与dates()相同
    field_name:为DateField的名称
    kind:应为hour,minute,month,year,second,day
    order:同dates()
    tzinfo:定义在阶段之前将数据时间转换到的时区
    """
```

### none()

调用`none()` 将创建一个从不返回任何对象的queryset , 并且在访问结果时不会执行任何查询 ; `qs.name()` 查询集是`EmptyQuerySet` 的一个实例

实例

```python
>>> Entry.objects.none()
<QuerySet []>
>>> from django.db.models.query import EmptyQuerySet
>>> isinstance(Entry.objects.none(), EmptyQuerySet)
True
```

### all()

返回当前`QuerySet` 或`QuerySet` 子类的副本 , 它可以用于在你希望传递一个模型管理器或`QuerySet` 并对结果做进一步过滤的情况

当对`QuerySet` 进行求值时 , 会缓存其结果 ; 如果数据库中的数据在`QuerySet` 求值之后可能已经改变 , 你可以通过在以前求值过的`all()` 上调用相同的`QuerySet` 查询以获得更新后的结果

### union()

```python
union(*other_qs,all=False):
    """
    使用SQL的UNION运算符组合两个或多个Queryset的结果
    all:为False表示不允许重复值,True即允许重复值
    """
```

实例

```python
>>> qs1.union(qs2, qs3)
```

### intersection()

```python
intersection(*other_qs):
    """使用SQL的INTERSECT运算符返回两个或多个QuerySet的共享元素"""
```

实例

```python
>>> qs1.intersection(qs2, qs3)
```

### difference()

```python
difference(*other_qs):
    """使用SQL的EXCEPT运算符只保留QuerySet中的元素,而不是在其他QuerySet中保存"""
```

实例

```python
>>> qs1.difference(qs2, qs3)
```

### select_related()

```python
select_related(*fields):
    """
    返回一个QuerySet,当执行它的查询时它沿着外键关系查询关联的对象的数据
    它会生成一个复杂的查询并引起性能的损耗,但是在以后使用外键关系时将不需要数据库查询
    简单说,在对QuerySet使用select_related()函数后,Django会获取相应外键对应的对象,从而在之后需要的时候不必再查询数据库了
    """
```

普通查询

```python
# Hits the database.
e = Entry.objects.get(id=5)

# Hits the database again to get the related Blog object.
b = e.blog
```

`select_related()` 查询

```python
# Hits the database.
e = Entry.objects.select_related('blog').get(id=5)

# Doesn't hit the database, because e.blog has been prepopulated
# in the previous query.
b = e.blog
```

`select_related()` 可用于objects的查询集

```python
from django.utils import timezone

# Find all the blogs with entries scheduled to be published in the future.
blogs = set()

for e in Entry.objects.filter(pub_date__gt=timezone.now()).select_related('blog'):
    # Without select_related(), this would make a database query for each
    # loop iteration in order to fetch the related blog for each entry.
    blogs.add(e.blog)
```

注 : `select_related('foo', 'bar')` 等同 `select_related('foo').select_related('bar')` 

### prefetch_related()

```python
prefetch_related(*lookups):
    """
    返回一个QuerySet,它将在单个批处理中自动检索每个指定查找的相关对象
    """
```

这具有与`select_related`类似的目的 , 两者都被设计为阻止由访问相关对象而导致的数据库查询的泛滥 , 但是策略是完全不同的

`select_related`通过创建SQL连接并在`SELECT`语句中包括相关对象的字段来工作 ;  因此 , `select_related`在同一数据库查询中获取相关对象 ,  然而 , 为了避免由于跨越"多个"关系而导致的大得多的结果集 , `select_related`限于单值关系 - 外键和一对一关系

`prefetch_related` , 另一方面 , 为每个关系单独查找 , 并在Python中"加入" ,  这允许它预取多对多和多对一对象 , 除了外键和一对一关系 , 它们不能使用`select_related`来完成 

### extra()

```python
extra(select=None,where=None,params=None,tables=None,order_by=None,select_params=None):
    """
    有些情况下,Django的查询语法难以简单的表达复杂的WHERE子句,对于这种情况,
    Django提供了extra()修改机制,它能在QuerySet生成的SQL从句中注入新子句
    """
```

`extra()`可以指定一个或多个WHERE , 如下 :

- select , 该参数可以让你在SELECT从句中添加其他字段信息,它应该是一个字典,存放着属性名到SQL从句的映射

  ```python
  Entry.objects.extra(select={'is_recent': "pub_date > '2006-01-01'"})
  # 对应的SQL
  SELECT blog_entry.*, (pub_date > '2006-01-01') AS is_recent
  FROM blog_entry;
  ```

- where/tables , 你可以使用WHERE定义显示SQL where子句 , 也许执行非显示连接 ; 你可以使用FROM手动将表添加到SQL tables子句 ; where和tables都接受字符串列表 , 所有where参数均为"与"任何其他搜索条件

  ```python
  Entry.objects.extra(where=["foo='a' OR bar = 'a'", "baz = 'a'"])
  # SQL如下
  SELECT * FROM blog_entry WHERE (foo='a' OR bar='a') AND (baz='a')
  ```

- order_by , 如果你需要使用通过`extra()`包含的一些新字段或表来对结果查询进行排序 , 可以使用order_by参数传入一个字符串序列 , 这些字符串应该是模型字段 , 如下 :

  ```python
  q = Entry.objects.extra(select={'is_recent': "pub_date > '2006-01-01'"})
  q = q.extra(order_by = ['-is_recent'])
  '''
  同前面的order_by参数
  '''
  ```

- params , 上述where参数可以使用标准Python数据库字符串占位符`%s` , 来指示数据库引擎应自动引用的参数 ; params参数是要替换的任何额外参数的列表

  ```python
  # 引号被正确转义
  Entry.objects.extra(where=['headline=%s'], params=['Lennon'])
  # 始终使用params而不是将值直接嵌入where,因为params会确保根据你的特定后端正确引用值
  ```

### defer()

```python
defer(*fields):
    """用于延迟字段的查询集"""
```

在一些复杂的数据建模情况下 , 你的模型可能包含大量字段 , 其中一些可能包含大量数据 (例如文本字段) , 或者需要昂贵的处理来将他们转换为Python对象 ; 当你最初获取数据时不知道是否需要这些特定字段的情况下 , 如果你正在使用查询集的结果 , 你可以告诉Django不要从数据库中检索它们

```python
# 通过传递字段名称到defer()实现不加载
Entry.objects.defer("headline", "body")
```

具有延迟字段的查询集仍将返回模型实例 , 每个延迟字段将在你访问该字段时从数据库中检索 , 并且每次只检索一个 , 而不是一次检索所有的延迟字段

还可以多次调用

```python
# Defers both the body and headline fields.
Entry.objects.defer("body").filter(rating=5).defer("headline")
```

### only()

```python
only(*fields):
    """与defer相反,仅让这些字段立即加载,其余的被延迟"""
```

对`only()`的连续调用的结果是只有最后一次调用的字段被考虑

```python
# This will defer all fields except the headline.
Entry.objects.only("body", "rating").only("headline")
```

由于`defer()` 以递增方式动作 (想延迟列表中添加字段) , 因此你可以结合`only()` 和 `defer()` , 它们将合乎逻辑地工作 : 

```python
# Final result is that everything except "headline" is deferred.
Entry.objects.only("headline", "body").defer("body")

# Final result loads headline and body immediately (only() replaces any
# existing set of fields).
Entry.objects.defer("body").only("headline", "body")
```

### using()

```python
using(alias):
    """
    控制QuerySet在哪个数据库上求值
    alias:数据库的别名,定义在DATABASES
    """
```

实例

```python
# queries the database with the 'default' alias.
>>> Entry.objects.all()

# queries the database with the 'backup' alias
>>> Entry.objects.using('backup')
```

### select_for_update()

```python
select_for_update(nowait=False,skip_locked=False):
    """
    返回一个锁住行直到事务结束的查询集,如果数据库支持,
    它将生成一个SELECT ... FOR UPDATE语句
    nowait:默认如果其他事务锁定了相关行,那么本查询将被阻塞,直到锁被释放;改为True使查询不阻塞
    skip_locked:如果其他事务持有冲突的锁,可以改为Trye忽略锁定的行
    nowait与skip_locked是互斥的,同时启用会导致ValueError
    """
```

### raw()

```python
raw(raw_query,params=None,translations=None):
    """
    接收一个原始的SQL查询,执行并返回一个django.db.models.query.RawQuereySet实例
    这个RawQuerySet实例可以迭代以提供实例对象,就像普通的QuerySet一样
    """
```

`raw()` 永远触发一个新的查询 , 而与之前的filter无关 ; 因此 , 它通常应该从Manager或一个全新的QuerySet实例调用

## 不返回QuerySet

以下方法对QuerySet进行求值并返回 , 返回结果不是QuerySet

这些方法不使用高速缓存 , 并且每次被调用的时候都会查询数据库

### get()

返回按照查询参数匹配到的对象 , 如果匹配到的对象个数不止一个 , get()将会触发`MultipleObjectReturned`异常

实例

```python
entry = Entry.objects.filter(...).exclude(...).get()
```

### create()

快捷创建对象并保存 , 如下 : 

```python
p = Person.objects.create(first_name="Bruce", last_name="Springsteen")
# 等同如下
p = Person(first_name="Bruce", last_name="Springsteen")
p.save(force_insert=True)
```

### get_or_create()

```python
get_or_create(defaults=None,**kwargs):
    """
    通过给出的kwargs来查询对象的便捷方法,需要的话创建一个对象,
    返回一个由(object,created)组成的元组,object是一个查询到的或者是被创建的对象,created是一个表示是否创建了新的对象的布尔值
    """
```

实例

```python
obj, created = Person.objects.get_or_create(
    first_name='John',
    last_name='Lennon',
    defaults={'birthday': date(1940, 10, 9)},
)
```

任何传递给 `get_or_create()` 的关键字参数 , 除了一个可选的`defaults`, 都将传递给get() 调用 ; 如果查找到一个对象 , `get_or_create()` 返回一个包含匹配到的对象以及`False` 组成的元组 , 如果查找到的对象超过一个以上 , `get_or_create` 将引发`MultipleObjectsReturned`异常 , 如果查找不到对象 , `get_or_create()` 将会实例化并保存一个新的对象 , 返回一个由新的对象以及`True` 组成的元组 ,  新的对象将会大概按照以下的逻辑创建 :

```python
params = {k: v for k, v in kwargs.items() if '__' not in k}
params.update({k: v() if callable(v) else v for k, v in defaults.items()})
obj = self.model(**params)
obj.save()
```

### update_or_create()

```python
update_or_create(defaults=None,**kwargs):
    """
    返回一个由(object,created)组成的元组,
    元组中的object是一个创建的或者是被更新的对象,
    created是一个标识是否创建了心得额对象的布尔值
    """
```

实例

```python
obj, created = Person.objects.update_or_create(
    first_name='John', last_name='Lennon',
    defaults={'first_name': 'Bob'},
)
```

### bulk_create()

```python
bulk_create(objs,batch_size=None):
    """
    以高效的方式(通常只有1个查询,无论多少对象)将提供的对象列表插入到数据库中
    obj:插入的对象
    batch_size:控制在单个查询中创建的对象数;默认值是在一个批处理中创建所有的对象,除了SQLite,其中默认值为每个查询最多使用999个变量
    """
```

实例

```python
>>> Entry.objects.bulk_create([
...     Entry(headline='This is a test'),
...     Entry(headline='This is only a test'),
... ])
```

该方法需要注意以下 : 

- 将不会调用模型的sava()方法 , 并且不会发送`pre_save` 和 `post_save` 信号
- 它不适用于多表继承场景中的子模型
- 如果模型的主键是`AutoField` , 则不会像`save()` 那样检索并设置主键属性 , 除非数据库后端支持(当前是PostgreSQL)
- 它不适用于多对多关系

### count()

返回在数据中对应的`QuerySet` 对象的个数 , `count()` 永远不会引发异常

```python
# Returns the total number of entries in the database.
Entry.objects.count()

# Returns the number of entries whose headline contains 'Lennon'
Entry.objects.filter(headline__contains='Lennon').count()
```

### in_bulk()

```python
in_bulk(id_list=None):
    """
    获取主键值的列表,并返回将每个主键值映射到具有给定ID的对象的实例的字典,
    如果未提供列表,则会返回查询集中的所有对象
    """
```

实例

```python
>>> Blog.objects.in_bulk([1])
{1: <Blog: Beatles Blog>}
>>> Blog.objects.in_bulk([1, 2])
{1: <Blog: Beatles Blog>, 2: <Blog: Cheddar Talk>}
>>> Blog.objects.in_bulk([])
{}
>>> Blog.objects.in_bulk()
{1: <Blog: Beatles Blog>, 2: <Blog: Cheddar Talk>, 3: <Blog: Django Weblog>}
```

### iterator()

对QuerySet进行求值并返回一个迭代器 , 其不会在QuerySet级别执行任何缓存 (内部 , 默认迭代器调用iterator() 并高速缓存返回值)

### latest()

```python
latest(field_name=None):
    """
    按日期返回表中的最新对象
    field_name:日期字段
    """
```

实例

```python
Entry.objects.latest('pub_date')
```

### earliest()

除非方向更改 , 否则像`latest()` 

### first()

返回结果集的第一个对象 , 当没有找到时返回None ; 如果QuerySet没有设置排序 , 则将会自动按主键进行排序 , 如下 :

```python
p = Article.objects.order_by('title', 'pub_date').first()
```

### last()

工作方式类似first() , 只是返回的是查询集中最后一个对象

### aggregate()

```python
aggregate(*args,**kwargs):
    """
    返回汇总值的字典(平均值,总和等),通过QuerySet进行计算
    每个参数指定返回的字典中将要包含的值
    """
```

实例

```python
>>> from django.db.models import Count
>>> q = Blog.objects.aggregate(Count('entry'))
{'entry__count': 16}
>>> q = Blog.objects.aggregate(number_of_entries=Count('entry'))
{'number_of_entries': 16}
```

### exists()

如果QuerySet包含任何结果 , 则返回True , 否则返回False

它视图用最简单和最快的方法完成查询 , 但它执行的方法与普通的QuerySet查询几乎一样 , exists()用于搜寻对象是都在QuerySet中以及QuerySet受否存在任何对象 , 特别是QuerySet比较大的时候

```python
entry = Entry.objects.get(pk=123)
if some_queryset.filter(pk=entry.pk).exists():
    print("Entry contained in queryset")
```

### update()

对指定的字段执行SQL更新查询 , 并返回匹配的行数 (如果某些行已具有新值 , 则可能不等于已更新的行数)

```python
>>> Entry.objects.filter(pub_date__year=2010).update(comments_on=False, headline='This is old')
```

### delete()

对QuerySet中的所有行执行SQL删除查询 , 并返回删除的对象数和每个对象类型的删除次数的字典

```python
>>> b = Blog.objects.get(pk=1)

# Delete all the entries belonging to this Blog.
>>> Entry.objects.filter(blog=b).delete()
(4, {'weblog.Entry': 2, 'weblog.Entry_authors': 2})
```

### as_manager()

`classmethod as_manager()` 

类方法 , 返回Manager的实例与QuerySet的方法的副本

## Field查询

字段查询是指如何指定SQL WHERE子句的内容 , 它通过`QuerySet的filter()` , `exclude()` 和 `get()` 的关键字参数指定 , 即使用双下划线时后的参数

### exact

精确匹配 , 如果为比较提供的值为NULL , 它将被解释SQL None

```python
Entry.objects.get(id__exact=14)
Entry.objects.get(id__exact=None)
# 等价的SQL
SELECT ... WHERE id = 14;
SELECT ... WHERE id IS NULL;
```

### iexact

不区分大小写的精确匹配 , 如果为比较提供的值为NULL , 它将被解释为SQL None

```python
Blog.objects.get(name__iexact='beatles blog')
Blog.objects.get(name__iexact=None)
# 等价的SQL
SELECT ... WHERE name ILIKE 'beatles blog';
SELECT ... WHERE name IS NULL;
```

### contains

大小写敏感的包含关系测试

```python
Entry.objects.get(headline__contains='Lennon')
# 等价SQL
SELECT ... WHERE headline LIKE '%Lennon%';
```

### icontains

与contains相反 , 大小写不敏感的包含关系测试

```python
Entry.objects.get(headline__icontains='Lennon')
# 等价SQL
SELECT ... WHERE headline ILIKE '%Lennon%';
```

### in

在给定的列表

```python
Entry.objects.filter(id__in=[1, 3, 4])
# 等价SQL
SELECT ... WHERE id IN (1, 3, 4);
```

### gt

大于

```python
Entry.objects.filter(id__gt=4)
# 等价SQL
SELECT ... WHERE id > 4;
```

### gte

大于或等于

### lt

小于

### lte

小于或等于

### startswith

区分大小写 , 开始位置匹配

```python
Entry.objects.filter(headline__startswith='Lennon')
# 等价SQL
SELECT ... WHERE headline LIKE 'Lennon%';
```

### istartswith

不区分大小写 , 开始位置匹配

```python
Entry.objects.filter(headline__istartswith='Lennon')
# 等价SQL
SELECT ... WHERE headline ILIKE 'Lennon%';
```

### endswith

区分大小写 , 结尾位置匹配

```python
Entry.objects.filter(headline__endswith='Lennon')
# 等价SQL
SELECT ... WHERE headline LIKE '%Lennon';
```

### iendswith

不区分大小写 , 结尾位置匹配

```python
Entry.objects.filter(headline__iendswith='Lennon')
# 等价SQL
SELECT ... WHERE headline ILIKE '%Lennon'
```

### range

范围测试

```python
import datetime
start_date = datetime.date(2005, 1, 1)
end_date = datetime.date(2005, 3, 31)
Entry.objects.filter(pub_date__range=(start_date, end_date))
# 等价SQL
SELECT ... WHERE pub_date BETWEEN '2005-01-01' and '2005-03-31';
```

### date

对于datetime字段 , 将值作为日期转换 ; 允许链接附加字段查找 , 获取日起值

```python
Entry.objects.filter(pub_date__date=datetime.date(2005, 1, 1))
Entry.objects.filter(pub_date__date__gt=datetime.date(2005, 1, 1))
```

### year

对于日期和时间字段 , 确切的年匹配 , 循序链接附加字段查找

```python
Entry.objects.filter(pub_date__year=2005)
Entry.objects.filter(pub_date__year__gte=2005)
# 等价SQL
SELECT ... WHERE pub_date BETWEEN '2005-01-01' AND '2005-12-31';
SELECT ... WHERE pub_date >= '2005-01-01';
```

### month

对于日期和日期时间字段 , 确切的月份匹配 , 允许链接附加字段查找

```python
Entry.objects.filter(pub_date__month=12)
Entry.objects.filter(pub_date__month__gte=6)
# 等价SQL
SELECT ... WHERE EXTRACT('month' FROM pub_date) = '12';
SELECT ... WHERE EXTRACT('month' FROM pub_date) >= '6';
```

### day

对于日期和日期时间字段 , 具体到某一天的匹配 , 允许链接附加字段查找 

```python
Entry.objects.filter(pub_date__day=3)
Entry.objects.filter(pub_date__day__gte=3)
# 等价SQL
SELECT ... WHERE EXTRACT('day' FROM pub_date) = '3';
SELECT ... WHERE EXTRACT('day' FROM pub_date) >= '3';
```

### week

对于日期和日期时间字段 , 根据 [ISO-8601](https://en.wikipedia.org/wiki/ISO-8601) 返回周号 , 即星期一开始的星期

```python
Entry.objects.filter(pub_date__week=52)
Entry.objects.filter(pub_date__week__gte=32, pub_date__week__lte=38)
```

### week_day

对于日期和日期时间字段 , 周号匹配 , 允许链接附加字段查找

```python
Entry.objects.filter(pub_date__week_day=2)
Entry.objects.filter(pub_date__week_day__gte=2)
```

### time

对于datetime字段 , 将值转换为时间 , 允许链接附加字段查找 , 获取datetime.time的值

```python
Entry.objects.filter(pub_date__time=datetime.time(14, 30))
Entry.objects.filter(pub_date__time__between=(datetime.time(8), datetime.time(17)))
```

### hour

对于日期时间和时间字段 , 确切的时间匹配 , 允许链接附加字段查找

```python
Event.objects.filter(timestamp__hour=23)
Event.objects.filter(time__hour=5)
Event.objects.filter(timestamp__hour__gte=12)
# 等价SQL
SELECT ... WHERE EXTRACT('hour' FROM timestamp) = '23';
SELECT ... WHERE EXTRACT('hour' FROM time) = '5';
SELECT ... WHERE EXTRACT('hour' FROM timestamp) >= '12';
```

### minute

对于日期时间和时间字段 , 确切的分钟匹配 , 允许链接附加字段查找

```python
Event.objects.filter(timestamp__minute=29)
Event.objects.filter(time__minute=46)
Event.objects.filter(timestamp__minute__gte=29)
# 等价SQL
SELECT ... WHERE EXTRACT('minute' FROM timestamp) = '29';
SELECT ... WHERE EXTRACT('minute' FROM time) = '46';
SELECT ... WHERE EXTRACT('minute' FROM timestamp) >= '29';
```

### second

对于日期时间和时间字段 , 确切的第二个匹配 , 允许链接附加字段查询

```python
Event.objects.filter(timestamp__second=31)
Event.objects.filter(time__second=2)
Event.objects.filter(timestamp__second__gte=31)
# 等价SQL
SELECT ... WHERE EXTRACT('second' FROM timestamp) = '31';
SELECT ... WHERE EXTRACT('second' FROM time) = '2';
SELECT ... WHERE EXTRACT('second' FROM timestamp) >= '31';
```

### isnull

值为False或True , 相当于SQL语句IS NULL 和IS NOT NULL

```python
Entry.objects.filter(pub_date__isnull=True)
# 等价SQL
SELECT ... WHERE pub_date IS NULL;
```

### search

一个Boolean类型的全文搜索 , 以全文搜索的优势 ; 这个很像contains , 但是由于全文索引的优势 , 以使它更显著的块

```python
Entry.objects.filter(headline__search="+Django -jazz Python")
# 等价SQL
SELECT ... WHERE MATCH(tablename, headline) AGAINST (+Django -jazz Python IN BOOLEAN MODE);
```

### regex

区分大小写的正则表达式匹配

```sql
Entry.objects.get(title__regex=r'^(An?|The) +')
# 等价SQL
SELECT ... WHERE title REGEXP BINARY '^(An?|The) +'; -- MySQL
SELECT ... WHERE REGEXP_LIKE(title, '^(An?|The) +', 'c'); -- Oracle
SELECT ... WHERE title ~ '^(An?|The) +'; -- PostgreSQL
SELECT ... WHERE title REGEXP '^(An?|The) +'; -- SQLite
```

### iregex

不区分大小写的正则表达式匹配

```sql
Entry.objects.get(title__iregex=r'^(an?|the) +')
# 等价SQL
SELECT ... WHERE title REGEXP '^(an?|the) +'; -- MySQL
SELECT ... WHERE REGEXP_LIKE(title, '^(an?|the) +', 'i'); -- Oracle
SELECT ... WHERE title ~* '^(an?|the) +'; -- PostgreSQL
SELECT ... WHERE title REGEXP '(?i)^(an?|the) +'; -- SQLite
```

## 聚合函数

Django的`django.db.models` 模块提供以下聚合函数 , 关于如果使用这些聚合函数的细节 , 参考 [the topic guide on aggregation](https://docs.djangoproject.com/en/1.11/topics/db/aggregation/) , 如何创建聚合函数 , 参考 [`Aggregate`](https://docs.djangoproject.com/en/1.11/ref/models/expressions/#django.db.models.Aggregate) 

所有聚合函数都具有以下共同的参数 : 

### expression

引用模型字段的一个字符串 , 或者一个查询表达式

### output_field

用来表示返回的模型字段 , 它是一个可选的参数

## \*\*extra 

这些关键字参数可以给聚合函数生成的SQL提供额外的信息

### Avg

` class Avg(expression, output_field=FloatField(), **extra*) `  

返回给定表达式的平均值 , 它必须是数值 , 除非你指定不同的output_field

默认别名为 : `<filed>__avg`

返回类型 : float(或指定output_field的类型)

### Count

返回表达式相关的对象的个数

默认别名 :`<filed>__count`

返回类型 : int

有一个可选的参数 : distinct , 如果为True , Count将只计算唯一的实例 , 它等同于CONUT(DISTINCT < filed >) SQL语句 , 默认为False

### Max

`class Max(expression,output_field=None,**extra)`

返回expression 的最大值。

- 默认的别名 : `<field>__max`
- 返回类型 : 与输入字段的类型相同 , 如果提供则为 `output_field` 类型

### Min

`class Min(expression,output_field=None, **extra) `

返回expression 的最小值

- 默认的别名 : `<field>__min`
- 返回类型 : 与输入字段的类型相同 , 如果提供则为 `output_field` 类型

### StdDev

`class StdDev(expression, sample=False, **extra)` 

返回expression 的标准差

- 默认的别名 : `<field>__stddev`
- 返回类型 : `float`

有一个可选的参数 : sample , 默认情况下 , StdDev 返回群体的标准差 ;  但是 , 如果`sample=True` , 返回的值将是样本的标准差

### Sum

`class Sum(expression, output_field=None, **extra)` 

计算expression 的所有值的和。

- 默认的别名 : `<field>__sum`
- 返回类型 : 与输入字段的类型相同 , 如果提供则为 `output_field` 类型

### Variance

`class Variance(expression,sample=False, **extra*)` 

返回expression 的方差。

- 默认的别名 : `<field>__variance`
- 返回类型 : `float`

有一个可选的参数 : sample , 默认情况下 , `Variance` 返回群体的方差 ;  但是 , 如果`sample=True` , 返回的值将是样本的方差

**在QuerySet API中还有几个查询相关的工具 :**

- Q() 对象
- Prefetch() 对象
- prefetch_related_objects()

详细内容见 : [Query-related tools](https://docs.djangoproject.com/en/1.11/ref/models/querysets/#query-related-tools)

更多QuerySet API 详细内容 : https://docs.djangoproject.com/en/1.11/ref/models/querysets/
