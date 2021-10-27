# Redis - 数据库








<extoc></extoc>

## 介绍

Redis 服务器默认会创建 16 个数据库 , 该值由服务器配置的 `databases` 选项决定 , 默认为16 , 查看方式如下 : 

```shell
127.0.0.1:6379> config get databases
1) "databases"
2) "16"
```

切换数据库

```shell
127.0.0.1:6379> SELECT 1
OK
127.0.0.1:6379[1]> SELECT 0
OK
127.0.0.1:6379> 
```

## 生存时间

通过 `EXPIRE` 命令或者 `PEXPIRE` 命令 , 客户端可以以秒或者毫秒精度为数据库中的某个键设置生存时间 (Time To Live , TTL) , 在经过指定的秒数或者毫秒数之后 , 服务器就会自动删除生存时间为 0 的键

实例

```shell
127.0.0.1:6379> SET key value
OK
127.0.0.1:6379> EXPIRE key 5
(integer) 1
127.0.0.1:6379> GET key  # 5秒之内
"value"
127.0.0.1:6379> GET key  # 5秒之后
(nil)
```

## 过期时间

与 `EXPIRE` 命令和 `REXPIRE` 命令类似 , 客户端可以通过 `EXPIREAT` 命令或 `PEXPIREAT` 命令 , 以秒或者毫秒精度给数据库中的某个键设置过期时间 (Expire Time)

过期时间是 UNIX 时间戳 , 当键的过期时间来临时 , 服务器就会自动从数据库中删除这个键

实例

```shell
127.0.0.1:6379> SET key value
OK
127.0.0.1:6379> EXPIREAT key 1377257300
(integer) 1
127.0.0.1:6379> Time
1) "1377257296"
2) "296543"
127.0.0.1:6379> GET key  # 1377257300之前
"value"
127.0.0.1:6379> Time
1) "1529772303"
2) "230656"
127.0.0.1:6379> GET key  # 1377257300之后
(nil)
```

TTL 命令和 PTTL 命令接受一个带有生存时间或者过期时间的键 , 返回这个键的剩余生存时间 , 也就是 , 返回距离这个键被服务器自动删除还有多长时间

实例

```shell
127.0.0.1:6379> SET key value
OK
127.0.0.1:6379> EXPIRE key 1000
(integer) 1
127.0.0.1:6379> TTL key
(integer) 997
127.0.0.1:6379> PTTL key
(integer) 93633
```

我们可以发现 Redis 有四个不同的命令可以用于设置键的生存时间或过期时间 : 

```shell
EXPIRE <key> <ttl> # 命令用于将键key的生存时间设置为ttl秒
PEXPIRE <key> <ttl> # 命令用于将键key的生存时间设置为ttl毫秒
EXPIREAT <key> <timestamp> # 命令用于将键key的生存时间设置为timestamp毫秒
PEXPIREAT <key> <timestamp> # 命令用于将键key的过期时间设置为timestamp毫秒
```

虽然有多种不同单位和不同形式的设置命令 , 但是实际上 EXPIRE , PEXPIRE , EXPIREAT 三个命令都是使用 PEXPIREAT 命令来实现的 : 无论客户端执行的是以上四个命令中的哪一个 , 经过转换之后 , 最终执行的效果都和执行 PEXPIREAT 命令一样

**保存过期时间**

当客户端执行 PEXPIREAT 命令 (或者其他三个命令) 为一个数据库键设置过期时间时 , 服务器会在数据库的过期字典中关联给定的数据库键和过期时间

**移除过期时间**

`PERSIST` 命令是 `PEXPIREAT` 命令的反操作 : `PERSIST` 命令在过期字典中查找给定的键 , 并解除和值 (过期时间) 在过期字典中的关联

Redis 过期键删除策略 : 通过配合使用惰性删除和定期删除两种策略 , 服务器可以很好地在合理使用 CPU 时间和避免浪费内存空间之间取得平衡

## 持久化

Redis 是一个键值对数据库服务器 , 服务器中通常包含着任意个非空数据库 , 而每个非空数据库中又可以包含任意个键值对 , 为了方便起见 , 我们将服务器中的非空数据库以及他们的键值对统称为数据库状态

因为 Redis 是内存数据库 , 它将自己的数据库状态储存在内存里面 , 所以如果不想办法将储存在内存中的数据库状态保存到磁盘里面 , 那么一旦服务器进程退出 , 服务器中的数据库状态也会消失不见 , 因此为了解决这个问题 , Redis 提供了持久化功能

### RDB持久化

RDB 持久化功能可以将 Redis 在内存中的数据库状态保存到磁盘里面 , 避免数据意外丢失

RDB 持久化既可以手动执行 , 也可以根据服务器配置选项定期执行 , 该功能可以将某个时间点上的数据库状态保存到一个 RDB 文件中

RDB 持久化功能所生成的 RDB 文件是一个经过压缩的二进制文件 , 通过该文件可以还原生成 RDB 文件时的数据库状态

**RDB 文件的创建和载入**

有两个命令可以用于生成 RDB 文件 :

1. SAVE , 会阻塞 Redis 服务器进程 , 知道 RDB 文件创建完毕为止 , 在服务器进程阻塞期间 , 服务器不能处理任何请求

   ```shell
   redis> SAVE
   OK
   ```

2. BGSAVE , 会派生出一个子进程 , 然后由子进程负责创建 RDB 文件 , 服务器进程 (父进程) 继续处理命令请求

   ```shell
   redis> BGSAVE
   Background saving started
   ```

和使用 SAVE 命令或者 BGSAVE 命令创建 RDB 文件不同 , RDB 文件的载入工作是在服务器启动时自动执行的 , 所以 Redis 并没有专门用于载入 RDB 文件的命令 , 只要 Redis 服务器在启动时检测到 RDB 文件存在 , 就会自动载入 RDB 文件

并且服务器在载入 RDB 文件期间 , 会一直处于阻塞状态 , 直到载入工作完成为止

注意 : 在载入或生成 RDB 文件时 , 只会载入未过期的键 , 而过期的键会被直接忽略

### AOF持久化

除了 RDB 持久化功能之外 , Redis 还提供了 AOF (Append Only File) 持久化功能 , 与 RDB 持久化通过保存数据库中的键值对来记录数据库状态不同 , AOF 持久化是通过保存 Redis 服务器所执行的写命令来记录数据库状态的

AOF 持久化功能的实现可以分为命令追加 (Append) , 文件写入 , 文件同步 (Sync) 三个步骤

**AOF 文件载入与数据还原**

因为 AOF 文件里面包含了重建数据库状态所需的所有写命令 , 所以服务器只要读入并重新执行一遍 AOF 文件里面保存的写命令 , 就可以还原服务器关闭之前的数据库状态

Redis 读取 AOF 文件并还原数据库状态的详细步骤如下 : 

1. 创建一个不带网络连接的伪客户端 (fake client) : 因为 Redis 的命令只能在客户端上下文中执行 , 而载入 AOF 文件时所使用的命令直接来源于 AOF 文件而不是网络连接 , 所以服务器使用了一个没有网络连接的伪客户端来执行 AOF 文件保存的写命令 , 伪客户端执行命令的效果和带网络连接的客户端执行命令的效果完全一样
2. 从 AOF 文件中分析并读取出一条写命令
3. 使用伪客户端执行被读出的命令
4. 一直执行步骤 2 和步骤 3 , 知道 AOF 文件中的所有写命令都被处理完毕为止 

**AOF 重写**

由于随着服务器运行时间的流逝 , AOF 文件中的内容会越来越多 , 文件的体积也会越来越大 , 为了解决这 AOF 文件体积膨胀的问题 , Redis 提供了 AOF 文件重写 (rewrite) 功能 , 通过该功能 , Redis 服务器可以创建一个新的 AOF 文件来替代现有的 AOF 文件

和生成 RDB 文件时类似 , 在执行 AOF 重写的过程中 , 程序会对数据库中的键进行检查 , 已过期的键不会被保存到重写后的 AOF 文件中

由于 Redis 是单线程的 , 那么在重写 AOF 文件期间 , 服务器将无法处理客户端发来的命令请求 , 所以 Redis 决定将 AOF 重写程序放到子进程里执行 , 以达到如下目的 :

- 子进程进行 AOF 重写期间 , 服务器进程 (父进程) 可以继续处理命令请求
- 子进程带有服务器进程的数据副本 , 使用子进程而不是线程 , 可以在避免使用锁的情况下 , 保证数据的安全性

但是由于子进程进行 AOF 重写期间 , 服务器进程还需要继续处理命令请求 , 而新的命令可能会对现有的数据库状态进程修改 , 从而使得服务器当前的数据库状态和重写后的 AOF 文件所保存的数据库状态不一致 ; 为此 , Redis 服务器设置了一个 AOF 重写缓冲区 , 这个缓冲区在服务器创建子进程之后开始使用 , 当 Redis 服务器执行完一个写命令之后 , 它会同时将这个写命令发送给 AOF 缓冲区和 AOF 重写缓冲区

也就是说 AOF 重写期间 , 服务器进程需要执行以下三个工作 : 

1. 执行客户端发来的命令
2. 将执行后的写命令追加到 AOF 缓冲区
3. 将执行后的写命令追加到 AOF 重写缓冲区

当子进程完成 AOF 重写工作后 , 它会向父进程发送一个信号 , 会调用一个信号处理函数 , 并执行以下工作 : 

1. 将 AOF 重写缓冲区中的所有内容写入到新的 AOF 文件中 , 这时新 AOF 文件所保存的数据库状态将和服务器当前的数据库状态一致
2. 对新的 AOF 文件进行改名 , 原子地覆盖现有的 AOF 文件 , 完成新旧两个 AOF 文件的替换

注意 : 默认如果 AOF 持久化功能开启 , 那么将优先使用 AOF 

## 发布订阅 

Redis 发布订阅(pub/sub)是一种消息通信模式 : 发送者(pub)发送消息 , 订阅者(sub)接收消息

Redis 客户端可以订阅任意数量的频道

下图展示了频道 `channel1` ,  以及订阅这个频道的三个客户端 : `client2` , `client5` 和 `client1` 之间的关系 :  

![pubsub1](http://oux34p43l.bkt.clouddn.com/pubsub1.png)

当有新消息通过 `PUBLISH` 命令发送给频道 `channel1` 时 , 这个消息就会被发送给订阅它的三个客户端 :

![pubsub2](http://oux34p43l.bkt.clouddn.com/pubsub2.png)

**实例**

以下实例演示了发布订阅是如何工作的 , 在我们实例中我们创建了订阅频道名为 `redisChat` : 

```shell
redis 127.0.0.1:6379> SUBSCRIBE redisChat
 
Reading messages... (press Ctrl-C to quit)
1) "subscribe"
2) "redisChat"
3) (integer) 1
```

现在 , 我们先重新开启个 redis 客户端 , 然后在同一个频道 redisChat 发布两次消息 , 订阅者就能接收到消息

```shell
redis 127.0.0.1:6379> PUBLISH redisChat "Redis is a great caching technique"
 
(integer) 1
 
redis 127.0.0.1:6379> PUBLISH redisChat "Learn redis by w3cschool.cc"
 
(integer) 1
 
# 订阅者的客户端会显示如下消息
1) "message"
2) "redisChat"
3) "Redis is a great caching technique"
1) "message"
2) "redisChat"
3) "Learn redis by w3cschool.cc"
```

Redis 发布订阅常用命令 : 

| 序号 | 命令及描述                                                   |
| ---- | ------------------------------------------------------------ |
| 1    | `PSUBSCRIBE pattern [pattern ...]` , 订阅一个或多个符合给定模式的频道 |
| 2    | `PUBSUB subcommand [argument [argument ...]]` , 查看订阅与发布系统状态 |
| 3    | `PUBLISH channel message` , 将信息发送到指定的频道           |
| 4    | `PUNSUBSCRIBE [pattern [pattern ...]]` , 退订所有给定模式的频道 |
| 5    | `SUBSCRIBE channel [channel ...]` , 订阅给定的一个或多个频道的信息 |
| 6    | `UNSUBSCRIBE [channel [channel ...]]` , 指退订给定的频道     |
