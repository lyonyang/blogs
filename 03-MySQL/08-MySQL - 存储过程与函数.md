# MySQL - 存储过程和函数


<extoc></extoc>

## 介绍  🍀

存储过程和函数是实现经过编译并存储在数据库中的一段SQL语句的集合 , 调用存储过程和函数可以简化应用开发人员的很多工作 , 减少数据在数据库和应用服务器之间的传输 , 对于提高数据处理的效率是有好处的

存储过程和函数的区别在于函数必须有返回值 , 而存储过程没有 , 存储过程的参数可以使用IN , OUT , INOUT类型 , 而函数的参数只能是IN类型的 , 如果有函数从其他类型的数据库迁移到MySQL , 那么就可能因此需要将函数改成成存储过程

参数介绍 : 

- IN 仅用于传入参数用
- OUT 仅用于返回值用
- INOUT 既可以传入又可以当做返回值

在对存储过程或函数进行操作时 , 需要首先确认用户是否具有相应的权限 ' 例如 : 创建存储过程或者函数需要CREATE ROUTINE权限 , 修改或者删除存储过程或者函数需要ALTER ROUTINE权限 , 执行存储过程或者函数需要EXECUTE权限

## 创建存储过程或函数  🍀

语法 : 

```mysql
/* 创建存储过程 */
CREATE PROCEDURE sp_name([proc_parameter[,...]])
	[characteristic ...] routine_body
/* 创建函数 */	
CREATE FUNCTION sp_name([func_parameter[,...]])
	RETURNS type
	[characteristic ...] routine_body
-- 参数介绍
proc_parameter:[IN\ OUT\ INOUT] param_name type
func_parameter:param_name type
characteristic:
LANGUAGE SQL
|[NOT] DETERMINISTIC  -- 修改SQL语句的结束符
|{CONTAINS SQL|NO SQL|READS SQL DATA|MODIFIES SQL DATA}
|SQL SECURITY{DEFINER|INVOKER}  -- SQL语句块
|COMMENT 'string' -- END 结束
```

实例

```mysql
-- 修改SQL语句的结束符为$$
mysql> DELIMITER $$
-- 创建存储过程
mysql> CREATE PROCEDURE film_in_stock(IN p_film_id INT,IN p_store_id INT,OUT p_film_count INT)
    -> READS SQL DATA
    -> BEGIN  -- 开始
    -> SELECT inventory_id  -- SQL语句块
    -> FROM inventory
    -> WHERE film_id = p_film_id
    -> AND store_id = p_store_id
    -> AND inventory_in_stock(inventory_id);
    -> SELECT FOUND_ROWS() INTO p_film_count;
    -> END $$  -- 结束
Query OK, 0 rows affected (0.11 sec)
-- 把SQL语句的结束符改为 ;
mysql> DELIMITER ;
```

**characteristic特征值部分说明**

| 特征值                                      | 说明                                       |
| ---------------------------------------- | ---------------------------------------- |
| LANGUAGE SQL                             | 说明下面过程的body是使用SQL语言编写 , 系统默认的 , 为今后MySQL会支持的除SQL外的其他语言做准备 |
| [NOT] DETERMINISTIC                      | DETERMINISTIC确定的 , 即每次输入一样输出也一样的程序 , NOT DETERMINISTIC非确定的 , 这个值当前还没有被优化程序使用 |
| {CONTAINS SQL<br>丨NO SQL<br>丨READS SQL DATA<br>丨MODIFIES SQL DATA} | CONTAINS SQL表示子程序不包含读或写数据的语句<br>NO SQL 表示子程序不包含SQL语句<br>READS SQL DATA表示子程序包含读数据的语句 , 但不包含写数据的语句<br>MODIFIES SQL DATA表示子程序包含写数据的语句<br>默认值为CONTAINS SQL |
| SQL SECURITY {DEFINER丨INVOKER}          | 可以用来指定子程序该用创建子程序者的许可来执行 , 还是使用调用者的许可来执行 , 默认为DEFINER(定义者) |
| COMMENT 'string'                         | 存储过程或者函数的注释信息                            |

通过`call`调用存储过程 

```mysql
CALL sp_name([parameter[,...]])
```

事务


## 修改存储过程或函数  🍀

语法 : 

```mysql
ALTER {PRCEDURE|FUNCTION} sp_name [characteristic...]
-- characteristic
{CONTAINS SQL|NO SQL|READS SQL DATA|MODIFIES SQL DATA}
|SQL SECURITY {DEFINER|INVOKER}
|COMMENT 'string'
```



## 删除存储过程或函数  🍀

一次只能删除一个存储过程或者函数 , 删除过程或者函数需要有该过程或者函数的ALTER ROUTINE权限

语法 : 

```mysql
DROP {PROCEDURE|FUNCTION} [IF EXISTS] sp_name
```

实例

```mysql
mysql> DROP PROCEDURE film_in_stock;
Query OK, 0 rows affected (0.00 sec)
```


## 查看存储过程或函数  🍀

1. 查看状态

   ```mysql
   SHOW PROCEDURE STATUS LIKE 'film_in_stock' \G;
   ```

2. 查看定义

   ```mysql
   SHOW CREATE {PROCEDURE|FUNCTION} sp_name;
   ```

3. 通过查看information_schema.Routines查看

   ```mysql
   SELECT * FROM ROUTINES WHERE ROUTINE_NAME = 'film_in_stock' \G;
   ```


## 变量的使用  🍀

存储过程和和函数可以使用变量 , 而且在MySQL 5.1版本中 , 变量不区分大小写

**变量的定义**

通过DECLARE定义一个局部变量 , 该变量的作用域只能在BEGIN...END块中 , 可以用在嵌套的块中 ; 变量的定义必须卸载复合语句的开头 , 并且在任何其他语句的前面 , 可以一次声明多个相同类型的变量 , DEFAULT可以设置默认值

语法 : 

```mysql
DECLARE var_name[,...] type [DEFAULT value];
```

实例

```mysql
DECLARE last_month_start DATE;
```

**变量的赋值**

变量可以直接赋值 , 或者通过查询赋值 ; 直接赋值使用SET , 可以赋厂里爱那个或者赋表达式

语法 : 

```mysql
SET var_name = expr [,var_name = expr]...
```

给刚才定义的last_month_start复制

```mysql
SET last_month_start = DATE_SUB(CURRENT_DATE(),INTERVAL 1 MONTH);
```

可以通过查询将结果赋给变量 , 但是结果必须只有一行

```mysql
SELECT col_name [,...] INTO var_name [,...] table_expr;
```

实例如下

```mysql
DECLARE v_payments DECIMAL(5,2); -- SUM OF PAYMENTS MADE PREVIOUSLY
```


## 条件处理  🍀

用于定义在处理过程中遇到问题时相应的处理步骤

定义条件

```mysql
DECLARE condition_name CONDITION FOR condition_value
condition_value:
	SQLSTATE [VALUE] sqlstate_value
|mysql_error_code
```

处理条件

```mysql
DECLARE handler_type HANDLER FOR condition_value [,...] sp_statement
handler_type:
	CONTINUE
|EXIT  -- 执行终止
|UNDO  -- 现在还不支持
condition_value:
	SQLSTATE [VALUE] sqlstate_value
|condition_name
|SQLWARNING
|NOT FOUND
|SQLEXCEPTION
|mysql_error_code
```

实例

```mysql
/* 事务 */
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
```


## 光标  🍀

在存储过程或函数中 , 可以使用光标对结果集进行循环处理

声明光标

```mysql
DECLARE curor_name CURSOR FOR select_statement
```

OPEN光标

```mysql
OPEN cursor_name
```

FETCH光标

```mysql
FETCH cursor_name INTO var_name [,var_name]...
```

CLOSE光标

```mysql
CLOSE cursor_name
```

实例

```mysql
mysql> DELIMITER $$
mysql> CREATE PROCEDURE p3()
    -> BEGIN
    ->   DECLARE ssid INT;   -- 定义变量
    ->   DECLARE ssname VARCHAR(50);
    ->   DECLARE done INT DEFAULT FALSE;
    ->   DECLARE my_cursor CURSOR FOR SELECT sid,sname FROM student;
    ->   DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    ->   OPEN my_cursor;
    -> 		ins:LOOP
    -> 			FETCH my_cursor INTO ssid,ssname;
    ->          IF done THEN
    ->          	LEAVE ins;
    ->          END IF;
    ->          INSERT INTO teacher(tname) values(ssname);
    ->      END LOOP ins;
    ->   CLOSE my_cursor;
    -> END $$
Query OK, 0 rows affected (0.02 sec)
```


## 流程控制  🍀

1. IF语句

   ```mysql
   IF search_condition THEN statement_list
   	[ELSEIF search_condition THEN statement_list]...
   	[ELSE statement_list]
   END IF
   ```

2. CASE语句

   ```mysql
   CASE case_value
   	WHEN when_value THEN statement_list
   	[WHEN when_value THEN statement_list]...
   	[ELSE statement_list]
   END CASE
   -- or
   CASE
   	WHEN search_condition THEN statement_list
   	[WHEN search_codition THEN statement_list]...
   	[ELSE statement_list]
   END CASE
   ```

3. LOOP语句

   ```mysql
   [begin_label:] LOOP
   	statement_list
   END LOOP [end_label]
   ```

4. LEAVE语句

   ```mysql
   /* 用来从标注流程构造中退出,通常和BEGIN...END或者循环一起使用 */
   BEGIN
   	...
   	ins:LOOP
   		...
   		LEAVE ins;
   		...
   	...
   	END LOOP ins;
   END;
   ```

5. ITERATE语句

   ```mysql
   /* 相当于continue */
   BEGIN
   	...
   	ins:LOOP
   		IF ... THEN
   		ITERATE ins;
   	END LOOP ins;
   	...
   END;
   ```

6. REPEAT语句

   ```mysql
   /* 满足条件退出循环 */
   [begin_lable:] REPEAT
   	statement_list
   UNTIL search_condition
   END REPEAT [end_late]
   ```

7. WHILE语句

   ```mysql
   /* 满足条件才执行 */
   [begin_lable:] WHILE search_condition DO
   	statement_list
   END WHILE [end_label]
   ```



## 内置函数  🍀

对于一些内置函数 , 就直接看官方的吧 https://dev.mysql.com/doc/refman/5.7/en/functions.html

需要注意的是 , 上述为自定义函数的操作 , 而对于自定义函数 , 在功能块中不要写SQL语句 , 否则会报错 , 函数仅仅只是一个功能 , 一个在SQL中被应用的功能 , 如果要写SQL则应该使用存储过程

