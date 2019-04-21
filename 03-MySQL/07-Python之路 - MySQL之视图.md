# Python之路 - MySQL之视图

## 介绍  🍀

视图是一种虚拟存在的表 , 对于使用视图的用户来说基本上是透明的 

视图并不在数据库中实际存在 , 行和列数据来自定义视图的查询中使用的表 , 并且是在使用视图时动态生成的

视图相对于普通的表的优势主要包括一下几点 : 

- 简单 : 使用视图的用户完全不需要关心后面对应的表的结构 , 关联条件和筛选条件 , 对用户来说已经是过滤好的复杂条件的结果集
- 安全 : 使用视图的用户只能访问他们被允许查询的结果集 , 对表的权限管理并不能限制到某个行某个列 , 但是通过视图就可以简单的实现
- 数据独立 : 一旦视图的结构确定了 , 可以屏蔽表结构变化对用户的影响 , 源表增加列对视图没有影响 ; 源表修改列名 , 则可以通过修改视图来解决 , 不会造成对访问者的影响 

## 视图操作  🍀

视图的操作包括创建或者修改视图 , 删除视图 , 以及查看视图定义

### 创建视图  🍀

创建视图需要有`CREATE VIEW `的权限 , 并且对于查询涉及的列有`SELECT`权限 ; 如果使用`CREATE OR REPLACE `或者`ALTER`修改视图 , 那么还需要该视图的DROP权限

语法 : 

```mysql
-- 创建视图
CREATE VIWE 视图名称 AS SQL语句

-- 完整
CREATE [OR REPLACE] [ALGORITHM = {UNDEFINED|MERGE|TEMPTABLE}]
	VIEW view_name [(column_list)]
	AS select_statement
	[WITH [CASCADED|LOCAL] CHECK OPTION]
```

实例

```mysql
mysql> CREATE VIEW lyon_view AS SELECT * FROM test;
Query OK, 0 rows affected (0.08 sec)
/* 注意 : 
MySQL视图的定义有一些限制,例如,在FROM关键字后面不能包含子查询,这和其他数据库是不同的
如果视图是从其他数据库迁移过来的,那么可能需要因此做一些改动,可以将子查询的内容先定义成
一个视图,然后对该视图再创建视图就可以实现类似的功能了
```

再次注意 : 

1. 使用视图后无需每次都重写子查询的sql , 但是这样效率并不高 , 还不如我们写子查询的效率高
2. 一个致命的问题 : 视图是存放在数据库中的 , 如果我们程序中的sql过分依赖于数据库中存放的视图 , 那么意味着 , 一旦sql需要修改且涉及到视图的部分 , 则必须去数据库中进行修改 , 而通常在公司中数据库有专门的DBA负责 , 你要想完成修改 , 必须付出大量的沟通成本DBA可能才会帮你完成修改 , 极其的不方便


### 修改视图  🍀

语法 : 

```mysql
-- 修改视图 
ALTER VIEW 视图名称 AS SQL语句

-- 完整如下
ALTER [ALGORITHM = {UNDEFINED|MERGE|TEMPTABLE}]
	VIEW view_name [(column_list)]
	AS select_statement
	[WITH [CASCADED|LOCAL] CHECK OPTION]
```

实例

```mysql
mysql> ALTER VIEW lyon_view AS SELECT * FROM test WHERE id > 4;
Query OK, 0 rows affected (0.09 sec)
```

**视图的可更新性**

对于视图中的数据 , 由于视图是虚拟的 , 所以如果更新数据那么原始表也跟着被更新 , 即视图的可更新性

视图的可更新性和视图中查询的定义有关 , 一下类型的视图是不可更新的 : 

- 包含一下关键字的SQL语句 : 聚合函数(SUM , MIN , MAX , COUNT等) , DISTINCT , GROUP BY , HAVING , UNION 或者 UNION ALL
- 常量视图
- SELECT中包含子查询
- JION
- FROM一个不能更新的视图
- WHERE字句的子查询引用了FROM字句中的表

实例

```mysql
-- 包含聚合函数
mysql> CREATE OR REPLACE VIEW payment_sum AS
	-> SELECT staff_id,SUM(count) FROM payment GROUP BY staff_id;
Query OK, 0 rows affected(0.00 sec)
-- 常量视图
mysql> CREATE OR REPLACE VIEW pi AS
	-> SELECT 3.1415926 AS pi;
Query OK, 0 rows affected(0.00 sec)
-- select中包含子查询
mysql> CREATE VIEW city_view AS
	-> SELECT (SELECT city FROM city WHERE city_id = 1);
Query OK, 0 rows affected(0.00 sec)
```

*`[WITH [CASCADED|LOCAL] CHECK OPTION]`*

该语句决定了是否允许更新数据使记录不再满足视图的条件 , 其中 : 

- LOCAL只要满足本视图的条件就可以更新
- CASCADED则必须满足所有针对该视图的所有视图的条件才可以更新

默认为CASCADED

实例

```mysql
mysql> CREATE OR REPLACE VIEW payment_view AS
	-> SELECT payment_id,amount FROM payment
	-> WHERE amount < 10 WITH CHECK OPTION;
Query OK, 0 rows affected (0.00 sec)

mysql> CREATE OR REPLACE VIEW payment_view1 AS
	-> SELECT payment_id,amount FROM payment_view
	-> WHERE amount < 5 WITH LOCAL CHECK OPTION;
Query OK, 0 rows affected (0.00 sec)

mysql> CREATE OR REPLACE VIEW payment_view2 AS
	-> SELECT payment_id,amount FROM payment_view
	-> WHERE amount > 5 WITH CASCADED CHECK OPTION;
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT * FROM payment_view1 limit 1;
+------------+--------+
| payment_id | amount |
+------------+--------+
| 3          | 5.99   | 
+------------+--------+
1 row in set (0.00 sec)

mysql> UPDATE payment_view1 SET amount=10
	-> WHERE payment_id = 3;
Query OK, 1 row affected (0.03 sec)
Rows matched: 1 changed: 1 warnings: 0

mysql> UPDATE payment_view2 SET amount=10
	-> WHERE payment_id = 3;
ERROR 1369 (HY000): CHECK OPTION failed 'sakila.payment_view2'
```


### 删除视图  🍀

用户可以一次删除一个或者多个视图 , 前提是必须有该视图的DROP权限

语法 : 

```mysql
-- 删除视图
DROP VIEW view_name

-- 完整如下
DROP VIEW [IF EXISTS] view_name [,view_name]...[RESTRICT|CASCADE];
```


### 查看视图  🍀

从MySQL 5.1开始 , 使用SHOW TABLES命令的时候不仅显示表的名字 , 同时也会显示视图的名字 , 而不存在单独显示视图的SHOW VIEWS命令 , 如下 : 

```mysql
mysql> SHOW TABLES;
+----------------------+
| Tables_in_mydatabase |
+----------------------+
| ...                  |
| salary_view          |
| ...                  |
+----------------------+
11 rows in set (0.00 sec)
```

同样使用SHOW TABLE STATUS命令时 , 不但可以显示表的信息 , 同时也可以显示视图的信息

```mysql
SHOW TABLE STATUS LIKE 'view_name' \G;
```

查询某个视图的定义

```mysql
SHOW CREATE VIEW view_name \G;
```

通过查看系统表information_schema.views也可以查看视图的相关信息

```mysql
SELECT * FROM VIEWS WHERE table_name = 'view_name' \G;
```



