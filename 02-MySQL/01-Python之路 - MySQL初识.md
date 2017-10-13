# Python之路 - MySQL初识
<!-- TOC -->

- [Python之路 - MySQL初识](#python之路---mysql初识)
    - [前言  🍀](#前言--🍀)
    - [MySQL介绍  🍀](#mysql介绍--🍀)
    - [SQL介绍](#sql介绍)
    - [数据库操作  🍀](#数据库操作--🍀)
    - [数据表操作  🍀](#数据表操作--🍀)

<!-- /TOC -->
## 前言  🍀

为了科学地组织和存储数据 , 实现高效获取和维护数据 , 我们需要使用一个系统软件 , 数据库管理系统 (DataBase Management System , BDMS) , 简称数据库

数据库又分为关系型和非关系型两种 : 

- 关系型数据库 : MySQL , Oracle , SqlServer , Access , Db2 , SQLite , MariaDB
- 非关系型数据库 : Redis , MongoDB , Memcached , Cassandra

## MySQL介绍  🍀

MySQL是一种快速易用的关系型数据库管理系统(RDBMS) , 由瑞典MySQL AB公司开发 , 目前属于Oracle旗下公司 , MySQL是目前最流行的关系型数据库管理系统 , 在Web应用方面MySQL是最好的RDBMS应用软件之一

具备以下优点 : 

1. 开源 , 免费使用
2. 自身功能非常强大 , 足以匹敌绝大多数功能强大但却价格昂贵的数据库软件
3. 使用业内所熟悉的标准SQL数据库语言(SQL语句通用)
4. 可运行于多个操作系统 , 支持多种语言 , 包括PHP , C , C++ , Java等语言
5. 非常迅速 , 即使面对大型数据集也毫无滞涩
6. 非常适用Web应用开发
7. 支持大型数据库 , 最高可在一个表中容纳5千多万行 ; 每张表的默认文件大小限制4GB , 不过如果操作系统支持 , 可以将期理论限制增加到800万TB
8. 可以自定义 , 开源GPL许可保证了程序员可以自由修改MySQL , 以便适应各自特殊的开发环境

**RDBMS术语**

| 术语                          | 描述                                       |
| --------------------------- | ---------------------------------------- |
| 数据库(Database)               | 数据库是带有相关数据的表的集合                          |
| 表(Table)                    | 表是带有数据的矩阵 , 数据库中的表就像一种简单的电子表格            |
| 列(Column)                   | 每一列 (数据元素) 都包含着同种类型的数据 , 比如邮编            |
| 行(Row)                      | 行 (又被称为元组 , 项或者记录) 是一组相关数据  , 比如有关订阅量的数据 |
| 冗余(Redundancy)              | 存储两次数据 , 以便使系统更快速                        |
| 主键(Primary key)             | 主键是唯一的 , 同一张表中不允许出现同样两个键值 , 一个键值只对应着一行   |
| 外键(Foreign key)             | 用于连接两张表                                  |
| 复合键(Compound key)           | 复合键 (又称组合键) 是一种由多列组成的键 , 因为一列并不足以确定唯一性   |
| 索引(Index)                   | 它在数据库中的作用就像书后的索引一样                       |
| 引用完性(Referential Integrity) | 用来确保外键一直指向已存在的一行                         |

## SQL介绍

SQL是Structured Query Language(结构化查询语言)的缩写 , SQL是转为数据库而建立的操作命令集 , 是一种功能齐全的数据库语言

**SQL分类**

SQL语句主要可以划分为一下3个类别 : 

- DDL(Data Definition Languages) 语句 : 数据定义语句 , 这些语句定义了不同的数据段 , 数据库 , 表 , 列 , 索引等数据库对象 ; 常用的语句关键字主要包括create , drop , alter等
- DML(Data Manipulation Language) 语句 : 数据操纵语句 , 用于添加 , 删除 , 更新和查询数据库记录 , 并检查数据完整性 ; 常用的语句关键字主要包括insert , delete , update和select等
- DCL(Data Control Language) 语句 : 数据控制语句 , 用于控制不同数据段直接许可和访问级别的语句 , 这些语句定义了数据库 , 表 , 字段 , 用户的访问权限和安全级别 ; 主要的语句关键字包括grant , revoke等

**SQL规范**

- 在数据库系统中 , SQL语句不区分大小写 (建议用大写) , 但字符串常量区分大小写 ; 建议命令大写 , 表名库名小写
- SQL语句可单行或多行书写 , 以" ; "结尾 , 关键字不能跨多行或简写
- 用空格和缩进来提高语句的可读性 , 子句通常位于独立行 , 便于编辑 , 提高可读性
- 单行注释 : --  多行注释 : / \*... \*/
- SQL语句可拆行操作

## 数据库操作  🍀

在MySQL数据中有如下默认数据库

| 默认数据库              | 描述                                       |
| ------------------ | ---------------------------------------- |
| information_schema | 虚拟库 , 不占用磁盘空间 , 存储的是数据库启动后的一些参数 , 如用户表信息 , 列信息 , 权限信息 , 字符信息等 |
| test               | 用户用来测试的数据库 (MySQL 5.7没有)                 |
| mysql              | 授权库 , 主要存储系统用户的权限信息                      |
| performance_schema | MySQL 5.5 后新增的 , 主要用于收集数据库服务器性能参数 , 记录处理查询请求时发生的各种事件 , 锁等现象 |
| sys                | 包含了一系列视图、函数和存储过程                         |

> **查看数据库**

```mysql
SHOW DATABASES; 查看所有数据库
SHOW CREATE DATABASE dbname; 查看数据库的创建信息
```

实例

```mysql
mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
4 rows in set (0.00 sec)
/* 查看mysql库的创建信息 */
mysql> show create database mysql;
+----------+----------------------------------------------------------------+
| Database | Create Database                                                |
+----------+----------------------------------------------------------------+
| mysql    | CREATE DATABASE `mysql` /*!40100 DEFAULT CHARACTER SET utf8 */ |
+----------+----------------------------------------------------------------+
1 row in set (0.00 sec)
```
> **创建数据库**

```mysql
CREATE DATABASE dbname DEFAULT CHARSET utf8 COLLATE utf8_general_ci; 创建字符串为utf-8的数据库
CREATE DATABASE dbname DEFAULT CHARACTER SET gbk COLLATE gbk_chinese_ci; 创建字符串为gbk的数据库
```

实例

```mysql
mysql> CREATE DATABASE test DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
Query OK, 1 row affected (0.00 sec)
/* 查看所有数据库 */
mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
| test               |
+--------------------+
5 rows in set (0.00 sec)
```
> **删除数据库**

```mysql
DROP DATABASE dbname; 删除数据库
```

> **使用数据库**

```mysql
USE dbname; 进入数据库
SHOW TABLES; 查看当前数据库中所有的表
SELECT DATABASE(); 查看当前使用的数据库
```

实例

```mysql
mysql> SELECT DATABASE();
+------------+
| DATABASE() |
+------------+
| NULL       |
+------------+
1 row in set (0.00 sec)
/* 使用mysql数据库 */
mysql> USE mysql;
Database changed
mysql> SELECT DATABASE();
+------------+
| DATABASE() |
+------------+
| mysql      |
+------------+
1 row in set (0.00 sec)
```
> **用户管理**

```mysql
CREATE USER 'lyon'@'%' IDENTIFIED BY '123'; 创建`lyon`用户,允许任意IP访问,密码为`123`
RENAME USER 'lyon'@'%' TO 'mylyon'@'127.0.0.1'; 修改用户
SET PASSWORD FOR 'mylyon'@'127.0.0.1' = PASSWORD('456'); 修改密码为`456`
DROP USER 'mylyon'@'127.0.0.1'; 删除用户`lyon`
```

实例

```mysql
/* 用户权限信息都在mysql库中,先进入mysql库 */
mysql> USE mysql;
Database changed
/* 查看原有用户 */
mysql> SELECT HOST,USER FROM USER;
+-----------+-----------+
| HOST      | USER      |
+-----------+-----------+
| localhost | mysql.sys |
| localhost | root      |
+-----------+-----------+
2 rows in set (0.00 sec)
/* 创建新用户'lyon',允许任意IP */
mysql> CREATE USER 'lyon'@'%' IDENTIFIED BY '123';
Query OK, 0 rows affected (0.00 sec)
/* 查看所有用户 */
mysql> SELECT HOST,USER FROM USER;
+-----------+-----------+
| HOST      | USER      |
+-----------+-----------+
| %         | lyon      |
| localhost | mysql.sys |
| localhost | root      |
+-----------+-----------+
3 rows in set (0.00 sec)
/* 修改用户 */
mysql> RENAME USER 'lyon'@'%' TO 'mylyon'@'127.0.0.1';
Query OK, 0 rows affected (0.00 sec)
/* 查看所有用户 */
mysql> SELECT HOST,USER FROM USER;
+-----------+-----------+
| HOST      | USER      |
+-----------+-----------+
| 127.0.0.1 | mylyon    |
| localhost | mysql.sys |
| localhost | root      |
+-----------+-----------+
3 rows in set (0.00 sec)
/* 修改用户密码 */
mysql> SET PASSWORD FOR 'mylyon'@'127.0.0.1' = PASSWORD('456');
Query OK, 0 rows affected, 1 warning (0.00 sec)
/* 删除用户 */
mysql> DROP USER 'mylyon'@'127.0.0.1';
Query OK, 0 rows affected (0.00 sec)
/* 查看所有用户 */
mysql> SELECT HOST,USER FROM USER;
+-----------+-----------+
| HOST      | USER      |
+-----------+-----------+
| localhost | mysql.sys |
| localhost | root      |
+-----------+-----------+
2 rows in set (0.00 sec)
```

注意 : 

```mysql
'username'@'IP'        	 用户只能在该IP下才能访问
'username'@'127.0.0.1'   用户只能在该IP段下才能访问(通配符%表示任意)
'username'@'%'           用户可以再任意IP下访问(默认IP地址为%)
```
> **授权管理**

```mysql
SHOW GRANTS FOR 'username'@'IP'; 查看用户权限
GRANT 权限 ON dbname.表 TO 'username'@'IP';  授权
REVOKE 权限 ON dbname.表 FROM 'username'@'IP'; 取消授权
```

实例

```mysql
/* 创建用户lyon@%,密码为123 */
mysql> CREATE USER 'lyon'@'%' IDENTIFIED BY '123';
Query OK, 0 rows affected (0.00 sec)
/* 查看用户lyon@%的权限 */
mysql> SHOW GRANTS FOR 'lyon'@'%';
+----------------------------------+
| Grants for lyon@%                |
+----------------------------------+
| GRANT USAGE ON *.* TO 'lyon'@'%' |
+----------------------------------+
1 row in set (0.00 sec)
/* 授予用户lyon@% select权限,即将Select_priv改成Y */
mysql> GRANT SELECT ON *.* TO 'lyon'@'%';
Query OK, 0 rows affected (0.00 sec)
/* 查看用户lyon@%的权限 */
mysql> SHOW GRANTS FOR 'lyon'@'%';
+-----------------------------------+
| Grants for lyon@%                 |
+-----------------------------------+
| GRANT SELECT ON *.* TO 'lyon'@'%' |
+-----------------------------------+
1 row in set (0.00 sec)
/* 取消对用户lyon@%的SELECT授权 */
mysql> REVOKE SELECT ON *.* FROM 'lyon'@'%';
Query OK, 0 rows affected (0.00 sec)
/* 查看用户lyon@%的权限 */
mysql> SHOW GRANTS FOR 'lyon'@'%';
+----------------------------------+
| Grants for lyon@%                |
+----------------------------------+
| GRANT USAGE ON *.* TO 'lyon'@'%' |
+----------------------------------+
1 row in set (0.00 sec)
```

也可以用`SELECT * FROM USER WHERE USER='lyon' AND HOST='%' \G;` 命令查看 , 具体如下 : 

```mysql
*************************** 1. row ***************************
                  Host: %
                  User: lyon
           Select_priv: N
           ...
*************************** 1. row ***************************
                  Host: %
                  User: lyon
           Select_priv: Y
           ...
```

权限介绍

```
all privileges  除grant外的所有权限
select          仅查权限
select,insert   查和插入权限
usage           无访问权限
alter           使用alter table
alter routine   使用alter procedure和drop procedure
create          使用create table
create routine  使用create procedure
create temporary tables 使用create temporary tables
create user     使用create user,drop user,rename user和revoke all privileges
create view     使用create view
delete          使用delete
drop            使用drop table
execute         使用call和存储过程
file            使用select into outfile 和 load data infile
grant option    使用grant 和 revoke
index           使用index
insert          使用insert
lock tables     使用lock table
process         使用show full processlist
select          使用select
show databases  使用show databases
show view       使用show view
update          使用update
reload          使用flush
shutdown        使用mysqladmin shutdown(关闭MySQL)
super           使用change master,kill,logs,purge,master和set global,还允许					mysqladmin调试登陆
replication client      服务器位置的访问
replication slave       由复制从属使用
flush privileges　　　	　将数据读取到内存中,从而立即生效
```

**PS** :  * 代表所有 , \*.\* 代表所有数据库中的所有表

## 数据表操作  🍀

> 创建表

```mysql
/* 是否可空 */
CREATE TABLE tablename(
	column_name type NULL,     /* 列名,类型,可为空 */
	column_name type NOT NULL  /* 列名,类型,不可为空 */
)ENGINE=InnoDB DEFAULT CHARSET=utf8
/* 默认值 */
CREATE TABLE tablename(
	column_name type DEFAULT NULL ,   	  /* 列名,类型,默认为空 */
  　column_name type NOT NULL DEFAULT 2   /* 列名,类型,默认为空 */
)ENGINE=InnoDB DEFAULT CHARSET=utf8
/* 自增 */
CREATE TABLE tablename(
    column_name type NOT NULL auto_increment PRIMARY KEY,
)ENGINE=InnoDB DEFAULT CHARSET=utf8
或
CREATE TABLE tablename(
    column_name type NOT NULL auto_increment,
    INDEX(column_name)
)ENGINE=InnoDB DEFAULT CHARSET=utf8
    对于自增列,必须是索引(含主键)
    对于自增可以设置步长和起始值
        SHOW SESSION VARIABLES LIKE 'auto_inc%';
        SET SESSION auto_increment_increment=2;
        SET SESSION auto_increment_offset=10;
        SHOW GLOBAL VARIABLES LIKE 'auto_inc%';
        SET GLOBAL auto_increment_increment=2;
        SET GLOBAL auto_increment_offset=10;
/* 主键 */
主键,一种特殊的唯一索引,不允许有空值,如果主键使用单个列,则它的值必须唯一,如果是多列,则其组合必须唯一
CREATE TABLE tablename(
	column_name type NOT NULL auto_increment PRIMARY KEY,
)
或
CREATE TABLE tablename(
	column_name type NOT NULL,
	PRIMARY KEY(column_name)
)
/* 外键 */
CREATE TABLE tablename(
	CONSTRAINT symbol FOREIGN KEY (id) REFERENCES table_child(id);
)
```

> 删除表

```mysql
DROP TABLE tablename;
```

> 清空表

```mysql
-- 如果清空的表又自增列,那么在清空之后会继续上次自增的值继续自增
DELETE FROM tablename;
-- 如果清空的表又自增列,那么在清空之后再次添加数据自增的值会从新开始计算
TRUNCATE TABLE tablename;
```

> 修改表

```mysql
-- 添加列
ALTER TABLE tablename ADD column_name column_type
-- 删除列
ALTER TABLE tablename DROP COLUMN column_name
-- 修改列
ALTER TABLE tablename MODIFY COLUMN column_name column_type;  -- 修改类型
ALTER TABLE tablename CHANGE originalname newname column_type; -- 修改列名与类型
-- 添加主键
ALTER TABLE tablename ADD PRIMARY KEY(columnname);
-- 删除主键
ALTER TABLE tablename DROP PRIMARY KEY;
ALTER TABLE tablename  MODIFY columnname INT, DROP PRIMARY KEY;
-- 添加外键
ALTER TABLE slave_table ADD CONSTRAINT symbol(ex:FK_slave_primary) FOREIGN KEY slave_table(foreign_key_field) REFERENCES primary_table(primary_field);
-- 删除外键
ALTER TABLE tablename DROP FOREIGN KEY foreign_key_field
-- 修改默认值
ALTER TABLE testalter_tbl ALTER i SET DEFAULT 1000;
-- 删除默认值
ALTER TABLE testalter_tbl ALTER i DROP DEFAULT;
```

实例在后续整理中续写