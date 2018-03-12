# Python之路 - 第三方库之SQlAlchemy

## 介绍  🍀

在介绍SQLAlchemy之前先介绍一下什么是ORM

**ORM** 

ORM即`Object Relational Mapping` , 简称ORM , 中文意思就是对象关系映射 ; 是一种程序技术 , 用于实现面向对象编程语言里不同类型系统的数据之间的转换

换一个方式介绍 , 我们知道面向对象是从**软件工程基本原则**(如耦合 , 聚合 , 封装) 的基础上发展起来的 , 而关系型数据库是从**数学理论**发展而来的 , 两套理论完全是不匹配的 , 那么正是为了解决这个问题 , 对象关系映射技术诞生了

**SQLAlchemy** 

SQLAlchemy是Python中最有名的一款ORM框架 , 该框架建立在数据库API之上 , 使用关系对象映射进行数据库操作

SQLAlchemy对象关系映射代表了用户使用Python定义类来与数据库中的表相关联的一种方式 , 类的实例则对应数据表中的一行数据 , SQLAlchemy包括了一套将对象中的变化同步到数据库表中的系统 , 这套系统被称之为工作单元(unit of work) , 同时也提供了使用类查询来实现数据库查询以及查询表之间关系的功能

**安装** 

```cmd
$ pip3 install SQLAlchemy
```

**版本检查**

```python
>>>import sqlalchemy
>>>sqlalchemy.__version__
'1.1.14'
```

**各数据库方言(Dialect)**

```mysql
MySQL-Python
    mysql+mysqldb://<user>:<password>@<host>[:<port>]/<dbname>
pymysql
    mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]
MySQL-Connector
    mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>
cx_Oracle
    oracle+cx_oracle://user:pass@host:port/dbname[?key=value&key=value...]
-- 更多详见：http://docs.sqlalchemy.org/en/latest/dialects/index.html
```

**内部处理**

SQLAlchemy操作数据库是利用Engine/ConnectionPooling/Dialect进行的 , Engine(引擎)使用ConnectionPooling连接数据库 , 然后再通过Dialect执行SQL语句 , SQLAlchemy Core如下

```
SQLAlchemy Core
+-----------------+  +-------------------------+  +-----------------+
|  Schema/Types   |  | SQL Expression Language |  |      Engine     |
+-----------------+  +-------------------------+  +-----------------+
                                                           ↓
									   +------------------+ +-------+
									   |Connection Pooling| |Dialect|
									   +------------------+ +-------+
---------------------------------------------------------------------
							DBAPI
```

## 连接数据库  🍀

```python
from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://root:myroot@localhost:3306/t1", echo=True)
```

`echo`参数是用来设置SQLAlchemy日志的 , 通过Python标准库logging模块实现 ; 设置为True表示所有操作记录可见 , 也可设置为False来减少日志的输出

`create_engine()` 的返回值是`Engine`的一个实例 , 此实例代表了操作数据库的核心接口 , 通过Dialect来处理数据库和数据库的API

PS : 初次调用`create_engine()`时并不会真正的去连接数据库 , 只有在真正执行一条命令的时候才会去简历真正的DBAPI连接 ; 很多地方都会使用这种方式 , 以达到省资源的目的

## 声明映射  🍀

当使用ORM的时候 , 配置过程以描述数据库的表来开始 , 然后定义与之匹配的类 ; 而在SQLAlchemy中 , 这两个过程一般结合在一起 , 通过一个声明(Declarative)系统实现 , 该系统帮我们定义类以及实现与表的对应

声明系统实现类与表的对应是通过一系列基类实现的 , 即声明基类(Declarative Base Class) , 我们的应用程序经常只有一个此基类的实例

```python
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
```

根据声明的基类"Base" , 我们就可以通过它定义任何数量的映射类

## ORM功能使用  🍀

流程如下 : 

1. 使用者通过ORM对象提交命令
2. 将命令给SQLAlchemy Core转换成SQL
3. 匹配使用者事先配置好的engine
4. engine从连接池中取出一个链接
5. 基于该链接通过Dialect调用DBAPI , 将SQL转交给数据库去执行

### 创建表  🍀

```python
# 创建单表
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Index, UniqueConstraint
# 根据Dialet创建引擎,echo=True表示输出所有操作日志
engine = create_engine('mysql+pymysql://root:myroot@localhost:3306/test', echo=True) 
# 声明基类
Base = declarative_base()
# 定义映射类
class Userinfo(Base):
    # 表名
    __tablename__ = 'user_info'  
    # 设置主键自增列
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32))
    extra = Column(String(16))
    __table_args__ = (
        # 唯一索引,索引名为uix_id_name
    	UniqueConstraint('id', 'name', name='uix_id_name'),
        # 联合索引
        Index('ix_id_name', 'name', 'extra'),
    )
    # 定义格式
    def __repr__(self):
        return "<User(id='%s', name='%s')>" % (self.id, self.name)
# 初始化函数
def init_db():
    # 将所有继承Base类的类,创建表结构
    Base.metadata.create_all(engine)
def drop_db():
    # 将所有继承Base类的类,删除表
    Base.metadata.drop_all(engine)
init_db()
```

对应的SQL语句

```mysql
CREATE TABLE `UserInfo` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	name VARCHAR(32), 
	extra VARCHAR(16), 
	PRIMARY KEY (id), 
	CONSTRAINT uix_id_name UNIQUE (id, name)
)
```

创建其他表

```python
# 创建单表:业务线
class Business(Base):
    __tablename__='business'
    id=Column(Integer,primary_key=True,autoincrement=True)
    bname=Column(String(32),nullable=False,index=True)
# 一对多:多个服务可以属于一个业务线,多个业务线不能包含同一个服务
class Service(Base):
    __tablename__='service'
    id=Column(Integer,primary_key=True,autoincrement=True)
    sname=Column(String(32),nullable=False,index=True)
    ip=Column(String(15),nullable=False)
    port=Column(Integer,nullable=False)
    business_id=Column(Integer,ForeignKey('business.id'))
    __table_args__=(
        UniqueConstraint(ip,port,name='uix_ip_port'),
        Index('ix_id_sname',id,sname)
    )
# 一对一:一种角色只能管理一条业务线,一条业务线只能被一种角色管理
class Role(Base):
    __tablename__='role'
    id=Column(Integer,primary_key=True,autoincrement=True)
    rname=Column(String(32),nullable=False,index=True)
    priv=Column(String(64),nullable=False)
    business_id=Column(Integer,ForeignKey('business.id'),unique=True
# 多对多:多个用户可以是同一个role,多个role可以包含同一个用户
class Users(Base):
    __tablename__='users'
    id=Column(Integer,primary_key=True,autoincrement=True)
    uname=Column(String(32),nullable=False,index=True)
class Users2Role(Base):
    __tablename__='users2role'
    id=Column(Integer,primary_key=True,autoincrement=True)
    uid=Column(Integer,ForeignKey('users.id'))
    rid=Column(Integer,ForeignKey('role.id'))
    __table_args__=(
        UniqueConstraint(uid,rid,name='uix_uid_rid'),
    )
class Favor(Base):
    __tablename__ = 'favor'
    nid = Column(Integer, primary_key=True, autoincrement=True)
    caption = Column(String(50), default='red', unique=True)
class Person(Base):
    __tablename__ = 'person'
    nid = Column(Integer, primary_key=True, autoincrement=True)
    favor_id = Column(Integer, ForeignKey("favor.nid"))
'''
设置外键的另一种方式 ForeignKeyConstraint(['other_id'], ['othertable.other_id'])
'''
```

**扩展分析 :  根据流程可以发现 , 如果我们不依赖于SQLAlchemy的转换而自己写好sql语句 , 那么我们完全可以只用SQLAlchemy执行纯sql语句 , 即利用配置好的engine执行 , `engine.execute()`** 

### 删除表  🍀

```python
Base.metadata.drop_all(engine)  # 把所有继承Base类的类，删除表
```

### 操作表  🍀

ORM处理数据库的方式是通过Session来实现的 , 当我们需要与数据库进行对话时 , 就需要创建一个Session实例 : 

engine对象已经创建完成时

```python
from sqlalchemy.orm import sessionmaker
# 创建Session工厂,并连接engine
Session = sessionmaker(bind=engine)
# 创建Session实例
session = Session()
```

engine未创建时

```python
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
# 创建Session工厂
Session = sessionmaker()
# 创建引擎
engine = create_engine()
# 连接Session与engine
Session.configure(bind=engine)
# 创建Session实例
session = Session()
```

#### 增加数据  🍀

单条数据

```python
Session = sessionmaker(bind=engine)
session = Session()
# 创建一条数据
users = Userinfo(name='Hello', password='World')
# 把数据添加到表内
session.add(users)
# 提交生效
session.commit()
```

多条数据

```python
session.add_all([
    Userinfo(name='Lyon',extra='xxx'),
    Userinfo(name='Kenneth Reitz',extra='xxx'),
])
session.commit()
```

#### 删除数据  🍀

```python
session.query(Userinfo).filter(Userinfo.name == 'Kenneth Reitz').delete()
session.commit()
```

#### 修改数据  🍀

```python
session.query(Userinfo).filter(Users.id > 2).update({"name" : "099"})
# synchronize_session同步会话
session.query(Userinfo).filter(Users.id > 2).update({Users.name: Users.name + "099"}, synchronize_session=False)
# 设置评估标准
session.query(Userinfo).filter(Users.id > 2).update({"num": Users.num + 1}, synchronize_session="evaluate")
session.commit()
'''
更多synchronize_session的参数可以查看官方文档
'''
```

#### 查询数据  🍀

```python
# 查所有,取所有字段
res = session.query(Userinfo).all()
print(res)
# 查所有,取指定字段,按照id排序
res = session.query(Userinfo.name).order_by(Userinfo.id).all()
print(res)
# 查所有,取指定字段,第一条信息
res = session.query(Userinfo.name).first()
print(res)
# 过滤查,逗号分隔,默认为and
res = session.query(Userinfo).filter(Userinfo.id > 1,Userinfo.id <1000)
print([(row.id, row.name) for row in res], type(res))
'''
执行结果:
[<User(id='1', name='Lyon')>]
[('Lyon',)]
('Lyon',)
[] <class 'sqlalchemy.orm.query.Query'>
'''
```

#### 其他查询  🍀

```python
#　条件
ret = session.query(MyClass).filter_by(name = 'some name')
ret = session.query(MyClass).filter(MyClass.id > 1, MyClass.name == 'Lyon').all()
ret = session.query(MyClass).filter(MyClass.id.between(1, 3), MyClass.name == 'eric').all()
ret = session.query(MyClass).filter(MyClass.id.in_([1,2,3])).all()
ret = session.query(MyClass).filter(~MyClass.id.in_([1,2,3])).all()
ret = session.query(MyClass).filter(MyClass.id.in_(session.query(MyClass.id).filter_by(name='Lyon'))).all()
from sqlalchemy import and_, or_
ret = session.query(MyClass).filter(and_(MyClass.id > 3, MyClass.name == 'Lyon')).all()
ret = session.query(MyClass).filter(or_(MyClass.id < 2, MyClass.name == 'Lyon')).all()
ret = session.query(MyClass).filter(
    or_(
        MyClass.id < 2,
        and_(MyClass.name == 'eric', MyClass.id > 3),
        MyClass.extra != ""
    )).all()
# 通配符
ret = session.query(MyClass).filter(MyClass.name.like('e%')).all()
ret = session.query(MyClass).filter(~MyClass.name.like('e%')).all()
# 限制
ret = session.query(MyClass)[1:2]
# 排序
ret = session.query(MyClass).order_by(MyClass.name.desc()).all()
ret = session.query(MyClass).order_by(MyClass.name.desc(), MyClass.id.asc()).all()
# 分组
from sqlalchemy.sql import func
ret = session.query(MyClass).group_by(MyClass.extra).all()
ret = session.query(
    func.max(MyClass.id),
    func.sum(MyClass.id),
    func.min(MyClass.id)).group_by(MyClass.name).all()
ret = session.query(
    func.max(MyClass.id),
    func.sum(MyClass.id),
    func.min(MyClass.id)).group_by(MyClass.name).having(func.min(MyClass.id) >2).all()
# 连表
ret = session.query(Users, Favor).filter(Users.id == Favor.nid).all()
ret = session.query(Person).join(Favor).all()
ret = session.query(Person).join(Favor, isouter=True).all()
# 组合
q1 = session.query(MyClass.name).filter(MyClass.id > 2)
q2 = session.query(Favor.caption).filter(Favor.nid < 2)
ret = q1.union(q2).all()
q1 = session.query(MyClass.name).filter(MyClass.id > 2)
q2 = session.query(Favor.caption).filter(Favor.nid < 2)
ret = q1.union_all(q2).all()
```