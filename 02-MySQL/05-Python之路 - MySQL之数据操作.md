# Python之路 - MySQL之数据操作
<!-- TOC -->

- [Python之路 - MySQL之数据操作](#python之路---mysql之数据操作)
    - [介绍  🍀](#介绍--🍀)
    - [插入记录  🍀](#插入记录--🍀)
    - [更新记录  🍀](#更新记录--🍀)
    - [删除记录  🍀](#删除记录--🍀)
    - [查询记录  🍀](#查询记录--🍀)
        - [查询不重复的记录  🍀](#查询不重复的记录--🍀)
        - [条件查询  🍀](#条件查询--🍀)
        - [排序和限制   🍀](#排序和限制---🍀)
        - [聚合  🍀](#聚合--🍀)
        - [表连接  🍀](#表连接--🍀)
        - [子查询  🍀](#子查询--🍀)
        - [记录联合  🍀](#记录联合--🍀)

<!-- /TOC -->
## 介绍  🍀

DML操作是指对数据库中表记录的操作 , 即数据操作

主要包括表记录的插入(insert) , 更新(update) , 删除(delete) 和查询(select) , 是开发人员日常使用最频繁的操作

## 插入记录  🍀

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

<!-- TOC -->
[**返回顶部**](#python之路---mysql之数据操作)
<!-- /TOC -->

## 更新记录  🍀

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

<!-- TOC -->
[**返回顶部**](#python之路---mysql之数据操作)
<!-- /TOC -->

## 删除记录  🍀

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

<!-- TOC -->
[**返回顶部**](#python之路---mysql之数据操作)
<!-- /TOC -->

## 查询记录  🍀

语法 : 

```mysql
SELECT * FROM tablename [WHERE CONDITION];
```

"*"表示要将所有的记录都选出来 , 也可以用逗号分割所有的字段来代替

如上面例子中

```mysql
mysql> SELECT ename,hiredate,sal,deptno FROM emp;
```

<!-- TOC -->
[**返回顶部**](#python之路---mysql之数据操作)
<!-- /TOC -->

### 查询不重复的记录  🍀

```mysql
mysql> SELECT DISTINCT deptno FROM emp;
+--------+
| deptno |
+--------+
|      1 |
+--------+
1 row in set (0.00 sec)
```

<!-- TOC -->
[**返回顶部**](#python之路---mysql之数据操作)
<!-- /TOC -->

### 条件查询  🍀

```mysql
mysql> SELECT * FROM emp WHERE deptno=1;
+-------+------------+-----------+--------+
| ename | hiredate   | sal       | deptno |
+-------+------------+-----------+--------+
| lyon  | 2000-01-01 | 100000.00 |      1 |
+-------+------------+-----------+--------+
1 row in set (0.00 sec)
```

<!-- TOC -->
[**返回顶部**](#python之路---mysql之数据操作)
<!-- /TOC -->

### 排序和限制   🍀

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

<!-- TOC -->
[**返回顶部**](#python之路---mysql之数据操作)
<!-- /TOC -->

### 聚合  🍀

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

<!-- TOC -->
[**返回顶部**](#python之路---mysql之数据操作)
<!-- /TOC -->

### 表连接  🍀

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


<!-- TOC -->
[**返回顶部**](#python之路---mysql之数据操作)
<!-- /TOC -->

### 子查询  🍀

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

<!-- TOC -->
[**返回顶部**](#python之路---mysql之数据操作)
<!-- /TOC -->

### 记录联合  🍀

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

<!-- TOC -->
[**返回顶部**](#python之路---mysql之数据操作)
<!-- /TOC -->
