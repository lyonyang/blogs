# Python之路 - MySQL表内操作
<!-- TOC -->

- [Python之路 - MySQL表内操作](#python之路---mysql表内操作)
    - [前言  🍀](#前言--🍀)
    - [DDL语句表实例  🍀](#ddl语句表实例--🍀)
        - [创建表  🍀](#创建表--🍀)
        - [删除表  🍀](#删除表--🍀)
        - [修改表  🍀](#修改表--🍀)
    - [DML语句介绍  🍀](#dml语句介绍--🍀)
        - [插入记录  🍀](#插入记录--🍀)
        - [更新记录  🍀](#更新记录--🍀)
        - [删除记录  🍀](#删除记录--🍀)
        - [查询记录  🍀](#查询记录--🍀)

<!-- /TOC -->
## 前言  🍀

前面已经介绍了SQL语句中表的增 , 删 , 改 , 查 , 以及MySQL中的数据类型

本篇根据SQL语句的分类 , 从建立数据库到完成表的所有操作进行实例整理

在第一篇MySQL初识中 , 已经对DDL语句中数据库部分进行了操作 , 那么这篇即对表部分进行操作 

## DDL语句表实例  🍀

DDL语句是对数据库内部的对象进行创建 , 删除 , 修改等操作

它与DML语句的最大区别是DML只是对表内部数据操作 , 而不涉及表的定义 , 结构的修改 , 更不会涉及其他对象

DDL语句更多地由数据库管理员(DBA)使用 , 开发人员一般很少使用

第一篇< [Python之路 - MySQL初识](https://lyonyang.gitbooks.io/blog/02-MySQL/01-Python%E4%B9%8B%E8%B7%AF%20-%20MySQL%E5%88%9D%E8%AF%86.html) > 中已经将DDL语句中表操作部分进行了介绍 , 但没有进行实例练习 , SO

### 创建表  🍀

```mysql
-- 创建数据库
mysql> CREATE DATABASE mydatabase DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
Query OK, 1 row affected (0.00 sec)
-- 使用数据库
mysql> USE mydatabase;
Database changed
-- 创建表tb
mysql> CREATE TABLE tb(
    -> id int(5) NOT NULL AUTO_INCREMENT,
    -> name char(15) NOT NULL,
    -> alias varchar(10) DEFAULT NULL,
    -> email varchar(30) DEFAULT NULL,
    -> password varchar(20) NOT NULL,
    -> phone char(11) DEFAULT '00000000000',
    -> PRIMARY KEY(id,name)
    -> )ENGINE=InnoDB DEFAULT CHARSET=utf8;
Query OK, 0 rows affected (0.24 sec)
-- 查看表定义
mysql> DESC tb;
+----------+-------------+------+-----+-------------+----------------+
| Field    | Type        | Null | Key | Default     | Extra          |
+----------+-------------+------+-----+-------------+----------------+
| id       | int(5)      | NO   | PRI | NULL        | auto_increment |
| name     | char(15)    | NO   | PRI | NULL        |                |
| alias    | varchar(10) | YES  |     | NULL        |                |
| email    | varchar(30) | YES  |     | NULL        |                |
| password | varchar(20) | NO   |     | NULL        |                |
| phone    | char(11)    | YES  |     | 00000000000 |                |
+----------+-------------+------+-----+-------------+----------------+
6 rows in set (0.00 sec)
-- 查看表详细定义,\G的含义是使记录按照字段竖向排列
mysql> SHOW CREATE TABLE tb \G;
*************************** 1. row ***************************
       Table: tb
Create Table: CREATE TABLE `tb` (
  `id` int(5) NOT NULL AUTO_INCREMENT,
  `name` char(15) NOT NULL,
  `alias` varchar(10) DEFAULT NULL,
  `email` varchar(30) DEFAULT NULL,
  `password` varchar(20) NOT NULL,
  `phone` char(11) DEFAULT '00000000000',
  PRIMARY KEY (`id`,`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
1 row in set (0.00 sec)
ERROR:
No query specified
```

### 删除表  🍀

```mysql
mysql> DROP TABLE tb;
Query OK, 0 rows affected (0.21 sec)
```

### 修改表  🍀

**1.修改表类型**

语法 : 

```mysql
ALTER TABLE tablename MODIFY [COLUMN] column_name column_type [FIRST|AFTER col_name]; -- [...]表示中间的可以省略不写
```

实例

```mysql
-- 创建emp表
mysql> CREATE TABLE emp(
    -> ename VARCHAR(10),
    -> hiredate DATE,
    -> sal DECIMAL(10,2),
    -> deptno INT(2)
    -> )ENGINE=InnoDB DEFAULT CHARSET=utf8;
Query OK, 0 rows affected (0.27 sec)
-- 修改emp表中ename字段的类型
mysql> ALTER TABLE emp MODIFY ename varchar(20);
Query OK, 0 rows affected (0.08 sec)
Records: 0  Duplicates: 0  Warnings: 0
-- 查看表定义
mysql> DESC emp;
+----------+---------------+------+-----+---------+-------+
| Field    | Type          | Null | Key | Default | Extra |
+----------+---------------+------+-----+---------+-------+
| ename    | varchar(20)   | YES  |     | NULL    |       |
| hiredate | date          | YES  |     | NULL    |       |
| sal      | decimal(10,2) | YES  |     | NULL    |       |
| deptno   | int(2)        | YES  |     | NULL    |       |
+----------+---------------+------+-----+---------+-------+
4 rows in set (0.00 sec)
```

**2.增加表字段**

语法 : 

```mysql
ALTER TABLE tablename ADD [COLUMN] column_name column_type [FIRST|AFTER col_name];
ALTER TABLE tablename ADD PRIMARY KEY(column_name);
ALTER TABLE slave_table ADD CONSTRAINT symbol(如:FK_slave_primary) FOREIGN KEY slave_table(foreign_name) REFERENCES primary_table(primary_name);
```

实例 : 

```mysql
-- 增加age字段
mysql> ALTER TABLE emp ADD age int(3);
Query OK, 0 rows affected (0.63 sec)
Records: 0  Duplicates: 0  Warnings: 0
-- 增加id字段
mysql> ALTER TABLE emp ADD id int(5);
Query OK, 0 rows affected (0.53 sec)
Records: 0  Duplicates: 0  Warnings: 0
-- 将id字段设置为主键
mysql> ALTER TABLE emp ADD PRIMARY KEY(id);
Query OK, 0 rows affected (0.41 sec)
Records: 0  Duplicates: 0  Warnings: 0
-- 查看表定义
mysql> DESC emp;
+----------+---------------+------+-----+---------+-------+
| Field    | Type          | Null | Key | Default | Extra |
+----------+---------------+------+-----+---------+-------+
| ename    | varchar(20)   | YES  |     | NULL    |       |
| hiredate | date          | YES  |     | NULL    |       |
| sal      | decimal(10,2) | YES  |     | NULL    |       |
| deptno   | int(2)        | YES  |     | NULL    |       |
| age      | int(3)        | YES  |     | NULL    |       |
| id       | int(5)        | NO   | PRI | NULL    |       |
+----------+---------------+------+-----+---------+-------+
6 rows in set (0.00 sec)
```

**3.删除表字段**

语法 : 

```mysql
ALTER TABLE tablename DROP [COLUMN] column_name;
ALTER TABLE DROP FOREIGN KEY foreign_key_name;
ALTER TABLE DROP PRIMARY KEY;
```

实例 : 

```mysql
-- 删除age字段
mysql> ALTER TABLE emp DROP age;
Query OK, 0 rows affected (0.42 sec)
Records: 0  Duplicates: 0  Warnings: 0
-- 删除主键
mysql> ALTER TABLE emp DROP PRIMARY KEY;
Query OK, 0 rows affected (0.62 sec)
Records: 0  Duplicates: 0  Warnings: 0
-- 查看表定义
mysql> DESC emp;
+----------+---------------+------+-----+---------+-------+
| Field    | Type          | Null | Key | Default | Extra |
+----------+---------------+------+-----+---------+-------+
| ename    | varchar(20)   | YES  |     | NULL    |       |
| hiredate | date          | YES  |     | NULL    |       |
| sal      | decimal(10,2) | YES  |     | NULL    |       |
| deptno   | int(2)        | YES  |     | NULL    |       |
| id       | int(5)        | NO   |     | NULL    |       |
+----------+---------------+------+-----+---------+-------+
5 rows in set (0.00 sec)
```

**4.字段改名**

语法 : 

```mysql
ALTER TABLE tablename CHANGE [COLUMN] old_col_name new_col_name column_type [FIRST|AFTER col_name];
```

实例 : 

```mysql
-- 将sal字段修改为salary
mysql> ALTER TABLE emp CHANGE sal salary decimal(10,2);
Query OK, 0 rows affected (0.09 sec)
Records: 0  Duplicates: 0  Warnings: 0
-- 查看表定义
mysql> DESC emp;
+----------+---------------+------+-----+---------+-------+
| Field    | Type          | Null | Key | Default | Extra |
+----------+---------------+------+-----+---------+-------+
| ename    | varchar(20)   | YES  |     | NULL    |       |
| hiredate | date          | YES  |     | NULL    |       |
| salary   | decimal(10,2) | YES  |     | NULL    |       |
| deptno   | int(2)        | YES  |     | NULL    |       |
| id       | int(5)        | NO   |     | NULL    |       |
+----------+---------------+------+-----+---------+-------+
5 rows in set (0.00 sec)
```

PS : change 和 modify都可以修改表类型 , 不同的是change后面需要写两次列名 ; 并且change可以修改列名 , modify则不能

**5.修改字段排列顺序**

前面介绍的字段增加和修改语法(ADD/CHANGE/MODIFY)中, 都有一个可选项 `[FIRST|AFTER col_name]` ,这个选项可以用来修改字段在表中的位置 , ADD增加的新字段默认是加在表的最后位置 , 而CHANGE/MODIFY默认都不会改变字段的位置

将新增的字段birth date加在ename之后

```mysql
mysql> DESC emp;
+----------+---------------+------+-----+---------+-------+
| Field    | Type          | Null | Key | Default | Extra |
+----------+---------------+------+-----+---------+-------+
| ename    | varchar(20)   | YES  |     | NULL    |       |
| hiredate | date          | YES  |     | NULL    |       |
| salary   | decimal(10,2) | YES  |     | NULL    |       |
| deptno   | int(2)        | YES  |     | NULL    |       |
| id       | int(5)        | NO   |     | NULL    |       |
+----------+---------------+------+-----+---------+-------+
5 rows in set (0.00 sec)
-- 新增birth date字段在ename之后
mysql> ALTER TABLE emp ADD birth date AFTER ename;
Query OK, 0 rows affected (0.45 sec)
Records: 0  Duplicates: 0  Warnings: 0
-- 查看表定义
mysql> DESC emp;
+----------+---------------+------+-----+---------+-------+
| Field    | Type          | Null | Key | Default | Extra |
+----------+---------------+------+-----+---------+-------+
| ename    | varchar(20)   | YES  |     | NULL    |       |
| birth    | date          | YES  |     | NULL    |       |
| hiredate | date          | YES  |     | NULL    |       |
| salary   | decimal(10,2) | YES  |     | NULL    |       |
| deptno   | int(2)        | YES  |     | NULL    |       |
| id       | int(5)        | NO   |     | NULL    |       |
+----------+---------------+------+-----+---------+-------+
6 rows in set (0.00 sec)
```

修改salary字段 , 将它放在最前面

```mysql
mysql> ALTER TABLE emp MODIFY salary DECIMAL(10,2) FIRST;
Query OK, 0 rows affected (0.55 sec)
Records: 0  Duplicates: 0  Warnings: 0
-- 查看表定义
mysql> DESC emp;
+----------+---------------+------+-----+---------+-------+
| Field    | Type          | Null | Key | Default | Extra |
+----------+---------------+------+-----+---------+-------+
| salary   | decimal(10,2) | YES  |     | NULL    |       |
| ename    | varchar(20)   | YES  |     | NULL    |       |
| birth    | date          | YES  |     | NULL    |       |
| hiredate | date          | YES  |     | NULL    |       |
| deptno   | int(2)        | YES  |     | NULL    |       |
| id       | int(5)        | NO   |     | NULL    |       |
+----------+---------------+------+-----+---------+-------+
6 rows in set (0.00 sec)
```

PS : CHANGE/FIRST|AFTER COLUMN 这些关键字都属于MySQL在标准SQL上的扩展 , 在其他数据库上不一定适用

**6.更改表名**

语法 : 

```mysql
ALTER TABLE tablename RENAME [TO] new_tablename;
```

实例 : 

```mysql
mysql> ALTER TABLE emp RENAME emp1;
Query OK, 0 rows affected (0.16 sec)
-- 表明改变
mysql> DESC emp1;
+----------+---------------+------+-----+---------+-------+
| Field    | Type          | Null | Key | Default | Extra |
+----------+---------------+------+-----+---------+-------+
| salary   | decimal(10,2) | YES  |     | NULL    |       |
| ename    | varchar(20)   | YES  |     | NULL    |       |
| birth    | date          | YES  |     | NULL    |       |
| hiredate | date          | YES  |     | NULL    |       |
| deptno   | int(2)        | YES  |     | NULL    |       |
| id       | int(5)        | NO   |     | NULL    |       |
+----------+---------------+------+-----+---------+-------+
6 rows in set (0.00 sec)
```

**7.默认值**

语法 : 

```mysql
-- 修改默认值
ALTER TABLE tablename ALTER field_name SET DEFAULT v;
-- 删除默认值
ALTER TABLE tablename ALTER field_name DROP DEFAULT;
```

实例 : 

```mysql
-- 将salary字段默认值修改为2000
mysql> ALTER TABLE emp1 ALTER salary SET DEFAULT 2000;
Query OK, 0 rows affected (0.12 sec)
Records: 0  Duplicates: 0  Warnings: 0
-- 查看表定义
mysql> DESC emp1;
+----------+---------------+------+-----+---------+-------+
| Field    | Type          | Null | Key | Default | Extra |
+----------+---------------+------+-----+---------+-------+
| salary   | decimal(10,2) | YES  |     | 2000.00 |       |
| ename    | varchar(20)   | YES  |     | NULL    |       |
| birth    | date          | YES  |     | NULL    |       |
| hiredate | date          | YES  |     | NULL    |       |
| deptno   | int(2)        | YES  |     | NULL    |       |
| id       | int(5)        | NO   |     | NULL    |       |
+----------+---------------+------+-----+---------+-------+
6 rows in set (0.00 sec)
-- 删除salary的默认值
mysql> ALTER TABLE emp1 ALTER salary DROP DEFAULT;
Query OK, 0 rows affected (0.09 sec)
Records: 0  Duplicates: 0  Warnings: 0
-- 查看表定义
mysql> DESC emp1;
+----------+---------------+------+-----+---------+-------+
| Field    | Type          | Null | Key | Default | Extra |
+----------+---------------+------+-----+---------+-------+
| salary   | decimal(10,2) | YES  |     | NULL    |       |
| ename    | varchar(20)   | YES  |     | NULL    |       |
| birth    | date          | YES  |     | NULL    |       |
| hiredate | date          | YES  |     | NULL    |       |
| deptno   | int(2)        | YES  |     | NULL    |       |
| id       | int(5)        | NO   |     | NULL    |       |
+----------+---------------+------+-----+---------+-------+
6 rows in set (0.00 sec)
```

## DML语句介绍  🍀

DML操作是指对数据库中表记录的操作 , 主要包括表记录的插入(insert) , 更新(update) , 删除(delete) 和查询(select) , 是开发人员日常使用最频繁的操作

### 插入记录  🍀

语法 : 

```mysql
INSERT INTO tablename(field1,field2,...,fieldn) VALUES(value1,value2,...,valuen);
```

实例 : 

```mysql
mysql> DESC emp;
+----------+---------------+------+-----+---------+-------+
| Field    | Type          | Null | Key | Default | Extra |
+----------+---------------+------+-----+---------+-------+
| ename    | varchar(10)   | YES  |     | NULL    |       |
| hiredate | date          | YES  |     | NULL    |       |
| sal      | decimal(10,2) | YES  |     | NULL    |       |
| deptno   | int(2)        | YES  |     | NULL    |       |
+----------+---------------+------+-----+---------+-------+
4 rows in set (0.00 sec)
-- 插入数据,values中的顺序需排列一致
mysql> INSERT INTO emp(ename,hiredate,sal,deptno) VALUES('lyon','2000-01-01','2000',1);
Query OK, 1 row affected (0.08 sec)
-- 插入第二条数据
mysql> INSERT INTO emp(ename,hiredate,sal,deptno) VALUES('kenneth','2000-01-01','1000',2);
Query OK, 1 row affected (0.10 sec)
-- 没写的字段自动设置为NULL,默认值,自增的下一个数字
mysql> INSERT INTO emp(ename,sal) VALUES('alex',500);
Query OK, 1 row affected (0.24 sec)
-- 查看emp表中的所有记录
mysql> SELECT * FROM emp;
+---------+------------+---------+--------+
| ename   | hiredate   | sal     | deptno |
+---------+------------+---------+--------+
| lyon    | 2000-01-01 | 2000.00 |      1 |
| kenneth | 2000-01-01 | 1000.00 |      2 |
| alex    | NULL       |  500.00 |   NULL |
+---------+------------+---------+--------+
3 rows in set (0.00 sec)
```

一次性插入多条 : 

```mysql
INSERT INTO tablename(field1,field2,...,fieldn) VALUES
(value1,value2,...,valuen),  -- 以逗号分隔
(value1,value2,...,valuen),
(value1,value2,...,valuen),
(value1,value2,...,valuen);
```

### 更新记录  🍀

语法 : 

```mysql
UPDATE tablename SET field1=value1,field2=value2,...,fieldn=valuen [WHERE CONDITION];
```

实例 : 

```mysql
mysql> UPDATE emp SET sal=100000 WHERE ename='lyon';
Query OK, 1 row affected (0.10 sec)
Rows matched: 1  Changed: 1  Warnings: 0
```

同时更新多个表中数据

```mysql
UPDATE t1,t2,...,tn SET t1.field1=expr1,tn.fieldn=exprn [WHERE CONDITION];
```

### 删除记录  🍀

语法 : 

```mysql
DELETE FROM tablename [WHERE CONDITION];
```

实例 : 

```mysql
mysql> DELETE FROM emp WHERE ename='alex';
Query OK, 1 row affected (0.06 sec)
```

一次删除多个表的数据

```mysql
DELETE t1,t2,...,tn FROM t1,t2,...,tn [WHERE CONDITION];
```

实例 : 

```mysql
-- 查询记录
mysql> SELECT * FROM dept;
+--------+----------+
| deptno | deptname |
+--------+----------+
|      1 | tech     |
|      2 | sale     |
|      3 | hr       |
+--------+----------+
3 rows in set (0.00 sec)
-- 查询记录
mysql> SELECT * FROM emp;
+---------+------------+-----------+--------+
| ename   | hiredate   | sal       | deptno |
+---------+------------+-----------+--------+
| lyon    | 2000-01-01 | 100000.00 |      1 |
| kenneth | 2000-01-01 |   1000.00 |      2 |
+---------+------------+-----------+--------+
2 rows in set (0.00 sec)
-- 删除两个表中deptno为2的记录
mysql> DELETE a,b FROM emp a,dept b WHERE a.deptno=b.deptno and a.deptno=2;
Query OK, 2 rows affected (0.11 sec)
-- 查询记录
mysql> SELECT * FROM emp;
+-------+------------+-----------+--------+
| ename | hiredate   | sal       | deptno |
+-------+------------+-----------+--------+
| lyon  | 2000-01-01 | 100000.00 |      1 |
+-------+------------+-----------+--------+
1 row in set (0.00 sec)
-- 查询记录
mysql> SELECT * FROM dept;
+--------+----------+
| deptno | deptname |
+--------+----------+
|      1 | tech     |
|      3 | hr       |
+--------+----------+
2 rows in set (0.00 sec)
```

PS : 不管是单表还是多表 , 不加where条件会把表的所有记录删除 , 所以操作时一定要小心

### 查询记录  🍀

语法 : 

```mysql
SELECT * FROM tablename [WHERE CONDITION];
```

"*"表示要将所有的记录都选出来 , 也可以用逗号分割所有的字段来代替

如上面例子中

```mysql
mysql> SELECT ename,hiredate,sal,deptno FROM emp;
```

**1.查询不重复的记录**

```mysql
mysql> SELECT DISTINCT deptno FROM emp;
+--------+
| deptno |
+--------+
|      1 |
+--------+
1 row in set (0.00 sec)
```

**2.条件查询**

```mysql
mysql> SELECT * FROM emp WHERE deptno=1;
+-------+------------+-----------+--------+
| ename | hiredate   | sal       | deptno |
+-------+------------+-----------+--------+
| lyon  | 2000-01-01 | 100000.00 |      1 |
+-------+------------+-----------+--------+
1 row in set (0.00 sec)
```

**3.排序和限制**

```mysql
-- 按工资高低进行显示
mysql> SELECT * FROM emp order by sal;
+---------+------------+-----------+--------+
| ename   | hiredate   | sal       | deptno |
+---------+------------+-----------+--------+
| kenneth | 2000-01-01 |   5000.00 |      2 |
| alex    | 2000-01-01 |   8000.00 |      3 |
| lyon    | 2000-01-01 | 100000.00 |      1 |
+---------+------------+-----------+--------+
3 rows in set (0.00 sec)
```

对于排序后的记录 , 如果希望只显示一部分 , 可以使用LIMIT关键字来实现

```mysql
SELECT ...[LIMIT offset_start,row_count]
-- offset_start表示记录的起始偏移量,默认为0;row_count表示显示的行数
```

实例

```mysql
mysql> SELECT * FROM emp ORDER BY sal LIMIT 2;
+---------+------------+---------+--------+
| ename   | hiredate   | sal     | deptno |
+---------+------------+---------+--------+
| kenneth | 2000-01-01 | 5000.00 |      2 |
| alex    | 2000-01-01 | 8000.00 |      3 |
+---------+------------+---------+--------+
2 rows in set (0.00 sec)
```

PS : limit属于MySQL扩展SQL92后的语法 , 在其他数据库上并不能通用

**4.聚合**

用于进行汇总操作

语法 : 

```mysql
SELECT [field1,field2,...,fieldn] fun_name
FROM tablename
[WHERE where_condition]
[GROUP BY field1,dield2,,...,fieldn
[WITH ROLLUP]]
[HAVING where_contition]
/* 参数说明 */
fun_name 表示要做的聚合操作,也就是聚合函数,常用的有 sum(求和),count(*)(记录表),max(最大值),min(最小值)
GROUP BY 关键字表示要进行分类聚合的字段,比如要按照部门分类统计员工数量,部门就应该写在 group by后面
WITH ROLLUP 是可选语法,表明是否对分类聚合后的结果进行再汇总
HAVING 关键字表示对分类后的结果再进行条件的过滤
-- 注意 :
having 和 where的区别在于,having是对聚合后的结果进行条件的过滤,而 where是在聚合前就对记录进行过滤,所以我们应该尽可能用 where先过滤记录,使结果集减小,会对聚合的效率大大提高
```

实例 : 

```mysql
/* 统计emp表中公司的总人数 */
mysql> SELECT count(1) FROM emp;
+----------+
| count(1) |
+----------+
|        5 |
+----------+
1 row in set (0.00 sec)
/* 统计个部门的总人数 */
mysql> SELECT count(1) FROM emp GROUP BY deptno;
+----------+
| count(1) |
+----------+
|        2 |
|        2 |
|        1 |
+----------+
3 rows in set (0.00 sec)
/* 既统计各部门人数,又统计总人数 */
mysql> SELECT deptno,count(1) FROM emp GROUP BY deptno WITH ROLLUP;
+--------+----------+
| deptno | count(1) |
+--------+----------+
|      1 |        2 |
|      2 |        2 |
|      3 |        1 |
|   NULL |        5 |
+--------+----------+
4 rows in set (0.00 sec)
/* 统计人数大于1的部门 */
mysql> SELECT deptno,count(1) FROM emp GROUP BY deptno HAVING count(1)>1;
+--------+----------+
| deptno | count(1) |
+--------+----------+
|      1 |        2 |
|      2 |        2 |
+--------+----------+
2 rows in set (0.00 sec)
/* 统计公司所有员工的薪水总额,最高和最低薪水 */
mysql> SELECT sum(sal),max(sal),min(sal) FROM emp;
+-----------+-----------+----------+
| sum(sal)  | max(sal)  | min(sal) |
+-----------+-----------+----------+
| 113000.00 | 100000.00 |  5000.00 |
+-----------+-----------+----------+
1 row in set (0.00 sec)
```

**5.表连接**

同时显示多个表中的字段 , 分为内连接和外连接

内连接仅选出两张表中互相匹配的记录 , 外连接会选出其他不匹配的记录 , 我们最常用的是内连接

外连接又分为左连接和右连接

内连接 : 

```mysql
mysql> SELECT * FROM emp;
+---------+------------+-----------+--------+
| ename   | hiredate   | sal       | deptno |
+---------+------------+-----------+--------+
| lyon    | 2000-01-01 | 100000.00 |      1 |
| kenneth | 2000-01-01 |   5000.00 |      2 |
| alex    | 2000-01-01 |   8000.00 |      3 |
| egon    | NULL       |      NULL |      1 |
| eva     | NULL       |      NULL |      2 |
+---------+------------+-----------+--------+
5 rows in set (0.00 sec)

mysql> SELECT * FROM dept;
+--------+----------+
| deptno | deptname |
+--------+----------+
|      1 | tech     |
|      3 | hr       |
|      2 | sale     |
+--------+----------+
3 rows in set (0.00 sec)

mysql> SELECT ename,deptname FROM emp,dept WHERE emp.deptno=dept.deptno;
+---------+----------+
| ename   | deptname |
+---------+----------+
| lyon    | tech     |
| kenneth | sale     |
| alex    | hr       |
| egon    | tech     |
| eva     | sale     |
+---------+----------+
5 rows in set (0.00 sec)
```

外连接 : 

根据上述实例 , 语句为

左连接 : `SELECT ename,deptname FROM emp LEFT JOIN dept ON emp.deptno=dept.deptno;`

右连接 : `SELECT ename,deptname FROM emp RIGHT JOIN dept ON emp.deptno=dept.deptno;`

**6.子查询**

查询时 , 需要的条件是另一个select语句的结果

```mysql
mysql> SELECT * FROM emp WHERE deptno in(SELECT deptno FROM dept);
+---------+------------+-----------+--------+
| ename   | hiredate   | sal       | deptno |
+---------+------------+-----------+--------+
| lyon    | 2000-01-01 | 100000.00 |      1 |
| kenneth | 2000-01-01 |   5000.00 |      2 |
| alex    | 2000-01-01 |   8000.00 |      3 |
| egon    | NULL       |      NULL |      1 |
| eva     | NULL       |      NULL |      2 |
+---------+------------+-----------+--------+
5 rows in set (0.00 sec)
```

如果子查询记录数唯一 , 可以用 = 代替 in , 即`SELECT * FROM emp WHERE deptno = (SELECT deptno FROM dept);` 

某些情况下 , 子查询可以转化为表连接 , 如下

```mysql
mysql> SELECT * FROM emp WHERE deptno in(SELECT deptno FROM dept);
+---------+------------+-----------+--------+
| ename   | hiredate   | sal       | deptno |
+---------+------------+-----------+--------+
| lyon    | 2000-01-01 | 100000.00 |      1 |
| kenneth | 2000-01-01 |   5000.00 |      2 |
| alex    | 2000-01-01 |   8000.00 |      3 |
| egon    | NULL       |      NULL |      1 |
| eva     | NULL       |      NULL |      2 |
+---------+------------+-----------+--------+
5 rows in set (0.00 sec)
```

PS : 

- MySQL 4.1 以前的版本不支持子查询 , 需要用表连接来实现子查询
- 表连接在很多情况下用于优化子查询

**7.记录联合**

`union` 和`union all` 关键字可以实现 , 将多个表的数据按照一定的查询条件查询出来后 , 将结果合并到一起显示

语法 : 

```mysql
SELECT * FROM t1
UNION\UNION ALL
SELECT * FROM t2
...
UNION\UNION ALL
SELECT * FROM tn;
```

实例 : 

```mysql
mysql> SELECT deptno FROM emp
    -> UNION
    -> SELECT deptno FROM dept;
+--------+
| deptno |
+--------+
|      1 |
|      2 |
|      3 |
+--------+
3 rows in set (0.00 sec)
```

PS : `union all`是把结果集直接合并在一起 , 而`union`是将union all后的结果进行一次distinct , 去除重复记录后的结果 















