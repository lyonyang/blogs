# ORM简介


<extoc></extoc>

## 介绍  🍀

ORM在开发者和数据库之间建立了一个中间层 , 把数据库中的数据转换成了 Python 中的对象实体 , 这样既屏蔽了不同数据库之间的差异性 , 又使开发者可以非常方便地操作数据库中的数据 , 而且可以使用面向对象的高级特性

ORM 为我们做了如下操作 : 

- 将调用转换成 SQL 语句
- 通过数据库引擎发送给数据库执行
- 将数据库返回的结果记录用 ORM 映射技术转换成类对象

ORM 优点 :

- 向开发者屏蔽了数据库的细节 , 使开发者无需与 SQL 语句打交道 , 提高了开发小懒虫
- 便于数据库迁移 , 由于每种数据库的 SQL 语法有细微差别 , 所以基于 SQL 的数据访问层在更换数据库时通常需要花费大量的时间调试 SQL 语句 , 而 ORM 提供了独立于 SQL 的接口 , ORM 引擎会处理不同数据库之间的差异 , 所以迁移数据库时无须更改代码
- 应用缓存优化等技术有时可以提高数据库操作的效率

## Python ORM 库介绍  🍀

Python 中提供 ORM 支持的组件有很多 , 每个组件的应用领域稍有区别 , 但是数据库操作的理论原理是相同的 , 下面对比较著名的 Python 数据库的 ORM 框架介绍 : 

- SQLAlchemy : 是 Python 中最成熟的 ORM 框架 , 资源和文档都很丰富 , 大多数 Python Web 框架对其都有很好的支持 , 能够胜任大多数应用场合 ; SQLAlchemy 被认为是 Python 事实上的 ORM 标准
- Django ORM : 是 Python 世界中大名鼎鼎的 Django Web 框架独用的 ORM 技术 , Django是一个大而全的框架 , 这使得其灵活性大大降低 , 其他 Python Web 框架可以随意更换 ORM , 但在 Django 中不能这样做 , 因为 Django 内置的很多 model 是用 Django 内置 ORM 实现的
- Peewee : 小巧灵活 , 是一个轻量级的 ORM , Peewee 是基于 SQLAlchemy 内核开发的 , 整个框架只由一个文件构成 , Peewee 提供了对多种数据库的访问方式 , 如 SQLite , MySQL , PostgreSQL , 适用于功能简单的小型网站
- Storm : 是一个中型的 ORM 库 ,比 SQLAlchemy 和 Django 等轻量 , 比 Peewee 的功能更丰富 , Storm 要求开发者编写数据表的 DDL 代码 , 而不能直接从数据表类定义中自动生成表定义
- SQLObject : 与 SQLAlchemy 相似 , 也是一套大而全的 ORM , SQLObject 的特点是其设计借鉴了 Ruby on Rails 的 ActiveRecord 模型 , 是的熟悉 Ruby 的开发者上手非常容易

## Peewee库使用  🍀

示例 : 

```python
# 引入Peewee包的所有内容
from peewee import *

# 建立一个SQLite数据库引擎对象,该引擎打开数据库文件sampleDB.db
db = SqliteDatabase("sampleDB.db")

# 定义一个ORM的基类,在基类中指定本ORM所使用的数据库
# 这样在之后所有的子类中就不用重复声明数据库了
class BaseModel(Model):
    class Meta:
        database = db
  
# 定义course表,继承自BaseModel
class Course(BaseModel):
    id = PrimaryKeyField()
    title = CharField(null=false)
    period = IntegerField()
    description = CharField()
    
    class Meta:
        order_by = ('title',)
        db_table = 'course'
        
# 定义teacher表,继承自BaseModel
class Teacher(BaseModel):
    id = PrimaryKeyField()
    name = CharField(null=false)
    gender = BooleanField()
    description = CharField()
    course_id = ForeignKeyField(Course, to_field="id", related_name="course")
    
    class Meta:
        order_by = ('name',)
        db_table = 'course'
```

使用 ORM 映射对数据内容进行增 , 删 , 改 , 查 : 

```python
# 建表,进需创建一次
Course.create_table()
Teacher.craete_table()

# 新增行
Course.create(id=1, title='经济学', period=320, description='文理科学生均可选修')
Teacher.create(name='Lyon', gender=True, address='...', course_id=1)

# 查询一行
record = Course.get(Course.title='经济学')
print("课程:%s, 学时:%d" % (record.titel, record.period))

# 更新
record.period = 200
record.save()

# 删除
record.delete_instance()

# 查询所有记录
courses = Course.select()

# 带条件查询,并将结果按period字段倒序排序
courses = Course.select().where(Course.id<10).order_by(Course.period.desc())

# 统计所有课程的平均学时
total = Course.select(fn.Avg(Course.period).alias('avg_period'))

# 更新多个记录
Course.update(period=300).where(Course.id>100).execute()

# 多表连接操作,Peewee会自动根据ForeignKeyField的外键定义进行连接
Record = Course.select().join(Teacher).where(Teacher.gender=True)
```