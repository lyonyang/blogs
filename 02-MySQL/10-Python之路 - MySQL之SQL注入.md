# Python之路 - MySQL之SQL注入

## 介绍  🍀

`SQL注入`(SQL Injection)就是利用某些数据的外部接口将用户数据插入到实际的数据库操作语言(SQL)当中 , 从而达到入侵数据库乃至操作系统的目的 , 它的产生主要是由于程序对用户输入的数据没有进行严格的过滤 , 导致非法数据库查询语句的执行 

`SQL注入`攻击具有很大的危害 , 攻击者可以利用它读取 , 修改或者删除数据库内的数据 , 获取数据库中的用户名和密码等敏感信息 , 甚至可以获得数据库管理原的权限 , 而且 , `SQL注入`也很难防范 , 网站管理员无法通过安装系统补丁或者进行简单的安全配置进行自我保护 , 一般的防火墙也无法拦截`SQl注入`攻击  

SQL注入实例(PHP程序实例)

创建用户表user

```mysql
CREATE TABLE user(
userid INT(11) NOT NULL AUTO_INCREMENT,
username VARCHAR(20) NOT NULL DEFAULT '',
password VARCHAR(20) NOT NULL DEFAULT '',
PRIMARY KEY(userid)
)TYPE=MyISAM AUTO_INCREMENT=3;
```

添加一条用户记录

```mysql
INSERT INTO 'user' VALUES(1,'angel','mypass');
```

验证用户root登录localhost服务器

```php
<?php
    $servername = "localhost";
	$dbusername = "root";
	$dbpassword = "";
	$dbname = "injection";
	mysql_connect($servername,$dbusername,$dbpassword) or die ("数据库连接失败!");
	$sql = "SELECT * FROM user WHERE username='$username' AND password='$password'";
	$result = mysql_db_query($dbname,$sql);
	$userinfo = mysql_fetch_array($result);
	if (empty($userinfo))
    {
    echo "登录失败" 
    } else {
    echo "登录成功"
    }
	echo "<p>SQL Query:$sql<p>";
	?>
```

提交URL

```php
http://127.0.0.1/injection/user.php?username=angel' or '1=1
```

结果发现 , 这个URL可以成功登录系统 , 显然这并不是我们预期的结果 ; 溶氧也可以利用SQL的注释语句实现SQL注入 , 如下 :

```php
http://127.0.0.1/injection/user.php?username=angel'/*
http://127.0.0.1/injection/user.php?username=angel'#
```

因为在SQL语句中 , "/*" 或者 "#" 都可以将后面的语句注释掉  这样上述语句就可以通过这两个注释符中的任意一个将后面的语句给注释掉  结果导致只根据用户名而没有密码的URL都成功进行了登录

"or" 是利用逻辑运算 , 注释符是根据MySQL的特性 , 这个比逻辑运算简单多了 , 两者都实现了SQL注入效果


## 应对措施  🍀

对于SQL注入隐患 , 后果可想而知 , 轻则获得数据信息 , 重则可以将数据进行非法更改 , 一下则是常用的防范方法

### PrepareStatemen + Bind - Variable  🍀

MySQL服务器端并不存在共享池的概念 , 所以在MySQL上使用绑定变量(Bind Variable) , 最大的好处主要是为了避免SQL注入 , 增加安全性

即使用PrepareStatement语句(如Java)来实现 , 输入的参数中的单引号会被正常转义 , 导致后续的` "or 1=1"` 作为username条件内容出现 , 而不会作为SQL的一个单独条件被解析 , 避免了SQL注入的风险 ; 同样的 , 在使用绑定变量的情况下 , 企图通过注释 `"/*" 或 "#" ` 让后续条件失效也是会失败的

需要注意 , PrepareStatement语句是由JDBC驱动来支持的 , 他仅仅做了简单的替换和转义 , 斌不是MySQL提供了PreparedStatement的特性


### 使用应用程序提供的转换函数  🍀

很多应用程序接口都提供了对特殊字符进行转换的函数 , 恰当地使用这些函数 , 可以防止应用程序用户输入使应用程序生成不期望的语句

- MySQL C API : 使用mysql_real_escape_string() API调用
- MySQL++ : 使用escape 和quote修饰符
- PHP : 使用mysql_real_escape_string()函数
- Perl DBI : 使用placeholders 或者quote()方法
- Ruby DBI : 使用paceholders 或者quote()方法


### 自己定义函数进行检验  🍀

如果现有的转换函数任然不能满足要求 , 则需要自己编写函数进行输入校验

目前最好的解决方法就是 , 对用用户提交或者可能改变的数据进行简单分类 , 分别应用正则表达式来对用户提供的输入数据进行严格的检测和验证

### Python中的pymysql模块  🍀

通过Python的pymysql模块来进行SQL的执行 , 在pymysql模块内部会自动把 " ' "(单引号做一个特殊的处理 , 来预防上述的错误)

```mysql
......
effect_row = cursor.execute("select username from user_info where username='%s' and password = '%s'", (username, pwd))
......
```










