# Python之路 - MySQL表操作

## 介绍  🍀

该部分语句属于DDL语句 , 对表的定义 , 结构的修改 

与DML语句的区别在于 , DML语句仅对表内部数据进行操作 , 即数据的增删改查

DDL语句更多地由数据库管理员(DBA)使用 , 开发人员一般很少使用

## 创建表  🍀

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


## 删除表  🍀

```mysql
mysql> DROP TABLE tb;
Query OK, 0 rows affected (0.21 sec)
```


## 修改表  🍀

### 修改表类型  🍀

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


### 增加表字段  🍀

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


### 删除表字段  🍀

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


### 字段改名  🍀

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


### 修改字段排列顺序  🍀

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

**PS :** CHANGE/FIRST|AFTER COLUMN 这些关键字都属于MySQL在标准SQL上的扩展 , 在其他数据库上不一定适用


### 更改表名  🍀

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


### 默认值  🍀

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


## 语句合集  🍀

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

