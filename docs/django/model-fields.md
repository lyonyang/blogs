# Django - Model Fields








<extoc></extoc>

## 介绍

对于一个模型来说 , 最重要的和不可或缺的是列出该模型在数据库中定义的字段

字段由属性指定 , 但是选择的字段名称不要和[models API](https://docs.djangoproject.com/en/1.11/ref/models/instances/) 冲突 , 比如 save , clean 或者 delete , 如下 : 

```python
from django.db import models

class Musician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    instrument = models.CharField(max_length=100)

class Album(models.Model):
    artist = models.ForeignKey(Musician, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    num_stars = models.IntegerField()
```

## 字段类型

模型中的每个字段都是 [`Field`](https://docs.djangoproject.com/en/1.11/ref/models/fields/#django.db.models.Field) 子类的某个实例 , Djnaog根据字段的类型确定以下信息 : 

- 列类型 , 它告知数据库要存储哪种数据 (如 , INTEGER , VARCHAR , TEXT)
- 渲染表单时使用的默认HTML  [widget](https://docs.djangoproject.com/en/1.11/ref/forms/widgets/) , 例如 : ` <input type="text">, <select>).` 即使用select小部件
- 最低限度的验证需求 , 它被用在Django管理站点和自动生成的表单中

Django拥有数十种内置的字段类型 ; 你可以在 [model field reference](https://docs.djangoproject.com/en/1.11/ref/models/fields/#model-field-types) 中找到完整列表 , 如果Django内置的字段不能满足我们的要求 , 那么我们可以进行自定义模型字段 : [Writing custom model fields](https://docs.djangoproject.com/en/1.11/howto/custom-model-fields/)

## 字段选项

每个字段都接受一组与字段有关的参数 , 例如 , `CharField` (和它的派生类) 需要`max_length` 参数来指定`VARCHAR` 数据库字段的大小

而对于所有的字段类型 , 都有一组通用的参数可供使用 , 以下介绍一些最常用的 : 

| 参数          | 说明                                       |
| ----------- | ---------------------------------------- |
| null        | 如果为True , Django将会把数据库中的空值保存为NULL ; 默认为False |
| blank       | 如果为True , 该字段允许为空值 ; 默认为False            |
| choices     | 一个二元组组成的可迭代对象 (list或tuple) , 用来给字段提供选择项 ; 如果设置了choices , 默认的表单将是一个选择框而不是标准的文本框 , 而且这个选择框的选项就是choices中的选项<br />choices实例见表格补充 |
| default     | 默认值 , 可以是一个值或可调用对象 , 如果是可调用对象 , 那么每个新对象被创建它都会被调用 |
| help_text   | 表单部件额外显示的帮助内容 , 即使字段不在表单中使用 , 它对生成文档也很有用 |
| primary_key | 如果为True , 那么这个字段就是模型的主键<br />如果没有指定任何一个字段的`primary_key=True` , Django就会自动添加一个IntegerField字段作为主键 , 也就是字段 `id`<br />主键字段是只读的 , 如果你在一个已存在的对象上面更改主键的值并且保存 , 那么就会在原有对象之外创建出一个新的对象 |
| unique      | 如果True , 则这个字段在整张表中必须是唯一的                |

**表格补充 :** 

choices实例

```python
YEAR_IN_SCHOOL_CHOICES = (
    ('FR', 'Freshman'),
    ('SO', 'Sophomore'),
    ('JR', 'Junior'),
    ('SR', 'Senior'),
    ('GR', 'Graduate'),
)
'''
元组中的第一个元素是将被存储在数据库中的值,第二个元素将由默认窗体小部件或ModelChoiceField显示
给定一个模型实例,可以使用get_FOO_display()方法来访问选项字段的显示值
'''
```

访问选项字段的显示值 

```python
from django.db import models

class Person(models.Model):
    SHIRT_SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )
    name = models.CharField(max_length=60)
    shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)
```

```python
# 创建Person对象
>>> p = Person(name="Fred Flintstone", shirt_size="L")
# 保存到数据库
>>> p.save()
# 查看shirt_size属性
>>> p.shirt_size
'L'
# 查看shirt_size显示值
>>> p.get_shirt_size_display()
'Large'
```

注 : 上述仅仅对最常见的字段选项进行说明 , 完整查看 [common model field option reference](https://docs.djangoproject.com/en/1.11/ref/models/fields/#common-model-field-options)

## 自增主键字段

默认 , Django给了每个模型一个主键字段 : 

```python
id = models.AutoField(primary_key=True)
```

这是一个自增主键

当我们想指定一个自定义主键字段时 , 只需要在某个字段上指定`primary_key=True` 即可 , 因为Django看到你显示地设置了`Field.primary_key` 就不会自动添加`id` 列

每个模型只能有一个字段指定`primary_key=True` 

## 字段的自述名

除了`ForeignKey` , `ManyToManyField` 和 `OneToOneField` 之外 , 每个字段类型都接受一个可选的位置参数 , 即字段的自述名 (在第一的位置) ; 如果没有给定自述名 , Django将根据字段的属性名称自动创建自述名 , 即将属性名称的下划线替换成空格

实例

```python
# 自述名为person's first name
first_name = models.CharField("person's first name", max_length=30)
# 自述名为first name
first_name = models.CharField(max_length=30)
```

`ForeignKey` , `ManyToManyField` 和`OneToOneField`都要求第一个参数是一个模型类 , 所以要使用`verbose_name` 关键字参数才能指定自述名 : 

```python
poll = models.ForeignKey(
    Poll,
    on_delete=models.CASCADE,
    verbose_name="the related poll",
)
sites = models.ManyToManyField(Site, verbose_name="list of sites")
place = models.OneToOneField(
    Place,
    on_delete=models.CASCADE,
    verbose_name="related place",
)
```

习惯上 , `verbose_name` 的首字母不用大写 , Djnaog在必要的时候会自动大写首字母

## 数据库关系

关系型数据库的威力体现在表之间的相互关联 , 而Django提供了三种最常见的数据库关系 : 

- 多对一 , many - to - one
- 多对多 , many - to - many
- 一对一 , ont - to - one

### 多对一

Django使用`django.db.models.ForeignKey` 定义多对以关系 

和使用其它字段类型一样 , 在模型当中把它作为一个类属性使用

```python
class ForeignKey(to, on_delete, **options):
    """
    ForeignKey需要两个位置参数,模型相关联的类和on_delete选项
    更多详细内容:https://docs.djangoproject.com/en/1.11/ref/models/fields/#foreignkey
    """
```

实例

```python
from django.db import models
# 制造商可以生产很多汽车
class Manufacturer(models.Model):
    # ...
    pass
# 每一辆汽车只能有一个制造商
class Car(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    # ...
```

若要创建递归关联关系 , 即具有多对一关系的对象需要使用 `models.ForeignKey('self' , on_delete=models.CASCADE)` 

如果需要在尚未定义的模型上创建关系 , 可以使用模型的名称 , 而不是模型对象本身 :

```python
from django.db import models

class Car(models.Model):
    manufacturer = models.ForeignKey(
        'Manufacturer',
        on_delete=models.CASCADE,
    )
    # ...

class Manufacturer(models.Model):
    # ...
    pass
# 更多说明:https://docs.djangoproject.com/en/1.11/ref/models/fields/#ref-foreignkey
```

ForeignKey字段还接受许多别的参数  , 更多 : [the model field reference](https://docs.djangoproject.com/en/1.11/ref/models/fields/#foreign-key-arguments)

多对一更多示例 : [Many-to-one relationship model example](https://docs.djangoproject.com/en/1.11/topics/db/examples/many_to_one/)

### 多对多

`ManyToManyField` 字段是用来定义多对多关系的 , 同使用其他字段类型一样

```python
class ManyToManyField(to, **options):
    """
    多对多关系,需要一个位置参数:模型相关联的类
    它与ForeignKey的工作方式完全相同,包括递归和延迟(未定义)关系
    """
```

实例

```python
from django.db import models
# 一种装饰可以在多个Pizza上
class Topping(models.Model):
    # ...
    pass
# 一个Pizza上可以有多种装饰
class Pizza(models.Model):
    # ...
    toppings = models.ManyToManyField(Topping)
```

官方文档中建议以被关联模型名称的复数形式作为`ManyToManyField` 的名字 , 如上实例中为`toppings` 

对于多对多关系 , 在哪个模型中设置`ManyToManyField` 都可以 , 但是不要两个模型都设置

完整示例 : [Many-to-many relationship model example](https://docs.djangoproject.com/en/1.11/topics/db/examples/many_to_many/) 

### 中介模型

对与上一节中Pizza和Topping搭配这样简单的多对多关系时 , 使用标准的`ManyToManyField` 就可以了 , 但是有时我们可能需要关联数据到两个模型之间的上

例如 , 有这样一个应用 , 它记录音乐家所属的音乐小组 , 我们可以用一个`ManyToManyField` 表示小组和成员之间的多对多关系 , 但是 , 有时你可能想知道更多成员关系的细节 , 比如成员是何时加入小组的 , 对于这些情况 , Django允许你指定一个*中介模型* 来定义多对多关系 , 你可以将其他字段放在中介模型里面

源模型的`ManyToManyField` 字段将使用through参数指向中介模型 , 实例 : 

```python
from django.db import models
# 音乐家,目标模型
class Person(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):              # __unicode__ on Python 2
        return self.name
# 音乐小组,源模型
class Group(models.Model):
    name = models.CharField(max_length=128)
    # 通过through参数指向中介模型Membership
    members = models.ManyToManyField(Person, through='Membership')

    def __str__(self):              # __unicode__ on Python 2
        return self.name
# 中介模型
class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)
```

中介模型的一些限制 : 

- 中介模型必须有且只有一个外键到源模型 , 或者必须使用`ManyToManyField.through_fields` 显示指定Django应该在关系中使用的外键 ; 如果你的模型中存在不止一个外键 , 并且`through_fields` 没有指定 , 将会触发一个无效的错误 . 对目标模型的外键有相同的限制(Person)
- 对于通过中介模型与自己进行多对多关联的模型 , 允许存在到同一个模型有两个外键 , 但他们将被当做多对多关联中一个关系的两边 ; 如果有超过两个外键 , 同样你必须像上面一样指定`through_fields`  , 否则将引发一个验证错误
- 使用中介模型定义与自身的多对多关系时 , 你必须设置`symmetrical=False` , 详细见[the model field reference](https://docs.djangoproject.com/en/1.11/ref/models/fields/#manytomany-arguments)

设置好中介模型(Membership)后 , 接下来要开始创建多对多关系 , 首先创建中介模型的实例 : 

```python
>>> ringo = Person.objects.create(name="Ringo Starr")
>>> paul = Person.objects.create(name="Paul McCartney")
>>> beatles = Group.objects.create(name="The Beatles")
>>> m1 = Membership(person=ringo, group=beatles,
...     date_joined=date(1962, 8, 16),
...     invite_reason="Needed a new drummer.")
>>> m1.save()
>>> beatles.members.all()
<QuerySet [<Person: Ringo Starr>]>
>>> ringo.group_set.all()
<QuerySet [<Group: The Beatles>]>
>>> m2 = Membership.objects.create(person=paul, group=beatles,
...     date_joined=date(1960, 8, 1),
...     invite_reason="Wanted to form a band.")
>>> beatles.members.all()
<QuerySet [<Person: Ringo Starr>, <Person: Paul McCartney>]>
```

与普通的多对多字段不同 , 不能使用add() , create() 和 set() 来建立关系 : 

```python
>>> # The following statements will not work
>>> beatles.members.add(john)
>>> beatles.members.create(name="George Harrison")
>>> beatles.members.set([john, paul, ringo, george])
```

因为你不能只创建`Membership` 和`Group` 之间的关联关系 , 你还要指定Person模型中所需要的所有信息 , 而简单的add() , create() 和复制语句是做不到这一点的 ; 所以它们不能在使用中介模型的多对多关系中使用 , 唯一的办法就是创建中介实例

同上remove() 也被禁用 , 但是clear()方法是可以用的 , 因为它会清空某个实例所有的多对多关系

```python
>>> # Beatles have broken up
>>> beatles.members.clear()
>>> # Note that this deletes the intermediate model instances
>>> Membership.objects.all()
```

建立好关系之后 , 就可以执行查询了

```python
'''直接使用被关联模型的属性进行查询'''
# Find all the groups with a member whose name starts with 'Paul'
>>> Group.objects.filter(members__name__startswith='Paul')
<QuerySet [<Group: The Beatles>]>
'''利用中介模型的属性进行查询'''
# Find all the members of the Beatles that joined after 1 Jan 1961
>>> Person.objects.filter(
...     group__name='The Beatles',
...     membership__date_joined__gt=date(1961,1,1))
<QuerySet [<Person: Ringo Starr]>
'''直接获取Membership模型'''
>>> ringos_membership = Membership.objects.get(group=beatles, person=ringo)
>>> ringos_membership.date_joined
datetime.date(1962, 8, 16)
>>> ringos_membership.invite_reason
'Needed a new drummer.'
'''还有一种方法是在Person对象查询多对多反向关系'''
# 详细见https://docs.djangoproject.com/en/1.11/topics/db/queries/#m2m-reverse-relationships
>>> ringos_membership = ringo.membership_set.get(group=beatles)
>>> ringos_membership.date_joined
datetime.date(1962, 8, 16)
>>> ringos_membership.invite_reason
'Needed a new drummer.'
```

### 一对一

`OneToOneField` 用来定义一对一关系 , 和使用其它字段类型一样

当某个对象想扩展自另一个对象时 , 最常用的方式就是这个对象的主键上添加一对一关系

```python
class OneToOneField(to, on_delete, parent_link=False, **options):
    """
    OneToOneField和ForeignKey以及ManyToManyField一样
    它有两个位置参数:相关联的类以及on_delete选项
    parent_link:该参数为True且使用从另一个具体模型继承的模型时,表明该字段应该作为返回到父类的链接,而
    而不是通常由子类隐式创建的额外的OneToOneField
    """
```

如果你正在建立一个"places" 的数据库 , 那么你将建立一个非常标准的地址 , 电话号码等 , 在数据库中; 接下来 , 如果你想在places数据库的基础上建立一个restaurant数据库 , 而不想将已有的字段复制到Restaurant模型 , 那么你可以在Restaurant添加一个OneToOneField字段 , 这个字段指向Place (因为Restaurant本身就是一个Place) , 事实上 , 在处理这个问题时 , 我们应该使用一个典型的[inheritance](https://docs.djangoproject.com/en/1.11/topics/db/models/#model-inheritance) , 因为它隐含一个一对一关系

示例 : https://docs.djangoproject.com/en/1.11/topics/db/examples/one_to_one/

与ForeignKey一样 , 可以定义 [recursive relationship](https://docs.djangoproject.com/en/1.11/ref/models/fields/#recursive-relationships) 和  [references to as-yet undefined models](https://docs.djangoproject.com/en/1.11/ref/models/fields/#lazy-relationships)

## Meta选项

使用内部的`class Meta` 可以定义模型的元数据 , 如下 : 

```python
from django.db import models

class Ox(models.Model):
    horn_length = models.IntegerField()

    class Meta:
        ordering = ["horn_length"]
        verbose_name_plural = "oxen"
```

模型元数据是任何不是字段的数据 , 比如排序选项 (ordering) , 数据库表名 (db_table) 或者可读的单复数名称 (verbose_name和verbose_name_plural)

所有Meta选项的完整列表见 : [model option reference](https://docs.djangoproject.com/en/1.11/ref/models/options/)

更多相关内容 : https://docs.djangoproject.com/en/1.11/topics/db/models/

