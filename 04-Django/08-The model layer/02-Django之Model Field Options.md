# Python之路 - Django之Model Field Options

## 介绍  🍀

本篇文章为"工具"笔记 , 适合用于翻阅查找 , 对于字段元选项的总结

以下字段选项对于所有字段类型都是可选的

## null  🍀

**说明**

如果为 `True` , 则Django将在数据库中将空值存储为`NULL`  , 也意味着该字段可填可不填 , 默认为 `False` 

**示例**

```python
class Student(models.Model):
    name = models.CharField(null=True)
```

**特别的 :** 

- 应该避免在基于字符串的字段中字段中使用 `null=True` , 例 :  `CharField` 和 `TextField` ; 因为空字符串值会存储为空字符串而不是NULL , 而如果使用该选项 , 则意味着 "无数据" 可能有两种状态 , `NULL` 和空字符串 , 并且在大多数情况下 , Django中惯例使用空字符串而不是 `NULL`
- 如果在 `CharField` 中同时拥有两个选项 , `unique=True` 与 `blank=True` , 那么需要设置 `null=True` 来防止在保存多个空白值 (`blank=True`的结果)时违反 `unique=True` 唯一约束
- `null` 选项是纯粹的数据库范畴 , 针对数据库的选项 , 即数据库中 , 数据是否能为空值

*如果我们需要在`BooleanField` 字段中设置 `null` , 我们应该使用 `NullBooleanField` 字段来代替*

## blank  🍀

**说明**

与上面的 `null` 不同 , `blank` 针对的是数据验证的范畴 , 如在使用 `admin` 录入数据时 , 默认不允许输入空值 , 通过设置 `blank=True` 即可输入空值 

在设计表时 , 如果仅设置 `null=True`  , 那么在使用 `admin` 录入数据时 , 是不可输入空值的

**示例**

```python
class Student(models.Model):
    name = models.CharField(blank=True)
```

## choices  🍀

**说明**

设置 `choices` 后 , 该字段就为一个选择框 (设置 `max_length` 选项指定可选数) , 设置值为一个可迭代的结构 , 如上示例中 : 每个元组中的第一个元素 , 是存储在数据库中的值 ; 第二个元素是该选项的描述值

**示例**

```python
class Student(models.Model):
    YEAR_IN_SCHOOL_CHOICES = (
        ('FR', 'Freshman'),
        ('SO', 'Sophomore'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
    )
    # default为默认选择项
    year_in_school = models.CharField(max_length=2,
                                      choices=YEAR_IN_SCHOOL_CHOICES,
                                      default='FR')
```

除了单层的二元元组 , 还可以设置成多成二元元组 : 

```python
MEDIA_CHOICES = (
    ('Audio', (
            ('vinyl', 'Vinyl'),
            ('cd', 'CD'),
        )
    ),
    ('Video', (
            ('vhs', 'VHS Tape'),
            ('dvd', 'DVD'),
        )
    ),
    ('unknown', 'Unknown'),
)
```

同样的 , 第一个元素为组的名字 , 第二个元素为描述值 , 并且每个二元元组的第一个元素是不可选的 , 可选选项为最里层的二元元组的第二个元素 , 例如 : 'Vinyl' , 'CD'

Django中 , 对于每一个选择框 , 都有一个 `get_fieldname_display()` 方法以获取描述值 (二元元组的第二个元素) , 如下 : 

```python
>>> stu = Student(year_in_school="FR")
>>> stu.save()
>>> stu.year_in_school
'FR'
>>> stu.get_year_in_school_display()
'Freshman'
```

**PS :** 如果不指定默认选项 , 那么选择菜单默认为 "-----------" , 如果我们要进行重写 , 只需在元组添加一项包含None的元组到 `choices` 中 , 如 : `(None, 'Your Choices')`

## db_column  🍀

**说明**

指定在数据库中的字段名 , 默认使用 `Field` 名 (即示例中的 `name` )

**示例**

```python
class Student(models.Model):
    name = models.CharField(max_length=32, db_column="姓名")
    
# 数据库表
+----+---------+
| id | 姓名    |
+----+---------+
|  1 | lyon    |
+----+---------+
```

## db_index  🍀

**说明**

为字段创建索引 , 默认为 `False` , 设置为 `True` Django会为该字段创建数据库索引

**示例**

```python
class Student(models.Model):
    name = models.CharField(max_length=32, db_index=True)
```

## db_tablespace  🍀

***待整理***

## default  🍀

**说明**

设置字段的默认值 , 该值可为一个值或一个可调用对象 , 但是不可为可变对象 (dict , list , ...) ; 如果为一个可调用对象 , 那么每次创建实例时都会被调用一次

**示例**

```python
def contact_default():
    return {"email": "to1@example.com"}

class Student(models.Model):
    name = models.CharField(max_length=32, default="未知")
	# 默认值为可调用对象
	contact_info = JSONField("ContactInfo", default=contact_default)
```

**PS :** 可调用对象不可使用 `lambdas` 函数 , 因为这类参数无法被 `migrations` 命令进行序列化

## editable  🍀

**说明**

默认为 `True` , 如果设置为 `False`  , 那么这个字段将不会出现 `admin` (本质使用了ModelForm) 或者其他 `ModelForm` 中

**示例**

```python
class Student(models.Model):
    role = models.CharField(max_length=32, editable=False)
```

## error_messages  🍀

**说明**

指定 `error_messages` 选项可以更改该字段将引发的默认错误信息 , `error_messages` 为一个字典 , 其中 key 包括 : null , blank , invalid , invalid_choice , unique 以及 unique_for_data (Django 1.7以上版本后添加)

**示例**

```python
class Student(models.Model):
    name = models.CharField(max_length=32, db_column="姓名", 	error_messages={
            'null':"不能为空",
        })
```

它们的默认错误信息如下 : 

```python
default_error_messages = {
        'invalid_choice': _('Value %(value)r is not a valid choice.'),
        'null': _('This field cannot be null.'),
        'blank': _('This field cannot be blank.'),
        'unique': _('%(model_name)s with this %(field_label)s '
                    'already exists.'),
        # Translators: The 'lookup_type' is one of 'date', 'year' or 'month'.
        # Eg: "Title must be unique for pub_date year"
        'unique_for_date': _("%(field_label)s must be unique for "
                             "%(date_field_label)s %(lookup_type)s."),
    	# 特殊的,在Field的派生类中定义,以DateField为例
    	'invalid': "'%(value)s' value has an invalid date format. It must be "
                     "in YYYY-MM-DD format."
    }
```

## help_text  🍀

**说明**

该选项会在表单控件form中 , 添加一些文档 , 文档会出现在 `input` 框下方

**示例**

```python
class Student(models.Model):
    name = models.CharField(max_length=32, help_text='这里填名字')
```

**PS :** 默认会对文档进行HTML转换 , 所以为了避免任何HTML特定的字符 , 我们可以使用简单文本或 `django.utils.html.escape()` 进行转换 , 以防止用户进行的跨站点脚本攻击

## primary_key  🍀

**说明**

指定该字段为主键 , 默认情况下 , 如果在model中没有指定 `primary_key=True` , Django会自动添加一个 `AutoField` 来作为主键 , 即默认创建的 `id` 字段

**示例**

```python
class Student(models.Model):
    sid = models.AutoField(primary_key=True)
```

**PS :** 主键字段是只读的 , 如果你更改现有对象的主键的值 , 然后将其保存 , 该结果并不是更改原对象的值 , 而是创建一个新对象

## unique  🍀

**说明**

唯一约束 , 如果为True , 该字段在表中必须是唯一的

**示例**

```python
class Student(models.Model):
    name = models.CharField(max_length=32, unique=True)
```

**PS :** 这个选项同 `null` 一样 , 是一个在数据库级别与Form验证级别的强制性动作 ; 该选项对于 `ManyToManyField` 和 `OneToOneField` 是无效的

只要设置 `unique=True` , 意味着创建唯一索引 , 所以不需要再次指定 `db_index` 选项

版本区别 : 在Django 1.11 中 , 为了版本支持 , `unique=True` 不可以使用 `FileField` 

## unique_for_date  🍀

**说明**

用于设置时间相关字段的值唯一 , 即针对 `DateField` 和 `DateTimeField` 字段

**示例**

```python
class Student(models.Model):
    opening_date = models.DateField(unique_for_date=True)
```

**PS :** 该选项是在Form验证期间通过 `Model.validate_unique()` 强制执行的 , 而不是在数据库级别进行的 , 所以这就意味着 , 如果字段中有 `editable=True`  , 那么 `Model.validate_unique()` 将忽略该约束

## unique_for_month  🍀

类似于 `unique_for_date` , 只是要求字段对于月份是唯一的

## unique_for_year  🍀

类似于 `unique_for_date` , 只是要求字段对于年份是唯一的

## verbose_name  🍀

**说明**

为字段设置一个可读性更高的名称 , 如果未设置该选项 , 那么Django在Form中默认会使用字段名 , 并会将字段名中的 "_" 转换成空格显示以及自动首字母大写

**示例**

```python
class Student(models.Model):
    name = models.CharField(max_length=32, verbose_name="学生姓名")
```

## validators  🍀

**说明**

可以自定制验证器 , 即验证值是否符合要求 , 它的值为一个列表 , 列表中为可调用对象

**示例**

```python
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(
            _('%(value)s is not an even number'),
            params={'value': value},
        )
        
        
from django.db import models

class MyModel(models.Model):
    even_field = models.IntegerField(validators=[validate_even])
```

除了我们自定制之外 , Django为我们提供了很多的内置验证器 , 我们可从 `django.core.validators` 中进行导入

本文参考 : https://docs.djangoproject.com/en/1.11/ref/models/fields