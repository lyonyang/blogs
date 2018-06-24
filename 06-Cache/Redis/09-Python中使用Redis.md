# Python中使用Redis

## 介绍  🍀

安装支持库

```shell
$ pip install redis
```

redis 包内容条目如下 : 

```
redis
├── __init__.py        
├── _compat.py        
├── client.py  
├── connection.py
├── exceptions.py
├── lock.py 
├── sentinel.py
└── utils.py
```

## 开始  🍀

```python
>>> import redis
>>> r = redis.StrictRedis(host='localhost', port=6379, db=0)
>>> r.set('foo', 'bar')
True
>>> r.get('foo')
'bar'
```

## API参考  🍀

[官方 Redis 命令文档](http://redis.io/commands) 中对每个命令都有详细的解释 , `redis-py` 公开了两个实现这些命令的客户端类 , `StrictRedis` 类视图坚持官方命令语法 , 但是有几个例外 , 如下 : 

- SELECT : 未实现 , 
- DEL : 由于 `del` 是 Python 语法中保留的关键字 , 所以 `redis-py` 使用 `delete` 代替
- CONFIG GET|SET : 它们分别以 `config_get` 或 `config_set` 实现
- MULTI/EXEC : 这些是作为管道类的一部分实现的
- SUBSCRIBE/LISTEN :  PubSub是作为一个单独的类实现的 , 因为它将底层连接置于无法执行非pubsub命令的状态中 , 从Redis客户端调用pubsub方法将返回一个PubSub实例 , 你可以在其中订阅通道并侦听消息
- SCAN/SSCAN/HSCAN/ZSCAN : 扫描命令是在 Redis 文档中存在的情况下实现的 , 此外 , 每个命令都有一个等量迭代器方法 ; 这些纯粹是为了方便 , 所以用户不必在迭代时跟踪游标 ; 对于此行为 , 请使用`scan_iter/sscan_iter/hscan_iter/zscan_iter` 方法 

除了上面的更改之外 , Redis 类是 StrictRedis 的子类 , 它重写了其他几个命令 , 以提供与较早版本的 `redis-py` 的向后兼容性 : 

- LREM : `"num"` 和 `"value"` 参数的顺序颠倒 , 这样 `"num"` 可以提供默认值为零 
- ZADD : Redis 在 `value` 之前指定 `score` 参数 , 这些在实现时被意外地交换了 , 直到人们已经在使用它之后才被发现 , Redis 类接受 *args 的形式为 : name1, score1, name2, score2, … 
- SETEX : `time` 和 `value` 参数顺序颠倒

## 连接池  🍀

在后台 , redis-py 使用连接池来管理到 Redis 服务器的连接 , 默认情况下 , 你创建的每个 Redis 实例将依次创建自己的连接池 , 你可以通过将已经创建的连接池实例传递给 Redis 类的 `connection_pool` 参数来覆盖此行为并使用现有的连接池 , 你可以选择这样做 , 以便实现客户端分片 , 或者对如何管理连接进行更精细的粒度控制

```python
>>> pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
>>> r = redis.Redis(connection_pool=pool)
```

## 连接  🍀

ConnectionPools 管理一组连接实例 , 默认的连接是一个正常的基于TCP套接字的连接 UnixDomainSocketConnection 允许运行在与服务器相同设备上的客户端通过 Unix 域套接字进行连接 , 要使用 UnixDomainSocketConnection 连接 , 只需将 `unix_socket_path ` 参数传递给 Unix域 套接字文件 , 它是一个字符串 ; 此外 , 确保在 `redis.conf` 文件中定义了 `unixsocket` 参数 , 默认情况下它被注释掉了

```
>>> r = redis.Redis(unix_socket_path='/tmp/redis.sock')
```

你也可以创建自己的连接子类 , 如果您想要控制异步框架内的套接字行为 , 这可能很有用 ; 要使用自己的连接实例化客户机类 , 需要创建一个连接池 , 将类传递给 `connection_class` 参数 , 传递给池的其他关键字参数将传递给初始化期间指定的类

```python
>>> pool = redis.ConnectionPool(connection_class=YourConnectionClass,
                                your_arg='...', ...)
```

## 解析器  🍀

解析器类提供了一种方法来控制来自Redis 服务器的响应是如何被解析的 , `redis-py` 工具有两个解析器类 , `PythonParser` 和 `HiredisParser` , 默认情况下 , 如果安装了 `hiredis` 模块 , `redis-py` 将尝试使用 `HiredisParser` , 否则将返回 `PythonParser`

Hiredis 是一个由核心Redis团队维护的C库 , PieterNoordhuis 很好地创建了 Python 绑定 , 使用Hiredis 可以使来自 Redis 服务器的解析响应速度提高10倍 , 在检索许多数据 (例如从LRANGE或SMEMBERS操作) 时 , 性能的提高最为明显

Hiredis 在PyPI上是可用的 , 可以通过 `pip` 或 `easeinstall` 安装 , 就像 `redis-py` 一样

```shell
$ pip install hiredis
```

或

```shell
$ easy_install hiredis
```

## 管道  🍀

Pipelines 是基 Redis 类的子类 , 它支持在单个请求中缓冲多个命令到服务器 , 它们可以通过减少客户端和服务器之间来回 TCP 数据包的数量来显着地提高命令组的性能

管道的使用非常简单 : 

```python
>>> r = redis.Redis(...)
>>> r.set('bing', 'baz')
>>> # Use the pipeline() method to create a pipeline instance
>>> pipe = r.pipeline()
>>> # The following SET commands are buffered
>>> pipe.set('foo', 'bar')
>>> pipe.get('bing')
>>> # the EXECUTE call sends all buffered commands to the server, returning
>>> # a list of responses, one for each command.
>>> pipe.execute()
[True, 'baz']
```

为了便于使用 , 所有被缓冲到管道中的命令都返回管道对象本身 , 因此 , 调用可以如下 : 

```python
>>> pipe.set('foo', 'bar').sadd('faz', 'baz').incr('auto_number').execute()
[True, True, 6]
```

此外 , 管道还可以确保缓冲命令作为一个组以原子形式执行 , 默认情况下会发生这种情况 , 如果希望禁用管道的原子性质 , 但仍然希望缓冲命令 , 则可以关闭事务

```python
>>> pipe = r.pipeline(transaction=False)
```

当需要原子事务时 , 需要在 Redis 中检索值以便在事务中使用时 , 就会出现一个常见的问题 , 例如 , 让我们假设 `incr` 命令不存在 , 我们需要在 Python 中构建 `incr` 的原子版本

完全天真的实现可以获得值 , 在 Python 中增加值 , 并将新值设置回原来的值 . 但是 , 这不是原子性的 , 因为多个客户端可以同时执行此操作 , 每个客户端从 `get` 获得相同的值

输入监视命令 , WATCH 命令提供了在启动事务之前监视一个或多个键的能力 , 如果这些键中的任何一个在该事务执行之前发生更改 , 则整个事务将被取消并引发 WatchError , 为了实现我们自己的客户端 incr 命令 , 我们可以这样做 : 

```python
>>> with r.pipeline() as pipe:
...     while 1:
...         try:
...             # put a WATCH on the key that holds our sequence value
...             pipe.watch('OUR-SEQUENCE-KEY')
...             # after WATCHing, the pipeline is put into immediate execution
...             # mode until we tell it to start buffering commands again.
...             # this allows us to get the current value of our sequence
...             current_value = pipe.get('OUR-SEQUENCE-KEY')
...             next_value = int(current_value) + 1
...             # now we can put the pipeline back into buffered mode with MULTI
...             pipe.multi()
...             pipe.set('OUR-SEQUENCE-KEY', next_value)
...             # and finally, execute the pipeline (the set command)
...             pipe.execute()
...             # if a WatchError wasn't raised during execution, everything
...             # we just did happened atomically.
...             break
...        except WatchError:
...             # another client must have changed 'OUR-SEQUENCE-KEY' between
...             # the time we started WATCHing it and the pipeline's execution.
...             # our best bet is to just retry.
...             continue
```

注意 , 由于管道必须在监视期间绑定到单个连接 , 因此必须注意通过调用 Reset() 方法确保连接返回到连接池 . 如果管道被用作上下文管理器(如上面的示例所示) , 则将自动调用 Reset() , 当然 , 您可以通过显式调用 Reset() 来手动完成此操作 : 

```python
>>> pipe = r.pipeline()
>>> while 1:
...     try:
...         pipe.watch('OUR-SEQUENCE-KEY')
...         ...
...         pipe.execute()
...         break
...     except WatchError:
...         continue
...     finally:
...         pipe.reset()
```

存在一个名为`transaction` 的方便方法 , 用于处理所有处理和重试手表错误的样板 , 它需要一个可调用的 , 应该期望有一个参数 , 一个管道对象和任何数量的键来监视 , 上面的客户端 incr 命令可以这样编写 , 这更容易阅读 : 

```python
>>> def client_side_incr(pipe):
...     current_value = pipe.get('OUR-SEQUENCE-KEY')
...     next_value = int(current_value) + 1
...     pipe.multi()
...     pipe.set('OUR-SEQUENCE-KEY', next_value)
>>>
>>> r.transaction(client_side_incr, 'OUR-SEQUENCE-KEY')
[True]
```

## 发布/订阅  🍀

redis-py 包括 PubSub 对象 , 该对象订阅通道并侦听新消息 , 创建一个 PubSub 对象如下 : 

```python
>>> r = redis.StrictRedis(...)
>>> p = r.pubsub()
```

一旦 PubSub 实例被创建 , 就可以订阅通道和模式

```python
>>> p.subscribe('my-first-channel', 'my-second-channel', ...)
>>> p.psubscribe('my-*', ...)
```

读取信息

```python
>>> p.get_message()
{'pattern': None, 'type': 'subscribe', 'channel': 'my-second-channel', 'data': 1L}
>>> p.get_message()
{'pattern': None, 'type': 'subscribe', 'channel': 'my-first-channel', 'data': 2L}
>>> p.get_message()
{'pattern': None, 'type': 'psubscribe', 'channel': 'my-*', 'data': 3L}
```

取消订阅 , 不传参数所有的通道或模式都将被取消订阅

```python
>>> p.unsubscribe()
>>> p.punsubscribe('my-*')
>>> p.get_message()
{'channel': 'my-second-channel', 'data': 2L, 'pattern': None, 'type': 'unsubscribe'}
>>> p.get_message()
{'channel': 'my-first-channel', 'data': 1L, 'pattern': None, 'type': 'unsubscribe'}
>>> p.get_message()
{'channel': 'my-*', 'data': 0L, 'pattern': None, 'type': 'punsubscribe'}
```

redis-py 还允许您注册回调函数来处理已发布的消息

```python
>>> def my_handler(message):
...     print 'MY HANDLER: ', message['data']
>>> p.subscribe(**{'my-channel': my_handler})
# read the subscribe confirmation message
>>> p.get_message()
{'pattern': None, 'type': 'subscribe', 'channel': 'my-channel', 'data': 1L}
>>> r.publish('my-channel', 'awesome data')
1
# for the message handler to work, we need tell the instance to read data.
# this can be done in several ways (read more below). we'll just use
# the familiar get_message() function for now
>>> message = p.get_message()
MY HANDLER:  awesome data
# note here that the my_handler callback printed the string above.
# `message` is None because the message was handled by our handler.
>>> print message
None
```

如果您的应用程序对订阅/取消订阅确认消息不感兴趣 , 你可以通过传设置 `ignore_subscribe_message=True` 忽略订阅消息

```python
>>> p = r.pubsub(ignore_subscribe_messages=True)
>>> p.subscribe('my-channel')
>>> p.get_message()  # hides the subscribe message and returns None
>>> r.publish('my-channel')
1
>>> p.get_message()
{'channel': 'my-channel', 'data': 'my data', 'pattern': None, 'type': 'message'}
```

更多资料 : [redis-py](https://pypi.org/project/redis/)







