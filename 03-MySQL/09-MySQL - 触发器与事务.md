# Python之路 - MySQL触发器与事务

## 介绍  🍀

触发器是与表有关的数据库对象 , 在满足定义条件时触发 , 并执行触发器中定义的语句集合

### 创建触发器  🍀

语法 : 

```mysql
CREATE TRIGGER trigger_name trigger_time trigger_event
	ON tbl_name FOR EACH ROW TRIGGER_stmt
/* 触发器只能创建在永久性(Permanent Table)上,不能对临时表(Temporary Table)创建触发器 */
trigger_time:  -- 触发器的触发时间
BEFORE|AFTER
-- BEFORE:在检查约束前触发
-- AFTER:在检查约束后触发
trigger_event:  -- 触发器触发的事件
INSERT|UPDATE|DELETE
PS:对于同一个表相同触发时间的相同触发事件,只能定义一个触发器
```

详细如下

```mysql
-- 插入前
CREATE TRIGGER tri_before_insert_tb1 BEFORE INSERT ON tb1 FOR EACH ROW
BEGIN
    ...
END
-- 插入后
CREATE TRIGGER tri_after_insert_tb1 AFTER INSERT ON tb1 FOR EACH ROW
BEGIN
    ...
END
-- 删除前
CREATE TRIGGER tri_before_delete_tb1 BEFORE DELETE ON tb1 FOR EACH ROW
BEGIN
    ...
END
-- 删除后
CREATE TRIGGER tri_after_delete_tb1 AFTER DELETE ON tb1 FOR EACH ROW
BEGIN
    ...
END
-- 更新前
CREATE TRIGGER tri_before_update_tb1 BEFORE UPDATE ON tb1 FOR EACH ROW
BEGIN
    ...
END
-- 更新后
CREATE TRIGGER tri_after_update_tb1 AFTER UPDATE ON tb1 FOR EACH ROW
BEGIN
    ...
END
```

实例

```mysql
-- 插入前触发
DELIMITER $$
CREATE TRIGGER tri_before_insert_tb1 BEFORE INSERT ON tb1 FOR EACH ROW
BEGIN
IF NEW.NAME == 'LYON' THEN
	INSERT INTO tb2 (NAME)
VALUES ('aa')
END
END $$
```


### 删除触发器  🍀

语法 : 

```mysql
DROP TRIGGER [schema_name.]trigger_name
-- 如果没有指定schema_name,默认为当前数据库
```

实例

```mysql
mysql> DROP TRIGGER ins_film
Query OK, 0 rows affected (0.00 sec)
```


### 查看触发器  🍀

1. 可通过执行`SHOW TRIGGERS \G;`  命令查看触发器的状态 , 语法等信息 , 但是因为不能查询指定的触发器 , 所以每次都返回所有的触发器信息 , 使用不方便

2. 查询系统表information_schema.triggers表 , 该方式可以查询指定触发器的指定信息

   ```mysql
   DESC TRIGGERS;
   SELECT * FROM TRIGGERS WHERE trigger_name = '...' \G;
   ```


### 使用触发器  🍀

触发器的语句有以下两个限制

- 触发程序不能调用将数据返回客户端的存储程序 , 也不能采用CALL语句的动态SQL语句 , 但是允许存储程序通过参数将数据返回触发程序 , 也就是存储过程或者函数通过OUT或者INOUT类型的参数将数据返回触发器是可以的 , 但是不能调用直接返回数据的过程
- 不能在触发器中使用以显示或隐式方式开始或结束事务的语句 , 如START TRANSACTION , COMMIT或ROLLBACK

总之触发器无法由用户直接调用


## 事务  🍀

事务用于将某些操作的多个SQL作为原子性操作 , 一旦有某一个出现错误 , 即可回滚到原来的状态 , 从而保证数据库数据完整性

MySQL通过`SET AUTOCOMIT` , `START TRANSACTION` , `COMMIT` 和 `ROLLBACK` 等语句支持本地事务 

语法 : 

```mysql
START TRANSACTION|BEGIN[WORK]
COMMIT [WORK] [AND [NO] CHAIN] [[NO] RELEASE]
ROLLBACK [WORK] [AND [NO] CHAIN] [[NO] RELEASE]
SET AUTOCOMMIT = {0/1}
-- 特征值介绍:
START TRANSACTION 或 BEGIN 语句可以开始一项新的事务
COMMIT 和 ROLLBACK 用来提交或者回滚事务
CHAIN 和 RELEASE子句分别用来定义在事务提交或者回滚之后的操作,CHAIN会立即启动一个新事务,宾且和刚才的事务具有相同的隔离级别,RELEASE则会断开和客户端的连接
SET AUTOCOMMIT可以修改当前连接的提交方式,如果设置了 SET AUTOCOMMIT=0,则设置之后的所有事务都需要通过明确的命令进行提交或者回滚
```

默认情况下 , MySQL是自动提交(Autocommt)的 , 如果需要通过明确的Commit和Rollback来提交和回滚事务 , 那么就需要通过明确的事务控制命令来开始事务 , 这是和Oracle的事务管理明显不同的地方

实例

```mysql
mysql> DELIMITER $$
mysql> CREATE PROCEDURE p1(
    -> OUT p_return_code TINYINT
    -> )
    -> BEGIN
    -> 	 DECLARE EXIT HANDLER FOR SQLEXCEPTION
    -> 	 BEGIN  -- ERROR
    ->     SET p_return_code = 1;
    ->     ROLLBACK;  -- 回滚
    ->   END;
    ->   DECLARE EXIT HANDLER FOR SQLWARNING
    ->   BEGIN  -- WARNING
    ->     SET p_return_code = 2;
    ->     ROLLBACK;  
    ->   END;
    ->   START TRANSACTION;  -- 开始事务
    ->     DELETE FROM tb1;
    ->     INSERT INTO tb2(name) values('lyon');
    ->   COMMIT;
    ->   SET p_return_code = 0;  -- SUCCESS
    -> END $$
Query OK, 0 rows affected (0.10 sec)
-- 调用
SET @i = 0;
CALL p1(@i);
SELECT @i;
```

