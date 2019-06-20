# Python使用Redis流程

## 安装redis-py  🍀

```shell
$ pip install redis
```

## 创建Redis接口对象  🍀

创建 Redis 接口对象实例 , 将通过实例对 Redis 进行操作

有两种创建方式 :

- Redis : 继承 StrictRedis 类 , 用于向后兼容旧版本的 redis-py
- StrictRedis : 实现大部分官方的命令 , 并使用官方的语法和命令

```python
import redis
r = redis.Redis(host='127.0.0.1', port=6379)
r = redis.StrictRedis(host='127.0.0.1', port=6379)
```

## 使用连接池  🍀

通过连接池管理 Redis 对象

默认每个 Redis 实例都会维护一个自己的连接池 , 可以建立一个连接池 , 然后作为参数创建 Redis 实例 , 以此实现 Redis 实例共享连接池

```python
import redis
pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
r = redis.Redis(connection_pool=pool)
```

## String操作  🍀

```python
def set(name, value, ex=None, px=None, nx=False, xx=False):
    """
    设置值 , 默认不存在则创建 , 存在则修改
    ex , 过期时间 (秒)
    px , 过期时间 (毫秒)
    nx , 如果设置为True , 则只有name不存在时 , 当前set操作才执行
    xx , 如果设置为True , 则只有name存在时 , 岗前set操作才执行
    """
    
def setnx(name, value):
    """
    设置值 , 只有name不存在时 , 执行设置操作
    """

def setex(name, value, time):
	"""
	设置值
	time , 过期时间 (数字秒 或 timedelta对象)
	"""

def psetex(name, time_ms, value):
    """
	设置值
	time_ms , 过期时间 (数字毫秒 或 timedelta对象)
	"""
    
def mset(*args, **kwargs):
    """
	批量设置值,参数为关键字或字典
	"""
    
def get(name):
    """
	获取值
	"""
    
def mget(keys, *args):
    """
	批量获取,如:
	    mget('1', '2')
	    mget(['1', '2'])
	"""
    
def getset(name, value):
    """
	设置新值并获取原来的值
	"""
def getrange(key, start, end):
    """
	获取子序列 (根据字节获取 , 非字符)
    name , Redis 的 name
    start , 起始位置 (字节)
    end , 结束位置 (字节)
	"""
    
def setrange(name, offset, value):
    """
	修改字符串内容 , 从指定字符串索引开始向后替换 (新值太长时 , 则向后添加)
    offset , 字符串的索引 , 字节 (一个汉字三个字节)
    value , 要设置的值
	"""
    
def setbit(name, offset, value):
    """
	对name对应值的二进制表示的位进行操作
	"""
    
def getbit(name, offset):
    """
	获取name对应的值的二进制表示中的某位的值  (0或1)
	"""
    
def bitcount(key, start=None, end=None):
    """
	获取name对应的值的二进制表示中 1 的个数
    key , Redis的name
    start , 位起始位置
    end , 位结束位置
	"""
    
def bitop(operation, dest, *keys):
    """
	获取多个值 , 并将值做位运算 , 将最后的结果保存至新的name对应的值
	operation,AND (并) 、 OR (或) 、 NOT (非) 、 XOR (异或)
    dest, 新的Redis的name
    *keys,要查找的Redis的name
	"""
    
def strlen(name):
    """
	返回name对应值的字节长度 (一个汉字3个字节)
	"""
    
def incr(self, name, amount=1):
    """
	自增 name对应的值 , 当name不存在时 , 则创建name＝amount , 否则 , 则自增。
	amount,自增数 (必须是整数)
	"""
    
def incrbyfloat(self, name, amount=1.0):
    """
	自增 name对应的值 , 当name不存在时 , 则创建name＝amount , 否则 , 则自增。
	amount,自增数 (浮点型)
	"""
    
def decr(self, name, amount=1):
    """
	自减 name对应的值 , 当name不存在时 , 则创建name＝amount , 否则 , 则自减
	amount,自减数 (整数)
	"""
    
def append(key, value):
    """
	在redis name对应的值后面追加内容
	"""
```

## Hash操作  🍀

```python
def hset(name, key, value):
    """
    name对应的hash中设置一个键值对 (不存在 , 则创建；否则 , 修改)
    """

def hsetnx(name, key, value):
    """
    当name对应的hash中不存在当前key时则创建 (相当于添加)
    """
    
def hmset(name, mapping):
    """
    在name对应的hash中批量设置键值对
    name , redis的name
    mapping , 字典 , 如 : hmset('xx', {'k1':'v1', 'k2': 'v2'})
    """

def hget(name,key):
    """
    在name对应的hash中获取根据key获取value
    """

def hmget(name, keys, *args):
    """
    在name对应的hash中获取多个key的值
    name , reids对应的name
    keys , 要获取key集合 , 如 : ['k1', 'k2', 'k3']
    *args , 要获取的key , 如 : k1,k2,k3
    r.mget('xx', ['k1', 'k2'])
    或
    r.hmget('xx', 'k1', 'k2')
    """

def hgetall(name):
    """
    获取name对应hash的所有键值
    """

def hlen(name):
    """
    获取name对应的hash中键值对的个数
    """

def hkeys(name):
    """
    获取name对应的hash中所有的key的值
    """

def hvals(name):
    """
    获取name对应的hash中所有的key的值
    """

def hexists(name, key):
    """
    检查name对应的hash是否存在当前传入的key
    """

def hdel(name,*keys):
    """
    将name对应的hash中指定key的键值对删除
    """

def hincrby(name, key, amount=1):
    """
    自增name对应的hash中的指定key的值 , 不存在则创建key=amount
    name , redis中的name
    key , hash对应的key
    amount , 自增数 (整数)
    """

def hincrbyfloat(name, key, amount=1.0):
    """
    自增name对应的hash中的指定key的值 , 不存在则创建key=amount
    name , redis中的name
    key , hash对应的key
    amount , 自增数 (浮点数)
    """
 
def hscan(name, cursor=0, match=None, count=None):
    """
    增量式迭代获取 , 对于数据大的数据非常有用 , hscan可以实现分片的获取数据 , 
    并非一次性将数据全部获取完 , 从而放置内存被撑爆
    name , redis的name
    cursor , 游标 (基于游标分批取获取数据)
    match , 匹配指定key , 默认None 表示所有的key
    count , 每次分片最少获取个数 , 默认None表示采用Redis的默认分片个数
 
    如 : 
        第一次 : cursor1, data1 = r.hscan('xx', cursor=0, match=None, count=None)
        第二次 : cursor2, data1 = r.hscan('xx', cursor=cursor1, match=None, count=None)
        ...
        直到返回值cursor的值为0时 , 表示数据已经通过分片获取完毕
    """

def hscan_iter(name, match=None, count=None):
    """
    利用yield封装hscan创建生成器 , 实现分批去redis中获取数据
    match , 匹配指定key , 默认None 表示所有的key
    count , 每次分片最少获取个数 , 默认None表示采用Redis的默认分片个数
    """　
```

## List操作  🍀

```python
def lpush(name,values):
    """
    在name对应的list中添加元素 , 每个新的元素都添加到列表的最左边
    """
 
def rpush(name, values):
    """
    表示从右向左操作
    """
    
def lpushx(name,value):
    """
    在name对应的list中添加元素 , 只有name已经存在时 , 值添加到列表的最左边
    """

def rpushx(name, value):
    """
    表示从右向左操作
    """
    
def llen(name):
    """
    返回list的长度
    """

def linsert(name, where, refvalue, value):
    """
    在name对应的列表的某一个值前或后插入一个新值
    name , redis的name
    where , BEFORE或AFTER
    refvalue , 标杆值 , 即 : 在它前后插入数据
    value , 要插入的数据
    """

def lset(name, index, value):
    """
    对name对应的list中的某一个索引位置重新赋值
    name , redis的name
    index , list的索引位置
    value , 要设置的值
    """

def lrem(name, value, num):
    """
    在name对应的list中删除指定的值
    name , redis的name
    value , 要删除的值
    num , num=0删除列表中所有的指定值
         num=2,从前到后 , 删除2个
         num=-2,从后向前 , 删除2个
    """

def lpop(name):
    """
    在name对应的列表的左侧获取第一个元素并在列表中移除 , 返回值则是第一个元素
    """
    
def rpop(name):
    """
    表示从右向左操作
    """
    
def lindex(name, index):
    """
    在name对应的列表中根据索引获取列表元素
    """

def lrange(name, start, end):
    """
    在name对应的列表分片获取数据
    name , redis的name
    start , 索引的起始位置
    end , 索引结束位置
    """

def ltrim(name, start, end):
    """
    在name对应的列表中移除没有在start-end索引之间的值
    name , redis的name
    start , 索引的起始位置
    end , 索引结束位置
    """

def rpoplpush(src, dst):
    """
    从一个列表取出最右边的元素 , 同时将其添加至另一个列表的最左边
    src , 要取数据的列表的name
    dst , 要添加数据的列表的name
    """

def blpop(keys, timeout):
    """
    将多个列表排列 , 按照从左到右去pop对应列表的元素
    keys , redis的name的集合
    timeout , 超时时间 , 当元素所有列表的元素获取完之后 , 阻塞等待列表内有数据的时间 (秒), 0 表示永远阻塞
    """

def brpop(keys, timeout):
    """
    从右向左获取数据
    """
    
def brpoplpush(src, dst, timeout=0):
    """
    从一个列表的右侧移除一个元素并将其添加到另一个列表的左侧
    src , 取出并要移除元素的列表对应的name
    dst , 要插入元素的列表对应的name
    timeout , 当src对应的列表中没有数据时 , 阻塞等待其有数据的超时时间 (秒) , 0 表示永远阻塞
    """
```

自定义增量迭代

```python
# 由于redis类库中没有提供对列表元素的增量迭代 , 如果想要循环name对应的列表的所有元素 , 那么就需要 : 
    # 1、获取name对应的所有列表
    # 2、循环列表
# 但是 , 如果列表非常大 , 那么就有可能在第一步时就将程序的内容撑爆 , 所有有必要自定义一个增量迭代的功能 : 
 
def list_iter(name):
    """
    自定义redis列表增量迭代
    :param name: redis中的name , 即 : 迭代name对应的列表
    :return: yield 返回列表元素
    """
    list_count = r.llen(name)
    for index in xrange(list_count):
        yield r.lindex(name, index)
 
# 使用
for item in list_iter('pp'):
    print(item)
```

## Set操作  🍀

```python
def sadd(name,values):
    """
    name对应的集合中添加元素
    """

def scard(name):
    """
    获取name对应的集合中元素个数
    """

def sdiff(keys, *args):
    """
    在第一个name对应的集合中且不在其他name对应的集合的元素集合
    """

def sdiffstore(dest, keys, *args):
    """
    获取第一个name对应的集合中且不在其他name对应的集合 , 再将其新加入到dest对应的集合中
    """

def sinter(keys, *args):
    """
    获取多一个name对应集合的并集
    """

def sinterstore(dest, keys, *args):
    """
    获取多一个name对应集合的并集 , 再讲其加入到dest对应的集合中
    """

def sismember(name, value):
    """
    检查value是否是name对应的集合的成员
    """

def smembers(name):
    """
    获取name对应的集合的所有成员
    """

def smove(src, dst, value):
    """
    将某个成员从一个集合中移动到另外一个集合
    """

def spop(name):
    """
    从集合的右侧 (尾部)移除一个成员 , 并将其返回
    """

def srandmember(name, numbers):
    """
    从name对应的集合中随机获取 numbers 个元素
    """

def srem(name, values):
    """
    在name对应的集合中删除某些值
    """

def sunion(keys, *args):
    """
    获取多一个name对应的集合的并集
    """

def sunionstore(dest,keys, *args):
    """
    获取多一个name对应的集合的并集 , 并将结果保存到dest对应的集合中
    """

def sscan(name, cursor=0, match=None, count=None):
    sscan_iter(name, match=None, count=None):
    """
    同字符串的操作 , 用于增量迭代分批获取元素 , 避免内存消耗太大
    """
```

## Zset操作  🍀

```python
def zadd(name, *args, **kwargs):
    """
    在name对应的有序集合中添加元素
    zadd('zz', 'n1', 1, 'n2', 2)
    或
    zadd('zz', n1=11, n2=22)
    """

def zcard(name):
    """
    获取name对应的有序集合元素的数量
    """

def zcount(name, min, max):
    """
    获取name对应的有序集合中分数 在 [min,max] 之间的个数
    """

def zincrby(name, value, amount):
    """
    自增name对应的有序集合的 name 对应的分数
    """

def zrange( name, start, end, desc=False, withscores=False, score_cast_func=float):
    """
    按照索引范围获取name对应的有序集合的元素
    name , redis的name
    start , 有序集合索引起始位置 (非分数)
    end , 有序集合索引结束位置 (非分数)
    desc , 排序规则 , 默认按照分数从小到大排序
    withscores , 是否获取元素的分数 , 默认只获取元素的值
    score_cast_func , 对分数进行数据转换的函数
    """
 
def zrevrange(name, start, end, withscores=False, score_cast_func=float):
    """
    按照索引范围从大到小排序
    """

def zrangebyscore(name, min, max, start=None, num=None, withscores=False, score_cast_func=float):
    """
    按照分数范围获取name对应的有序集合的元素
    """

zrevrangebyscore(name, max, min, start=None, num=None, withscores=False, score_cast_func=float)
    """
    按照分数范围从大到小排列
    """
def zrank(name, value):
    """
    获取某个值在 name对应的有序集合中的排行 (从 0 开始)
    """

def zrevrank(name, value):
    """
    zrank从大到小排序
    """
    
def zrangebylex(name, min, max, start=None, num=None):
    """
    当有序集合的所有成员都具有相同的分值时 , 
    有序集合的元素会根据成员的值 (lexicographical ordering)来进行排序 , 
    而这个命令则可以返回给定的有序集合键 key 中 , 元素的值介于 min 和 max 之间的成员,
    对集合中的每个成员进行逐个字节的对比 (byte-by-byte compare) , 并按照从低到高的顺序 , 
    返回排序后的集合成员,
    如果两个字符串有一部分内容是相同的话 , 那么命令会认为较长的字符串比较短的字符串要大
    name , redis的name
    min , 左区间 (值)。 + 表示正无限； - 表示负无限； ( 表示开区间； [ 则表示闭区间
    min , 右区间 (值)
    start , 对结果进行分片处理 , 索引位置
    num , 对结果进行分片处理 , 索引后面的num个元素
    如 : 
        ZADD myzset 0 aa 0 ba 0 ca 0 da 0 ea 0 fa 0 ga
        zrangebylex('myzset', "-", "[ca") 结果为 : ['aa', 'ba', 'ca']
    """

def zrevrangebylex(name, max, min, start=None, num=None):
    """
    zrangebylex从大到小排序
    """
    
def zrem(name, values):
    """
    删除name对应的有序集合中值是values的成员
    如 : 
    	zrem('zz', ['s1', 's2'])
    """

def zremrangebyrank(name, min, max):
    """
    根据排行范围删除
    """

def zremrangebyscore(name, min, max):
    """
    根据排行范围删除
    """

def zremrangebylex(name, min, max):
    """
    根据值返回删除
    """

def zscore(name, value):
    """
    获取name对应有序集合中 value 对应的分数
    """

def zinterstore(dest, keys, aggregate=None):
    """
    获取两个有序集合的交集 , 如果遇到相同值不同分数 , 则按照aggregate进行操作
    aggregate的值为:  SUM  MIN  MAX
    """

def zunionstore(dest, keys, aggregate=None):
    """
    获取两个有序集合的并集 , 如果遇到相同值不同分数 , 则按照aggregate进行操作
    aggregate的值为:  SUM  MIN  MAX
    """

def zscan(name, cursor=0, match=None, count=None, score_cast_func=float):
    zscan_iter(name, match=None, count=None,score_cast_func=float):
    """
    同字符串相似 , 相较于字符串新增score_cast_func , 用来对分数进行操作
    """
```

## 其他操作  🍀

```python
def delete(*names):
    """
    根据删除redis中的任意数据类型
    """

def exists(name):
    """
    检测redis的name是否存在
    """

def keys(pattern='*'):
    """
    根据模型获取redis的name
    KEYS * 匹配数据库中所有 key 。
    KEYS h?llo 匹配 hello  , hallo 和 hxllo 等。
    KEYS h*llo 匹配 hllo 和 heeeeello 等。
    KEYS h[ae]llo 匹配 hello 和 hallo  , 但不匹配 hillo
    """

def expire(name ,time):
    """
    为某个redis的某个name设置超时时间
    """

def rename(src, dst):
    """
    对redis的name重命名为
    """

def move(name, db):
    """
    将redis的某个值移动到指定的db下
    """

def randomkey():
    """
    随机获取一个redis的name (不删除)
    """

def type(name):
    """
    获取name对应值的类型
    """

def scan(cursor=0, match=None, count=None):
    scan_iter(match=None, count=None):
    """
    同字符串操作 , 用于增量迭代获取key
    """
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

## 利用管道实现计数器  🍀

```python
import redis

conn = redis.Redis(host='192.168.1.41',port=6379)

conn.set('count',1000)

with conn.pipeline() as pipe:

    # 先监视 , 自己的值没有被修改过
    conn.watch('count')

    # 事务开始
    pipe.multi()
    old_count = conn.get('count')
    count = int(old_count)
    if count > 0:  # 有库存
        pipe.set('count', count - 1)

    # 执行 , 把所有命令一次性推送过去
    pipe.execute()
```

## 发布订阅  🍀

发布者 : 服务器

订阅者 : Dashboard和数据处理

示例如下 :

helprs.py

```python
import redis

class RedisHelper:

    def __init__(self):
        self.__conn = redis.Redis(host='10.211.55.4')
        self.chan_sub = 'fm104.5'
        self.chan_pub = 'fm104.5'

    def public(self, msg):
        self.__conn.publish(self.chan_pub, msg)
        return True

    def subscribe(self):
        pub = self.__conn.pubsub()
        pub.subscribe(self.chan_sub)
        pub.parse_response()
        return pub
```

订阅者

```python
from helpers import RedisHelper
 
obj = RedisHelper()
redis_sub = obj.subscribe()
 
while True:
    msg= redis_sub.parse_response()
    print(msg)
```

发布者

```python
from helpers import RedisHelper
 
obj = RedisHelper()
obj.public('hello')
```

## Sentinel  🍀

redis重的sentinel主要用于在redis主从复制中 , 如果master顾上 , 则自动将slave替换成master 

```python
from redis.sentinel import Sentinel
 
# 连接哨兵服务器(主机名也可以用域名)
sentinel = Sentinel([('10.211.55.20', 26379),
                     ('10.211.55.20', 26380),
                     ],
                    socket_timeout=0.5)
 
# 获取主服务器地址
# master = sentinel.discover_master('mymaster')
# print(master)

# 获取从服务器地址
# slave = sentinel.discover_slaves('mymaster')
# print(slave)

# 获取主服务器进行写入
# master = sentinel.master_for('mymaster')
# master.set('foo', 'bar')
 
# 获取从服务器进行读取 (默认是round-roubin)
# slave = sentinel.slave_for('mymaster', password='redis_auth_pass')
# r_ret = slave.get('foo')
# print(r_ret)
```

更多参见 : [Redis for GitHub](https://github.com/andymccurdy/redis-py/) , [Doc](http://doc.redisfans.com/)

