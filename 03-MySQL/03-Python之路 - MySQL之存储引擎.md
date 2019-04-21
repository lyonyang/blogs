# Python之路 - MySQL存储引擎

## 介绍  🍀

插件式存储引擎是MySQL数据库最重要的特性之一 , 用户可以根据应用的需要选择如何存储和索引数据 , 是否使用实务等 , MySQL默认支持多种**存储引擎(表类型)** , 用户还可以按照自己的需要定制和使用自己的存储引擎

MySQL 5.0支持的存储引擎包括MyISAM , InnoDB , BDB , MEMORY , MERGE , EXAMPLE , NDB Cluster , ARCHIVE , CSV , BLACKHOLE 等 , 其中InnoDB 和 BDB提供事物安全表 , 其他存储引擎都是非安全事物安全表

创建新表时如果不指定存储引擎 , 那么系统就会使用默认存储引擎 , MySQL 5.5 之前的默认存储引擎是`MyISAM`  , 5.5 之后改为了`InnoDB` , 如果修改默认的存储引擎 , 可以在参数文件中红设置 default-table-type 

查看当前默认存储引擎 , 可以使用以下命令 : 

```mysql
SHOW VARIABLES LIKE 'table_type';
```

查询当前数据库支持的存储引擎 , 可以使用一下命令 : 

```mysql
-- 第一种方法
SHOW ENGINES \G
-- 第二种方法
SHOW VARIABLES LIKE 'have%';
```

常用存储引擎对比

|   特点    | MyISAM | InnoDB | MEMORT | MERGE | NDB  |
| :-----: | :----: | :----: | :----: | :---: | :--: |
|  存储限制   |   有    |  64TB  |   有    |  没有   |  有   |
|  事物安全   |        |   支持   |        |       |      |
|   锁机制   |   表锁   |   行锁   |   表锁   |  表锁   |  行锁  |
|  B树索引   |   支持   |   支持   |   支持   |  支持   |  支持  |
|  哈希索引   |        |        |   支持   |       |  支持  |
|  全文索引   |   支持   |        |        |       |      |
|  集群索引   |        |   支持   |        |       |      |
|  数据缓存   |        |   支持   |   支持   |       |  支持  |
|  索引缓存   |   支持   |   支持   |   支持   |  支持   |  支持  |
|  数据可压缩  |   支持   |        |        |       |      |
|  空间使用   |   低    |   高    |  N/A   |   低   |  低   |
|  内存使用   |   低    |   高    |   中等   |   低   |  高   |
| 批量插入的速度 |   高    |   低    |   高    |   高   |  高   |
|  支持外键   |        |   支持   |        |       |      |

下面重点介绍最常使用的4中存储引擎 : MyISAM , InnoDB , MEMORY 和 MERGE


## MyISAM  🍀

MyISAM**不支持事务** , 也不支持外键 , 其优势是访问的速度快 , 对事务完整性没有要求或者以SELECT , INSERT为主的应用基本上都可以使用这个引擎来创建表

每个MyISAM在磁盘上存储成3个文件 , 其文件名都和表明相同 , 但扩展名分别是` .frm(存储表定义)` , `.MYD(MYDate , 存储数据)`  , ` .MYI(MYIndex , 存储索引)`  ; MyISAM的表还支持3种不同的存储格式 , 分别是 : 静态表(固定长度) , 动态表 , 压缩表

数据文件和索引文件可以放置在不同的目录 , 平局分布IO , 获得更快的速度 ; 不同MyISAM表的索引文件和数据文件可以放置到不同的路经下 , 文件路经要是绝对路经 , 并且具有访问权限

MyISAM类型的表可能会损坏 , 原因可能是多种多样的 , 损坏后的表可能不能被访问 , 会提示需要修复或者访问返回错误的结果 ; MyISAM类型的表提供修复的工具 , 可以用`CHECK TABLE`语句来检查MyISAM表的健康 , 并用REPAIR TABLE语句修复一个损坏的MyISAM表 .

MyISAM另一个与众不同的地方是 , 它的**缓冲池只缓存(cache)索引文件** **, 而不缓存数据文件** , 这与大多数的数据库都不相同


## InnoDB  🍀

InnoDB存储引擎提供了具有提交 , 回滚和崩溃恢复能力的事务安全 , 但是对比MyISAM , InnoDB写的处理效率差一些 , 并且会占用更多的磁盘空间以保留数据和索引

InnoDB是MySQL数据库最为常用的存储引擎 , 其不同于其他存储引擎的表的特点如下


### 自动增长列  🍀

InnoDB表的自增列可以手工插入 , 但是插入的值如果是空或者0 , 则实际插入的将是自动增长后的值

自增实例

```mysql
mysql> USE mydatabase;
Database changed
mysql> CREATE TABLE autoincre_demo(
    -> id int NOT NULL AUTO_INCREMENT,  -- 设置id列自增
    -> name varchar(10),
    -> PRIMARY KEY(id)  -- 将id列设为主键
    -> )ENGINE=InnoDB;
Query OK, 0 rows affected (0.28 sec)
/* 插入数据 */
mysql> INSERT INTO autoincre_demo VALUES(1,'lyon'),(0,'leon'),(NULL,'kenneth');
Query OK, 3 rows affected (0.11 sec)
Records: 3  Duplicates: 0  Warnings: 0
/* 查看表 */
mysql> SELECT * FROM autoincre_demo;
+----+---------+
| id | name    |
+----+---------+
|  1 | lyon    |
|  2 | leon    |
|  3 | kenneth |
+----+---------+
3 rows in set (0.00 sec)
```

PS : 可以通过`ALTER TABLE *** AUTO_INCREMENT = n;` 语句强制设置自动增长列的初始值 , 默认从1开始 , 但是该强制的默认值是保留在内存中的 , 如果该值在使用之前数据库重新启动 , 那么这个强制的默认值就会丢失 , 就需要在数据库启动以后重新设置

可以使用`LAST_INSERT_ID()` 查询当前线程最后插入记录使用的值 , 如果一次插入多条记录 , 则返回第一条记录使用的自动增长值

LAST_INSERT_ID()实例

```mysql
/* 从1开始,所以自增值为2 */
mysql> SELECT LAST_INSERT_ID();
+------------------+
| LAST_INSERT_ID() |
+------------------+
|                2 |
+------------------+
1 row in set (0.00 sec)
/* 再插3条 */
mysql> INSERT INTO autoincre_demo(name) VALUES('FIVE'),('SIX'),('SEVEN');
Query OK, 3 rows affected (0.12 sec)
Records: 3  Duplicates: 0  Warnings: 0
/* 默认开始有3条,所以自增值为5 */
mysql> SELECT LAST_INSERT_ID();
+------------------+
| LAST_INSERT_ID() |
+------------------+
|                5 |
+------------------+
1 row in set (0.00 sec)
```

**对于InnoDB表 , 自动增长列必须是索引(主键) , 如果是组合索引 , 也必须是组合索引的第一列**

但是对于MyISAM表 , 自增列可以是组合索引的其他列


### 外键约束  🍀

MySQL支持外键的存储引擎只有InnoDB , 在创建外键的时候 , 要求父表必须有对应的索引 , 子表在创建外键的时候也会自动创建对应的索引

实例

```mysql
/* 创建父表country */
mysql> CREATE TABLE country(
    -> country_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,  -- 创建自增列(索引)
    -> country VARCHAR(50) NOT NULL,
    -> last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,  -- 最后更新时间
    -> PRIMARY KEY (country_id) -- 设置主键索引
    -> )ENGINE=InnoDB DEFAULT CHARSET=utf8;
Query OK, 0 rows affected (0.32 sec)
/* 创建子表city */
mysql> CREATE TABLE city(
    -> city_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,  -- 创建自增列
    -> city VARCHAR(50) NOT NULL,
    -> country_id SMALLINT UNSIGNED NOT NULL,  -- 外键
    -> last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    -> PRIMARY KEY (city_id),  -- 设置主键索引
    -> KEY idx_fk_country_id (country_id),
    -> CONSTRAINT fk_city_country FOREIGN KEY (country_id) REFERENCES country (country_id) ON DELETE RESTRICT ON UPDATE CASCADE  -- 设置外键,对应country表的主键country_id
    -> )ENGINE=InnoDB DEFAULT CHARSET=utf8;
Query OK, 0 rows affected (0.40 sec)
```

在创建索引时 , 可以指定在删除 , 更新父表时 , 对子表进行的相应操作 , 包括RESTRICT , CASCADE , SET NULL 和 NO ACTION . 

其中`RESETRICT` 和 `NO ACTION` 相同 , 是指限制在子表有关联记录的情况下父表不能更新 ; CASCADE表示父表在更新或者删除时 , 更新或者删除子表对应记录 ; 

`SET NULL` 则表示父表在更新或者删除的时候 , 子表的对应字段被设置为NULL

```mysql
/* 子表的外键指定是 ON DELETE RESTRICT ON UPDATE CASCADE 方式,即主表删除记录时,如果子表有对应记录,则不允许删除,主表在更新记录时,如果子表有对应记录,则子表对应更新 */
-> CONSTRAINT fk_city_country FOREIGN KEY (country_id) REFERENCES country (country_id) ON DELETE RESTRICT ON UPDATE CASCADE
```

**当某个表被其他表创建了外键参照 , 那么该表的对应索引或者主键禁止被删除**

> 关闭外键 

在导入多个表的数据时 , 如果需要忽略表之前的导入顺序 , 可以暂时关闭外键的检查 ; 在执行LOAD DATE 和 ALTER TABLE操作的时候 , 可以通过暂时关闭外键约束来加快处理的速度

关闭命令 : `SET FOREIGN_KEY_CHECKS = 0; ` 打开外键则将0改为1即可

> 查看外键信息

命令 :  `SHOW CREATE TABLE`或者`SHOW TABLE STATUS` 

实例 : 

```mysql
mysql> SHOW TABLE STATUS LIKE 'city' \G;
*************************** 1. row ***************************
           Name: city
         Engine: InnoDB
        Version: 10
     Row_format: Dynamic
           Rows: 0
 Avg_row_length: 0
    Data_length: 16384
Max_data_length: 0
   Index_length: 16384
      Data_free: 0
 Auto_increment: 1
    Create_time: 2017-10-18 17:16:18
    Update_time: NULL
     Check_time: NULL
      Collation: utf8_general_ci
       Checksum: NULL
 Create_options:
        Comment:
1 row in set (0.01 sec)

ERROR:
No query specified
```


### 存储方式  🍀

InnoDB存储表和索引有两种方式 : 

- 使用共享表空间存储
- 使用多表空间存储 , 需要设置参数 innodb_file_per_table , 并且重新启动才生效

对于表中数据的存储 , InnoDB 存储引擎采用了聚集(clustered)的方式 , 每张表都是按主键的顺序进行存储的 , 如果没有显式地在表定义时指定主键 , InnoDB 存储引擎会为每一行生成一个 6 字节的 ROWID , 并以此作为主键

深入了解InnoDB存储引擎的工作 , 原理 , 实现和应用 , 可以参考《MySQL技术内幕 : InnoDB存储引擎》一书


## MEMORY  🍀

MEMORY存储引擎使用存在于内存中的内容来创建表

每个MEMORY表只实际对应一个磁盘文件 , 格式是`.frm`  , MEMORY类型的表访问非常地快 , 因为它的数据是存放在内存中的 , 并且默认使用HASH索引 , 但是一旦服务关闭 , 表中的数据就会丢失

给MEMORY创建索引的时候 , 可以指定使用HASH索引还是BTREE索引

实例

```mysql
mysql> CREATE TABLE tab_memory ENGINE=MEMORY
    ->   SELECT city_id,city,country_id
    ->   FROM city GROUP BY city_id;
Query OK, 0 rows affected (0.07 sec)
Records: 0  Duplicates: 0  Warnings: 0

mysql> CREATE INDEX mem_hash USING HASH ON tab_memory(city_id);
Query OK, 0 rows affected (0.10 sec)
Records: 0  Duplicates: 0  Warnings: 0

mysql> SHOW INDEX FROM tab_memory \G;
*************************** 1. row ***************************
        Table: tab_memory
   Non_unique: 1
     Key_name: mem_hash
 Seq_in_index: 1
  Column_name: city_id
    Collation: NULL
  Cardinality: 0
     Sub_part: NULL
       Packed: NULL
         Null:
   Index_type: HASH
      Comment:
Index_comment:
1 row in set (0.00 sec)

ERROR:
No query specified
```

服务器需要足够内存来维持所有在同一时间使用的MEMORY表  , 当不再需要MEMOY表的内容之时 , 要释放被MEMORY表使用的内存 , 应该执行DELETE FROM 或TRUNCATE TABLE , 或者整个地删除(使用DROP TABLE操作)

MEMORY类型的存储引擎主要用于那些内容变化不频繁的代码表 , 或者作为统计操作的中间结果表 , 便于高效地对中间结果进行分析并得到最终的统计结果 ; 对存储引擎为MEMORY的表进行更新操作要谨慎 , 因为数据并没有实际写入到磁盘中 , 所以一定要对下次重新启动服务后如何获得这些修改后的数据有所考虑


## MERGE  🍀

MERGE存储是一组MyISAM表的组合 , 这些MyISAM表必须结构完全相同 ,  MERGE表本身并没有数据 ,  对MERGE类型的表可以进行查询 , 更新 , 删除操作 , 这些操作实际上是对内部的MyISAM表进行的

可以对MERGE表进行DROP操作 , 这个操作只是删除MERGE的定义 , 对内部的表没有任何的影响

通常我们使用MERGE表来透明地对多个表进行查询和更新操作 , 而对按照时间记录的操作日志则可以透明地进行插入操作


## TokuDB  🍀

前面的都是MySQL自带的存储引擎 , 除了这些之外 , 还有一些常见的第三方存储引擎 , 在某些特定应用中也有广泛使用 , 比如列式存储引擎Infobright , 高写性能高压缩的TokuDB就是其中非常有代表性的两种

TokuDB是一个高性能 , 支持事务处理的MySQL和MariaDB的存储引擎 , 具有高扩展性 , 高压缩率 , 高效的写入性能 , 支持大多数在线DDL操作 

主要特性 : 

- 使用Fractal树索引保证高效的插入性能
- 优秀的压缩特性 , 比InnoDB高近10倍
- Hot Schema Changes 特性支持在线创建索引和添加 , 删除属性列等DDL操作
- 使用Bulk Loader达到快速加载大量数据
- 提供了主从延迟消除技术
- 支持ACID和MVCC

适用场景 : 

- 日志数据 , 因为日志通常插入频繁切存储量大
- 历史数据 , 通常不会再有写操作 , 可以利用TokuDB的高压缩特性进行存储
- 在线DDL较频繁的场景 , 使用TokuDB可以大大增加系统的可用性




