# Python之路 - 第三方库之PyMySQL

## 介绍  🍀

pymysql是用于Python 3.x 链接MySQL数据库的一个第三方库 , 其使用方法和MySQLdb几乎相同 , pymysql的目的就是为了称为MySQLdb的替代品 , 因为MySQLdb不支持Python 3.x以后的版本

安装

```cmd
$ pip install PyMySQL
```

包内容

```python
PACKAGE CONTENTS
    _compat
    _socketio
    charset
    connections
    constants (package)
    converters
    cursors
    err
    optionfile
    tests (package)
    times
    util
```

## 使用  🍀

包中我们主要需要了解`connectinos.py` 中的内容

在pymysql包中我们只需要使用`Connect()` 来创建一个Connection对象

```python
def Connect(*args, **kwargs):
    """
    Connect to the database; see connections.Connection.__init__() for
    more information.
    """
    from .connections import Connection
    return Connection(*args, **kwargs)  # 返回一个Connection对象
```

Connection.\_\_init \_\_() 参数如下

```python
Connect(*args, **kwargs)
        Establish a connection to the MySQL database. Accepts several
        arguments:
        
        host: Host where the database server is located
        user: Username to log in as
        password: Password to use.
        database: Database to use, None to not use a particular one.
        port: MySQL port to use, default is usually OK. (default: 3306)
        bind_address: When the client has multiple network interfaces, specify
            the interface from which to connect to the host. Argument can be
            a hostname or an IP address.
        unix_socket: Optionally, you can use a unix socket rather than TCP/IP.
        charset: Charset you want to use.
        sql_mode: Default SQL_MODE to use.
        read_default_file:
            Specifies  my.cnf file to read these parameters from under the [client] section.
        conv:
            Conversion dictionary to use instead of the default one.
            This is used to provide custom marshalling and unmarshaling of types.
            See converters.
        use_unicode:
            Whether or not to default to unicode strings.
            This option defaults to true for Py3k.
        client_flag: Custom flags to send to MySQL. Find potential values in constants.CLIENT.
        cursorclass: Custom cursor class to use.
        init_command: Initial SQL statement to run when connection is established.
        connect_timeout: Timeout before throwing an exception when connecting.
            (default: 10, min: 1, max: 31536000)
        ssl:
            A dict of arguments similar to mysql_ssl_set()'s parameters.
            For now the capath and cipher arguments are not supported.
        read_default_group: Group to read from in the configuration file.
        compress; Not supported
        named_pipe: Not supported
        autocommit: Autocommit mode. None means use server default. (default: False)
        local_infile: Boolean to enable the use of LOAD DATA LOCAL command. (default: False)
        max_allowed_packet: Max size of packet sent to server in bytes. (default: 16MB)
            Only used to limit size of "LOAD LOCAL INFILE" data packet smaller than default (16KB).
        defer_connect: Don't explicitly connect on contruction - wait for connect call.
            (default: False)
        auth_plugin_map: A dict of plugin names to a class that processes that plugin.
            The class will take the Connection object as the argument to the constructor.
            The class needs an authenticate method taking an authentication packet as
            an argument.  For the dialog plugin, a prompt(echo, prompt) method can be used
            (if no authenticate method) for returning a string from the user. (experimental)
        db: Alias for database. (for compatibility to MySQLdb)
        passwd: Alias for password. (for compatibility to MySQLdb)
```

### 连接数据库  🍀

```python
import pymysql
# 连接MySQL数据库
connection = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='myroot',
                             db='mydatabase',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
```

pymysql包中的`cursors.py` 中的`class Cursor(object)` 可供我们建立与数据库进行交互的对象 , cursor(游标) , 下面就开始与数据库进行交互了

### 创建表  🍀

```mysql
import pymysql.cursors
# 连接MySQL数据库
connection = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='myroot',
                             db='mydatabase',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
try:
	# 创建游标实例
    with connection.cursor() as cursor:
        sql = """CREATE TABLE EMPLOYEE (
                 FIRST_NAME  CHAR(20) NOT NULL,
                 LAST_NAME  CHAR(20),
                 AGE INT,
                 SEX CHAR(1),
                 INCOME FLOAT );"""
        # 执行sql,并返回受影响行数
        cursor.execute(sql)
        # executemany()可一次性执行多个sql语句,提高了多行插入的性能
    # 提交,不然无法保存新建或者修改的数据
    connection.commit()
finally:
    connection.close()
```

**execute介绍**

```python
def execute(self, query, args=None):
    """Execute a query
    :param str query: Query to execute.
    :param args: parameters used with query. (optional)
    :type args: tuple, list or dict

    :return: Number of affected rows
    :rtype: int

     If args is a list or tuple, %s can be used as a placeholder in the query.
     If args is a dict, %(name)s can be used as a placeholder in the query.
     """
# list example
cursor.execute("update hosts set host = '1.1.1.2' where nid > %s", (1,))
# tuple example
cursor.execute("insert into hosts(host,color_id) values(%s,%s)", [("1.1.1.11",1),("1.1.1.11",2)])
```

### 查询表  🍀

Python查询MySQL获取数据使用方法如下 : 

- fetchone(self) : 获取下一行查询结果
- fetchmany(self, size=None) : 获取`size`行数的查询结果
- fetchall(self) : 获取全部的返回结果
- rowcount : 这是一个只读属性 , 并返回执行execute() 方法后影响的行数

在fetch数据时按照顺序进行 , 可以使用scroll(num, mode)来移动游标位置 , 如 : 

- cursor.scroll(1, mode='relative')  , 相对当前位置移动
- cursor.scroll(2, mode='absolute')  , 相对绝对位置移动

```python
import pymysql.cursors
# 连接MySQL数据库
connection = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='myroot',
                             db='mydatabase',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
try:
  	# 创建游标实例
    with connection.cursor() as cursor:
        sql = "SELECT * FROM user_info"
        # 执行sql,并返回受影响行数
        cursor.execute(sql)
        # 查询结果
        result = cursor.fetchall()
        print(result)
    # 提交
    connection.commit()
finally:
    connection.close()
'''
执行结果:
[{'username': 'Lyon', 'id': 1, 'password': '456'}]
'''
```

注意 : fetch默认获取的数据是元组类型 , 可以在建立cursor(游标)对象时 , 设置cursor属性进行修改 , 如设置为字典类型 : `cursor(cursor=pymysql.cursors.DictCursor)` 

获取最新自增ID : `cursor.lastrowid`

### 修改表  🍀

```python
import pymysql.cursors
# 连接MySQL数据库
connection = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='myroot',
                             db='mydatabase',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
try:
    # 创建游标实例
    with connection.cursor() as cursor:
        sql = "UPDATE user_info SET password = '456' WHERE username = 'Lyon'"
        # 执行sql,并返回受影响行数
        effect_row = cursor.execute(sql)
        print(effect_row)
    # 提交
    connection.commit()
except:
    # 发生错误时回滚
    connection.rollback()
# 关闭连接
connection.close()
```

### 删除表  🍀

```python
import pymysql.cursors
# 连接MySQL数据库
connection = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='myroot',
                             db='mydatabase',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
try:
    # 创建游标实例
    with connection.cursor() as cursor:
        sql = "DROP TABLE EMPLOYEE"
        # 执行sql,并返回影响行数
        cursor.execute(sql)
    # 提交
    connection.commit()
finally:
    # 关闭连接
    connection.close()
```