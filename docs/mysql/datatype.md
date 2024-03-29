# MySQL - 基本数据类型








<extoc></extoc>

## 介绍

MySQL中定义数据字段的类型对数据库的优化是非常重要的

MySQL支持多种数据类型 , 主要包括 : 

1. 数值类型
2. 日期时间类型
3. 字符串类型

本篇内容 , 以MySQL 5.0 版本为例 , 因为不同的版本可能有所差异 , 不过差异不大

## 数值类型

MySQL支持所有标准SQL中的数值类型 , 其中包括严格数值类型 , 以及近似数值数据类型 , 并在此基础上做了扩展 , 增加了TINYINT , MEDIUMINT , BIGINT 3种长度不同的整型 , 并增加了BIT类型 , 用来存放位数据 

> 整数类型介绍

| 整数类型          | 字节   | 最小值                                   | 最大值                                      |
| ------------- | ---- | ------------------------------------- | ---------------------------------------- |
| TINYINT       | 1    | 有符号 : -128 <br>无符号 : 0                | 有符号 : 127<br>无符号 : 255                   |
| SMALLINT      | 2    | 有符号 : -32768<br>无符号 : 0               | 有符号 : 32767<br>无符号 : 65535               |
| MEDIUMINT     | 3    | 有符号 : -8388608<br>无符号 : 0             | 有符号 : 8388607<br>无符号 : 1677215           |
| INT , INTEGER | 4    | 有符号 : -2147483648<br>无符号 : 0          | 有符号 : 2147483647<br>无符号 : 4294967295     |
| BIGINT        | 8    | 有符号 : -9223372036854775808<br>无符号 : 0 | 有符号 : 9223372036854775807<br>无符号 : 18446744073709551615 |

> 浮点数类型介绍

| 浮点数类型  | 字节   | 最小值                      | 最大值                      |
| ------ | ---- | ------------------------ | ------------------------ |
| FLOAT  | 4    | ±1.175494351E-38         | ±3.402823466E+38         |
| DOUBLE | 8    | ±2.2250738585072014E-308 | ±1.7976931348623157E+308 |

> 定点数类型介绍

| 定点数类型                           | 字节    | 描述                                       |
| ------------------------------- | ----- | ---------------------------------------- |
| DEC (M , D) <br>DECIMAL (M , D) | M + 2 | 最大取值范围与DOUBLE相同 , 给定DECIMAL的有效取值范围由 M 和 D 决定 |

> 位类型介绍

| 位类型     | 字节   | 最小值     | 最大值      |
| ------- | ---- | ------- | -------- |
| BIT (M) | 1~8  | BIT (1) | BIT (64) |

特别的 : MySQL中无布尔值 , 可以使用TINYINT(1)构造 , 0为假非0为真 , 如下 : 

```mysql
mysql> SELECT IF(0, 'true', 'false');
+------------------------+
| IF(0, 'true', 'false') |
+------------------------+
| false                  |
+------------------------+
1 row in set (0.00 sec)
mysql> SELECT IF(1, 'true', 'false');
+------------------------+
| IF(1, 'true', 'false') |
+------------------------+
| true                   |
+------------------------+
1 row in set (0.00 sec)
```

但是真假的值只有1和0 , 而不是非0的值都为真 , 如下 : 

```mysql
mysql> SELECT IF(0 = FALSE, 'true', 'false');
+--------------------------------+
| IF(0 = FALSE, 'true', 'false') |
+--------------------------------+
| true                           |
+--------------------------------+
1 row in set (0.01 sec)
mysql> SELECT IF(1 = TRUE, 'true', 'false');
+-------------------------------+
| IF(1 = TRUE, 'true', 'false') |
+-------------------------------+
| true                          |
+-------------------------------+
1 row in set (0.00 sec)
mysql> SELECT IF(2 = TRUE, 'true', 'false');
+-------------------------------+
| IF(2 = TRUE, 'true', 'false') |
+-------------------------------+
| false                         |
+-------------------------------+
1 row in set (0.00 sec)
mysql> SELECT IF(2 = FALSE, 'true', 'false');
+--------------------------------+
| IF(2 = FALSE, 'true', 'false') |
+--------------------------------+
| false                          |
+--------------------------------+
1 row in set (0.00 sec)
```


## 日期时间类型

MySQL中有多种数据类型可以用于日期和时间的表示 , 这些数据类型的主要区别如下 : 

- 表示年月日 , 通常用DATE来表示
- 表示年月日时分秒 , 通常用DATETIME表示
- 只表示时分秒 , 通常用TIME来表示

> 日期和时间类型介绍

| 日期和时间类型   | 字节   | 最小值                     | 最大值                     |
| --------- | ---- | ----------------------- | ----------------------- |
| DATE      | 4    | 1001-01-01              | 9999-12-31              |
| DATETIME  | 8    | 1000-01-01 00 : 00 : 00 | 9999-12-31 23 : 59 : 59 |
| TIMESTAMP | 4    | 19700101080001          | 2038年的某个时刻              |
| TIME      | 3    | -838 : 59 : 59          | 838 : 59 : 59           |
| YEAR      | 1    | 1901                    | 2155                    |

每种日期时间类型都有一个有效值范围 , 如果超出这个范围 , 在默认的SQLMode下 , 系统会进行错误提示 , 并将以零值来进行存储 , 不同日期类型零值的表示如下 : 

> 日期和时间类型的零值表示

| 数据类型      | 零值表示                    |
| --------- | ----------------------- |
| DATETIME  | 0000-00-00 00 : 00 : 00 |
| DATE      | 0000-00-00              |
| TIMESTAMP | 00000000000000          |
| TIME      | 00 : 00 : 00            |
| YEAR      | 0000                    |


## 字符串类型

MySQL包括了CHAR , VARCHAR , BINARY , VARBINARY , BLOB , TEXT , ENUM 和 SET等多种字符串类型

> 字符串类型介绍

| 字符串类型        | 字节   | 描述及存储需求                        |
| ------------ | ---- | ------------------------------ |
| CHAR(M)      | M    | M为0~255之间的整数                   |
| VARCHAR(M)   |      | M为0~65535之间的整数 , 值的长度+1个字节     |
| TINYBLOB     |      | 允许长度0~255字节 , 值的长度+1个字节        |
| BLOB         |      | 允许长度0~65535字节 , 值的长度+2个字节      |
| MEDIUMBLOB   |      | 允许长度0~167772150字节 , 值的长度+3个字节  |
| LONGBLOB     |      | 允许长度0~4294967295字节 , 值的长度+4个字节 |
| TINYTEXT     |      | 允许长度0~255字节 , 值的长度+2个字节        |
| TEXT         |      | 允许长度0~65535字节 , 值的长度+2个字节      |
| MEDIUMTEXT   |      | 允许长度0~167772150字节 , 值的长度+3个字节  |
| LONGTEXT     |      | 允许长度0~4294967295字节 , 值的长度+4个字节 |
| VARBINARY(M) |      | 允许长度0~M个字节的变长字节字符串 , 值的长度+1个字节 |
| BINARY(M)    | M    | 允许长度0~M个字节的定长字节字符串             |

**CHAR 与 VARCHAR** 

两者类似 , 但保存和检索方式不同 

- CHAR长度固定 , VARCHAR长度可变
- 在检索时 , CHAR列删除了尾部的空格 , 而VARCHAR则保留这些空格 

BINARY 与 VARBINARY

BINARY 与 VARBINARY 类似于 CHAR 与 VARCHAR , 不同的是它们包含二进制字符串而不包含非二进制字符串 , 也就是说 , 它们包含字节字符串而不是字符字符串 , 它们没有字符集 , 并且排序和比较基于列值字节的数值值

**ENUM**

ENUM中文名称叫枚举类型 , 它的值范围需要在创建表时通过枚举方式显示指定 , 意思就是字段的值只能在给定范围中选择 , 对1~255个成员的枚举需要1个字节存储 ; 对于255~65535个成员 ,  需要2个字节存储 , 最多允许由65535个成员

使用ENUM时需注意 : 

- ENUM类型是忽略大小写的 , 在存储时会将小写都转成大写
- 对于插入不在ENUM指定范围内的值时 , 并不会返回警告 , 而是插入enum()中的第一个值
- ENUM类型只允许从值集合中选取单个值 , 而不能一次选取多个值

**SET**

SET 和 ENUM类型非常类似 , 也是一个字符串对象 , 里面可以包含0~64个成员 

- 1~8成员的集合 , 占1个字节
- 9~16成员的集合 , 占2个字节
- 17~24成员的集合 , 占3个字节
- 25~32成员的集合 , 占4个字节
- 33~64成员的集合 , 占8个字节

SET 和 ENUM除了存储之外 , 最主要的区别在于SET类型一次可以选取多个成员 , ENUM则只能选一个

```mysql
mysql> CREATE TABLE myset(col SET('a','b','c','d'));
Query OK, 0 rows affected (0.32 sec)

mysql> INSERT INTO myset VALUES('a,b'),('a,d,a'),('a,b'),('a,c'),('a');
Query OK, 5 rows affected (0.12 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> SELECT * FROM myset;
+------+
| col  |
+------+
| a,b  |
| a,d  |
| a,b  |
| a,c  |
| a    |
+------+
5 rows in set (0.00 sec)
```

对于超出允许值范围的值 , 将不允许注入到设置的SET类型中 , 而对于包含重复成员的集合将只取一次 , 集合去重

