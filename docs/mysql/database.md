# MySQL - 库操作








<extoc></extoc>

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


## 数据库操作

在MySQL数据中有如下默认数据库

| 默认数据库              | 描述                                       |
| ------------------ | ---------------------------------------- |
| information_schema | 虚拟库 , 不占用磁盘空间 , 存储的是数据库启动后的一些参数 , 如用户表信息 , 列信息 , 权限信息 , 字符信息等 |
| test               | 用户用来测试的数据库 (MySQL 5.7没有)                 |
| mysql              | 授权库 , 主要存储系统用户的权限信息                      |
| performance_schema | MySQL 5.5 后新增的 , 主要用于收集数据库服务器性能参数 , 记录处理查询请求时发生的各种事件 , 锁等现象 |
| sys                | 包含了一系列视图、函数和存储过程                         |


### 查看数据库

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


### 创建数据库

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


### 删除数据库

```mysql
DROP DATABASE dbname; 删除数据库
```

### 使用数据库

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


### 用户管理

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


### 授权管理

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

