# Python之路 - 第三方库之MySQLdb

## 介绍  🍀

MySQLdb是用于Python链接MySQL数据库的接口 , 它实现了Python数据库API规范V2.0 , 基于MySQL C API 上建立的

Python DB-API使用流程 : 

1. 导入API模块
2. 获取与数据的连接
3. 执行SQL语句和存储过程
4. 关闭数据库连接

MySQLdb只支持Python 3.x之前的版本 , 在Python 3.x中则是用PyMySQL来代替

安装

```python
https://sourceforge.net/projects/mysql-python/
# 安装相关教程可以通过google,baidu等进行查找
```

在上一篇已经介绍了PyMySQL , MySQLdb的用户与PyMySQL是一样的 , 所以这篇直接以实例进行整理 , 并补充对于事务的说明

## 连接数据库  🍀

```python
import MySQLdb
connection = MySQLdb.Connect(host='localhost',
                             user='root',
                             passwd='myroot',
                             db='test',
                             port='3306',
                             charset='utf8')
```

## 创建表  🍀

```python
import MySQLdb
# 连接数据库
connection = MySQLdb.Connect(host='localhost',
                             user='root',
                             passwd='myroot',
                             db='test',
                             port='3306',
                             charset='utf8')
# 创建游标
cursor = connection.cursor()
# 定义sql语句
sql = """CREATE TABLE EMPLOYEE (
         FIRST_NAME  CHAR(20) NOT NULL,
         LAST_NAME  CHAR(20),
         AGE INT,  
         SEX CHAR(1),
         INCOME FLOAT )"""
# 执行sql
cursor.execute(sql)
# 关闭连接
connection.close()
```

## 查询表  🍀

查询方法如下 : 

- fetchone() : 获取下一条查询结果 , 结果集是一个对象
- fetchall() : 获取全部查询结果
- rowcount : 这是一个只读属性 , 并返回执行execute() 方法后的影响行数

```python
import MySQLdb
# 连接数据库
connection = MySQLdb.Connect(host='localhost',
                             user='root',
                             passwd='myroot',
                             db='test',
                             port='3306',
                             charset='utf8')
# 创建游标
cursor = connection.cursor()
# 定义sql语句
sql = "SELECT * FROM EMPLOYEE \
       WHERE INCOME > '%d'" % (1000)
try:
   # 执行SQL语句
   cursor.execute(sql)
   # 获取所有记录列表
   results = cursor.fetchall()
   for row in results:
      fname = row[0]
      lname = row[1]
      age = row[2]
      sex = row[3]
      income = row[4]
      # 打印结果
      print "fname=%s,lname=%s,age=%d,sex=%s,income=%d" % \
             (fname, lname, age, sex, income )
except:
   print "Error: unable to fecth data"
# 关闭连接
connection.close()
```

## 修改表  🍀

插入数据

```python
import MySQLdb
# 连接数据库
connection = MySQLdb.Connect(host='localhost',
                             user='root',
                             passwd='myroot',
                             db='test',
                             port='3306',
                             charset='utf8')
# 创建游标
cursor = connection.cursor()
# 定义sql语句
sql = """INSERT INTO EMPLOYEE(FIRST_NAME,
         LAST_NAME, AGE, SEX, INCOME)
         VALUES ('Mac', 'Mohan', 20, 'M', 2000)"""
try:
   # 执行sql语句
   cursor.execute(sql)
   # 提交到数据库执行
   connection.commit()
except:
   # 出现异常回滚
   connection.rollback()
# 关闭连接
connection.close()
```

更新数据

```python
import MySQLdb
# 连接数据库
connection = MySQLdb.Connect(host='localhost',
                             user='root',
                             passwd='myroot',
                             db='test',
                             port='3306',
                             charset='utf8')
# 创建游标 
cursor = connection.cursor()
# 定义sql语句
sql = "UPDATE EMPLOYEE SET AGE = AGE + 1 WHERE SEX = '%c'" % ('M')
try:
   # 执行SQL语句
   cursor.execute(sql)
   # 提交到数据库执行
   connection.commit()
except:
   # 发生错误时回滚
   connection.rollback()
# 关闭连接
connection.close()
```

## 删除表  🍀

```python
import MySQLdb
# 连接数据库
connection = MySQLdb.Connect(host='localhost',
                             user='root',
                             passwd='myroot',
                             db='test',
                             port='3306',
                             charset='utf8')
# 创建游标 
cursor = connection.cursor()
# 定义sql语句
sql = "DELETE FROM EMPLOYEE WHERE AGE > '%d'" % (20)
try:
   # 执行SQL语句
   cursor.execute(sql)
   # 提交修改
   connection.commit()
except:
   # 发生错误时回滚
   connection.rollback()
# 关闭连接
connection.close()
```

## 事务  🍀

事务机制是为了确保数据的一致性

事务应该具有4个属性 : 

1. 原子性 : 一个事务是一个不可分割的工作单位 , 事务中包括的诸操作要么都做 , 要么都不做
2. 一致性 : 事务必须是数据库从一个一致性状态变到另一个一致性状态 , 一致性与原子性是密切相关的
3. 隔离性 : 一个事务的执行不能被其他事务干扰 , 即一个事务内部的操作及使用的数据对并发的其他事务是隔离的 , 并发执行的各个事务之间不能互相干扰
4. 持久性 : 也成为永久性 , 指一个事务一旦提交 , 它对数据库中数据的改变就应该是永久性的 , 接下来的其他操作或故障不应该对其有任何影响

Python DB-API 2.0的事务提供了两个方法 commit 和rollback , 在上述实例中已经见过了

```python
try:
   # 执行SQL语句
   cursor.execute(sql)
   # 向数据库提交
   connection.commit()
except:
   # 发生错误时回滚
   connection.rollback()
```