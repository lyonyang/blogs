# SQL优化

## 一般步骤

MySQL 客户端连接成功后 , 通过

```MySQL
mysql> show [session|global]status
```

可以提供服务器状态信息 , 也可以在操作系统上使用 `mysqladmin extended-status` 命令获得这些消息 

对于 `session` 与 `global` 参数 : 

- session : 显示当前连接的统计结果 , 默认使用session
- global : 显示自数据库上次启动至今的统计结果

示例

```mysql
mysql> show status like 'Com_%';
+-----------------------------+-------+
| Variable_name               | Value |
+-----------------------------+-------+
| Com_admin_commands          | 0     |
| Com_assign_to_keycache      | 0     |
| Com_alter_db                | 0     |
| Com_alter_db_upgrade        | 0     |
| Com_alter_event             | 0     |
| Com_alter_function          | 0     |
| Com_alter_instance          | 0     |
| Com_alter_procedure         | 0     |
| Com_alter_server            | 0     |
| Com_alter_table             | 0     |
...
```

`Com_xxx` 表示每个 xxx 语句执行的次数 , 我们通常比较关心以下几个统计参数 : 

- Com_select : 执行 `SELECT` 操作的次数 , 一次查询只累加 1
- Com_insert : 执行 `INSERT` 操作的次数 , 对于批量插入的 `INSERT` 操作 , 只累加一次
- Com_update : 执行 `UPDATE` 操作的次数
- Com_delete : 执行 `DELETE` 操作的次数

以上 4 个参数对于所有存储引擎的表操作都会进行累加 , 下面这几个参数只是针对 `InnoDB` 存储引擎的 , 累加的算法也略有不同 :

- Innodb_rows_read : `SELECT` 查询返回的行数
- Innodb_rows_inserted : 执行 `INSERT` 操作插入的行数
- Innodb_rows_upddated : 执行 `UPDATE` 操作更新的行数
- Innodb_rows_deleted : 执行 `DELETE` 操作删除的行数

通过以上几个参数 , 可以容易地了解当前数据库的应用是以插入更新为主还是以查询操作为主 , 以及各种类型的 SQL 大致的执行比例是多少 ; 对于更新操作的技术 , 是对执行次数的技术 , 不论提交还是回滚都会进行累加

对于事务型的应用 , 通过 Com_commit 和 Com_rollback 可以了解事务提交和回滚的情况 , 对于回滚操作非常频繁的数据 , 可能意味着应用编写存在问题 , 此外还有几个参数便于用户了解数据库的基本情况 : 

- Connections : 视图连接 MySQL 服务器的次数
- Uptime : 服务器工作时间
- Slow_queries : 慢查询的次数

## 定位低效SQL

有两种方式定位执行效率较低的 SQL : 

1. 通过慢查询日志定位那些执行效率较低的 SQL 语句 , 用 `--log-slow-queries[= file_name]` 选项启动时 , mysqld 写一个包含所有执行时间超过 `long_query_time` 秒的 SQL 语句的日志文件
2. 慢查询日志在查询结束以后才记录 , 所以在应用反映执行效率出现问题的时候查询慢查询日志并不能定位问题 , 可以使用 `show processlist` 命令查看当前 MySQL 在进行的线程 , 包括线程的状态 , 是否锁表等 , 可以实时地查看 SQL 的执行情况 , 同时对一些锁表操作进行优化

## EXPLAIN分析低效SQL

通过上一步定位效率低的 SQL 语句后 , 可以通过 EXPLAIN 或者DESC 命令获取 MySQL 如何执行 SELECT 语句的信息 , 包括在 SELECT 语句执行过程中表如何连接和连接的顺序 , 比如想统计某个 email 为租赁电影拷贝所支付的总金额 , 需要关联客户表 customer 和付款表 payment , 并且对付款金额 amount 字段做求和 (sum) 操作 , 相应的 SQL 执行计划如下 : 

```mysql
mysql>explain select sum(amount) from custoer a, payment b where l=l and a.customer_id = b.customer_id and email = 'lyon.yang@qq.com'\G;
*************************** 1. row ***************************
           id: 1
  select_type: SIMPLE
        table: a
         type: ALL
possible_keys: PRIMARY
          key: NULL
      key_len: NULL
          ref: NULL
         rows: 583
        Extra: Using where
*************************** 2. row ***************************
           id: 1
  select_type: SIMPLE
        table: b
         type: ref
possible_keys: idx_fk_customer_id
          key: idx_fk_customer_id
      key_len: 2
          ref: sakila.a.customer_id
         rows: 12
        Extra: 
2 rows in set (0.00 sec)
```

参数说明 : 

- select_type : 表示 SELECT 的类型 , 常见的取值有 SIMPLE (简单表 , 即不使用表连接或者子查询) , PRIMARY (主查询 , 即外层的查询) , UNION (UNION 中的第二个或者后面的查询语句) , SUBQUERY (子查询中的第一个 SELECT ) 等

- table : 输出结果集的表

- type : 表示 MySQL 在表中找到所需行的方式 , 或者叫访问类型 , 常见类型有 : 

  ```mysql
  # 从左至右,性能由最差到最好
  +------+--------+-------+-----+--------+--------------+------+
  |  ALL |  index | range | ref | eq_ref | const,system | NULL |
  +------+--------+-------+-----+--------+--------------+------+
  ```

  - ALL : 全表扫描 , MySQL 遍历全表来找到匹配的行 

    ```mysql
    # type=ALL
    explain select * from film where rating > 9\G;
    ```

  - index : 索引全扫描 , MySQL 遍历整个索引来查询匹配的行

    ```mysql
    # type=index
    explain select title from film\G;
    ```

  - range : 索引范围扫描 , 常见与< , <= , > , >= , between 等操作符

    ```mysql
    # type=range
    explain select * from payment where customer_id >= 300 and customer_id <= 350\G;
    ```

  - ref : 使用非唯一索引扫描或唯一索引的前缀扫描 , 返回匹配某个单独值的记录行

    ```mysql
    # type=ref
    explain select * from payment where customer_id = 350\G;
    ```

  - eq_ref : 类似 ref , 区别就在使用的索引是唯一索引 , 对于每个索引键值 , 表中只有一条记录匹配 ; 简单来说 , 就是多表连接中使用主键或者联合索引作为关联条件

    ```mysql
    # type=eq_ref
    explain select * from film a, film_text b where a.film_id = b.film_id\G;
    ```

  - const/system : 单表中最多有一个匹配行 , 查询起来非常迅速 , 所以这个匹配行中的其他列的值可以被优化器在当前查询中当做常量来处理 , 如 , 根据主键或唯一索引进行的查询

    ```mysql
    # type=const/system
    explain select * from (select * from customer where email='lyon.yang@qq.com')a\G;
    ```

  - NULL : MySQL 不用访问表或者索引 , 直接就能得到结果

    ```mysql
    # type=NULL
    explain select 1 from dual where 1\G;
    ```

  type 还有其他值 , 如 ref_or_null (与 ref 类似 , 区别在于条件中包含对 NULL 的查询) , index_merge (索引合并优化) , unique_subquery (in 的后面是一个查询主键字段的子查询) , index_subquery (与 unique_subquery 类似 , 区别在于 in 的后面是查询非唯一索引字段的子查询)

- possible_keys : 表示查询时可能使用的索引

- key : 表示实际使用的索引

- key_len : 使用到索引字段的长度

- rows : 扫描行的数量

- Extra : 执行情况的说明和描述 , 包含不适合在其他列中显示但是对执行计划非常重要的额外信息

## show profile分析SQL

查看是否支持 profile

```mysql
mysql> select @@have_profiling;
+------------------+
| @@have_profiling |
+------------------+
| YES              |
+------------------+
1 row in set, 1 warning (0.00 sec)
```

默认 profiling 是关闭的 , 在 Session 级别开启 profiling : 

```mysql
mysql> select @@profiling;
+-------------+
| @@profiling |
+-------------+
|           0 |
+-------------+
1 row in set, 1 warning (0.00 sec)

mysql> set profiling=1;
Query OK, 0 rows affected, 1 warning (0.05 sec)

mysql> select @@profiling;
+-------------+
| @@profiling |
+-------------+
|           1 |
+-------------+
1 row in set, 1 warning (0.00 sec)
```

通过 `show profiles` 语句可以查看 SQL 的 Query ID : 

```mysql
mysql> show profiles;
+----------+------------+--------------------+
| Query_ID | Duration   | Query              |
+----------+------------+--------------------+
|        1 | 0.00050550 | select @@profiling |
+----------+------------+--------------------+
1 row in set, 1 warning (0.00 sec)
```

通过 `show profile for query` 语句查看执行过程中线程的每个状态和消耗的时间

```mysql
mysql> show profile for query 1;
+----------------------+----------+
| Status               | Duration |
+----------------------+----------+
| starting             | 0.000081 |
| checking permissions | 0.000005 |
| Opening tables       | 0.000004 |
| init                 | 0.000009 |
| optimizing           | 0.000336 |
| executing            | 0.000012 |
| end                  | 0.000004 |
| query end            | 0.000004 |
| closing tables       | 0.000003 |
| freeing items        | 0.000036 |
| cleaning up          | 0.000013 |
+----------------------+----------+
11 rows in set, 1 warning (0.03 sec)
```