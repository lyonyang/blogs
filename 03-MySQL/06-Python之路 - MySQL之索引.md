# Python之路 - MySQL之索引

## 介绍  🍀

索引是数据库中最常用也是最重要的手段之一 , 是数据库中专门用于帮助用户快速查询数据的一种数据结构 , 类似于字典中的目录 , 查找字典内容时可以根据目录查找到数据的存放位置 , 然后直接获取值即可

索引是在MySQL的存储引擎层中实现的  而不是在服务器层实现的 , 所以每种存储引擎的索引都不一定完全相同 , 也不是所有的存储引擎都支持所有的索引类型

三个常用引擎支持的索引类型比较

| 索引          | MyISAM引擎 | InnoDB引擎 | Memory引擎 |
| ----------- | -------- | -------- | -------- |
| B-Tree索引    | 支持       | 支持       | 支持       |
| HASH索引      | 不支持      | 不支持      | 支持       |
| R-Tree索引    | 支持       | 不支持      | 不支持      |
| Full-text索引 | 支持       | 5.6版本后支持 | 不支持      |

下面对比较常用的两个索引类型进行说明

## B-Tree索引与HASH索引  🍀

**B-Tree索引**

B-Tree索引是最常见的索引 , 构造**类似二叉树** , 所以可以根据键值进行快速的访问 , 通常只需要很少的读操作就可以找到正确的行 , 不过B-Tree中的B不代表二叉树 , 而是代表**平衡树** , **B-Tree并不是一棵二叉树**

B-Tree索引适用于全关键字 , 关键字范围和关键字前缀查询

**HASH索引**

HASH索引相对简单 , 只有Memory/Heap引擎支持 

HASH索引适用于 **Key - Value**查询 , 通过HASH索引要比通过B-Tree索引查询更迅速 , 但是HASH**不适用范围查询** , 例如 : < , > , <= , >=这类操作 ; 如果使用Memory/Heap引擎并且where条件中不使用 "=" 今夕in个索引列 , 那么不会用到索引 , Memory/Heap引擎只有在 "=" 的条件下才会使用索引


## MySQL索引管理  🍀

索引的功能就是为了加速查找和约束 , 下面对常用索引进行介绍

查看索引 : `SHOW INDEX FROM tablename \G;` 

### 普通索引  🍀

普通索引仅有一个功能 , 就是加速查找

**创建方式**

方式一  : 

```mysql
/* 创建索引 */
CREATE INDEX indexname ON tablename(column_name(length));
-- 注意如过是CHAR,VARCHAR类型,length可以小于字段长度
-- 如果是BLOB和TEXT类型,必须指定length
```

方式二 : 

```mysql
/* 修改表结构 */
ALTER TABLE tablename ADD INDEX indexname (column_name);
```

方式三 : 

```mysql
/* 创建表时直接指定 */
CREATE TABLE mytable(  
ID INT NOT NULL,   
name VARCHAR(16) NOT NULL,  
INDEX [indexname] (name(length))  -- indexname可不写
);  
```

**删除索引**

```mysql
DROP INDEX indexname ON tablename; 
ALTER TABLE tablename DROP INDEX column_name;
```


### 唯一索引  🍀

唯一索引有两个功能 : 加速查找和唯一约束(可含NULL)

与普通索引类似 , 不同的就是 : 索引列的值必须唯一 , 但允许有空值 , 如果是组合索引 , 则列值的组合必须唯一

**创建方式**

方式一 : 

```mysql
/* 创建索引 */
CREATE UNIQUE INDEX indexname ON tablename(column_name(length));
```

方式二 : 

```mysql
/* 修改表结构 */
ALTER TABLE tablename ADD UNIQUE [indexname] (column_name(length));
```

方式三 : 

```mysql
/* 创建表时指定 */
CREATE TABLE mytable(  
ID INT NOT NULL,   
username VARCHAR(16) NOT NULL,  
UNIQUE [indexname] (username(length))  
);  
```

**删除索引**

```mysql
DROP INDEX indexname ON tablename; 
ALTER TABLE tablename DROP INDEX column_name;
```


### 主键索引  🍀

主键有两个功能 : 加速查找和唯一约束(不可NULL)

**创建方式**

方式一 : 

```mysql
/* 修改表结构 */
ALTER TABLE tablename ADD PRIMARY KEY column_name;
```

方式二 : 

```mysql
/* 创建表时指定 */
CREATE TABLE mytable(  
id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(32) NOT NULL
);
-- or
CREATE TABLE mytable(  
id INT NOT NULL AUTO_INCREMENT,
name VARCHAR(32) NOT NULL
PRIMARY KEY(id)
);
```

**删除主键**

```mysql
ALTER TABLE tablename DROP PRIMARY KEY;
ALTER TABLE tablename MODIFY column_name column_type, drop primary key;
```


###　组合索引  🍀

组合索引是将n个列组合成一个索引 , 专门用于组合搜索 , 其效率大于索引合并

应用场景 : 频繁的同时使用n列来进行查询 , 如 : where n1 = 'alex' and n2 = 666

**创建索引**

```mysql
/* 创建表 */
CREATE TABLE mytable(
nid INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(32) NOT NULL,
email VARCHAR(64) NOT NULL,
extra TEXT
);
/* 创建组合索引 */
CREATE INDEX ix_name_email ON mytable(name,email);
```

如上创建索引后 , 查询 : 

- name and email  -- 使用索引
- name  -- 使用索引
- email  -- 不使用索引

PS : 对于同时搜索n个条件时 , 组合索引的性能好于多个单一索引合并

全文索引 : 对文本的内容进行分词 , 进行搜索

索引合并 : 使用多个单列索引组合搜索

覆盖索引 : 

MySQL只需要通过索引就可以返回查询所需要的数据 , 而不必在查到索引之后进行回表操作 , 减少IO , 提供效率

当你对一个sql 使用explain statement 查看一个sql的执行计划时 , 在EXPLAIN的Extra列出现Using Index提示时 , 就说明该select查询使用了覆盖索引


## 使用索引  🍀

使用索引可以加速查找 , 但是如果以错误的方式使用 , 即使建立索引也不会生效

1. 以"%"开头的LIKE查询不走索引

   ```mysql
   mysql> EXPLAIN SELECT * FROM actor WHERE last_name LIKE '%NI' \G;  -- 不走索引
   mysql> EXPLAIN SELECT * FROM actor WHERE last_name LIKE 'NI%' \G;  -- 走索引
   ```

2. 数据类型出现隐式转换不走索引 , MySQL默认把输入的常量值进行转换后才进行检索 , 如下last_name列为字符串类型

   ```mysql
   mysql> EXPLAIN SELECT * FROM actor WHERE last_name = 1 \G;  -- 不走索引,全表扫描
   mysql> EXPLAIN SELECT * FROM actor WHERE last_name = '1' \G;  -- 走索引
   -- 一定记得在where条件中把字符常量值用引号引起来
   ```

3. 组合索引情况下 , 查询条件不包含索引列最左边部分 , 不走索引

   ```mysql
   mysql> EXPLAIN SELECT * FROM mytable WHERE name='lyon' AND email='myemail' \G; -- 使用索引
   mysql> EXPLAIN SELECT * FROM mytable WHERE email='myemail' AND name='lyon' \G; -- 不使用索引
   -- 最左原则
   ```

4. 如果MySQL估计使用索引比全表扫描更慢 , 不走索引 , MySQL 5.6版本中 , 能够通过Trace清晰地看到优化器选择的过程

5. 用or分割开的条件中有未建立索引的列 , 不走索引

   ```mysql
   mysql> SELECT * FROM tb1 WHERE nid = 1 OR email = 'myemail';  -- 不使用索引,email列未建立
   mysql> SELECT * FROM tb1 WHERE nid = 1 OR name = 'myemail';  -- 使用索引,两者都建立
   ```

6. 普通索引的"!="和">"不走索引 , 特别的走

   ```mysql
   -- !=
   mysql> SELECT * FORM tb1 WHERE name != 'lyon'; -- 不走索引
   mysql> SELECT * FORM tb1 WHERE nid != 123; -- 走索引,nid为主键
   -- >
   mysql> SELECT * FORM tb1 WHERE name > 'lyon'; -- 不走索引
   mysql> SELECT * FORM tb1 WHERE nid > 123;  -- 走索引,nid为主键或索引是整数类型
   ```

7. 排序条件为索引 , 选择的映射如果不是索引 , 则不走索引

   ```mysql
   mysql> SELECT email FROM tb1 ORDER BY name desc; -- 不走索引
   mysql> SELECT * FROM tb1 ORDER BY nid desc;  -- 走索引,如果对主键排序,则还是走
   ```

**注意 :** 

```mysql
-- 避免使用select *

-- count(1)或count(列) 代替 count(*)

-- 创建表时尽量时 char 代替 varchar

-- 表的字段顺序固定长度的字段优先

-- 组合索引代替多个单列索引（经常使用多个条件查询时）

-- 尽量使用短索引

-- 使用连接（JOIN）来代替子查询(Sub-Queries)

-- 连表时注意条件类型需一致

-- 索引散列值（重复少）不适合建索引，例：性别不适合
```


