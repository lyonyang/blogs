# Redis - 简介

## 介绍  🍀

REmote DIctionary Server(Redis) 是一个由 Salvatore Sanfilippo 写的 `key-value` 存储系统

Redis是一个开源的使用 `ANSI C` 语言编写 , 遵守BSD协议 , 支持网络 , 可基于内存亦可持久化的日志型 , `Key-Value` 数据库 , 并提供多种语言的API

**特点**

Redis 与其他 key - value 缓存产品有以下三个特点 : 

- Redis支持数据的持久化 , 可以将内存中的数据保持在磁盘中 , 重启的时候可以再次加载进行使用
- Redis不仅仅支持简单的 `key-value` 类型的数据 , 同时还提供 list , set , zset , hash等数据结构的存储
- Redis支持数据的备份 , 即 `master-slave` 模式的数据备份

**优势**

- 性能极高 – Redis能读的速度是 `110000次/s` , 写的速度是 `81000次/s `
- 丰富的数据类型 – Redis支持二进制案例的 Strings , Lists , Hashes , Sets 及 Ordered Sets 数据类型操作
- 原子 – Redis的所有操作都是原子性的 , 同时Redis还支持对几个操作全并后的原子性执行
- 丰富的特性 – Redis还支持 `publish/subscribe` , 通知 key 过期等等特性

## 安装  🍀

方式一

```shell
$ yum isntall redis
```

运行

```shell
$ redis-server /etc/redis.conf
```

方式二 : 

```shell
$ wget http://download.redis.io/releases/redis-4.0.10.tar.gz
$ tar xzf redis-4.0.10.tar.gz
$ cd redis-4.0.10
$ make
```

运行

```shell
$ src/redis-server
```

与内置客户端进行交互 : 

```shell
$ src/redis-cli
redis> set foo bar
OK
redis> get foo
"bar"
```

## 配置  🍀

Redis 的配置文件位于 Redis 安装目录下 , 文件名为 `redis.conf` 

我们可以通过 `CONFIG` 命令查看或者设置配置项 

### 查看配置  🍀

语法

```shell
redis 127.0.0.1:6379> CONFIG GET CONFIG_SETTING_NAME
```

实例

```shell
redis 127.0.0.1:6379> CONFIG GET loglevel
 
1) "loglevel"
2) "notice"
```

使用 * 号获取所有配置项 : 

```shell
redis 127.0.0.1:6379> CONFIG GET *
```

### 修改配置  🍀

你可以通过修改 `redis.conf` 文件或使用 `CONFIG SET` 命令来修改配置

语法

```shell
redis 127.0.0.1:6379> CONFIG SET CONFIG_SETTING_NAME NEW_CONFIG_VALUE
```

实例

```shell
redis 127.0.0.1:6379> CONFIG SET loglevel "notice"
OK
redis 127.0.0.1:6379> CONFIG GET loglevel
 
1) "loglevel"
2) "notice"
```

## 数据类型  🍀

Redis支持五种数据类型 : `string (字符串)`  , `hash (哈希)`  , `list (列表)`  , `set (集合)` 及 `zset(sorted set : 有序集合)`

### String  🍀

string 是 Redis 最基本的类型 , 你可以理解成与 Memcached 一模一样的类型 , 一个 key 对应一个 value

string 类型是二进制安全的 , 意思是 Redis 的 string 可以包含任何数据 , 比如 jpg 图片或者序列化的对象

string 类型是 Redis 最基本的数据类型 , 一个键最大能存储 512 MB

实例

```shell
redis 127.0.0.1:6379> SET name "redis.net.cn"
OK
redis 127.0.0.1:6379> GET name
"redis.net.cn"
```

在以上实例中我们使用了 Redis 的 `SET` 和 `GET` 命令 , 键为 name , 对应的值为`redis.net.cn` 

**注意 : **一个键最大能存储 512 MB

### Hash  🍀

Redis hash 是一个键值对集合

Redis hash 是一个 string 类型的 `field` 和 `value` 的映射表 , hash 特别适合用于存储对象

实例

```shell
redis 127.0.0.1:6379> HMSET user:1 username redis.net.cn password redis.net.cn points 200
OK
redis 127.0.0.1:6379> HGETALL user:1
1) "username"
2) "redis.net.cn"
3) "password"
4) "redis.net.cn"
5) "points"
6) "200"
redis 127.0.0.1:6379>
```

以上实例中 hash 数据类型存储了包含用户脚本信息的用户对象 ,  实例中我们使用了 Redis `HMSET` , `HEGTALL` 命令 , `user:1` 为键值

每个 hash 可以存储 `2^(32-1)` 键值对 , 相当于 40 多亿 

### List  🍀

Redis 列表是简单的字符串列表 , 按照插入顺序排序 , 你可以添加一个元素导列表的头部 (左边) 或者尾部 (右边) 

实例

```shell
redis 127.0.0.1:6379> lpush redis.net.cn redis
(integer) 1
redis 127.0.0.1:6379> lpush redis.net.cn mongodb
(integer) 2
redis 127.0.0.1:6379> lpush redis.net.cn rabitmq
(integer) 3
redis 127.0.0.1:6379> lrange redis.net.cn 0 10
1) "rabitmq"
2) "mongodb"
3) "redis"
redis 127.0.0.1:6379>
```

列表最多可存储 `2^(32-1)` 元素 (4294967295 , 每个列表可存储40多亿)

### Set  🍀

Redis 的 Set 是 string 类型的无序集合

集合是通过哈希表实现的 , 所以添加 , 删除 , 查找的复杂度都是 O(1)

**sadd 命令**

添加一个 string 元素到 , key 对应的 set 集合中 , 成功返回 1 ,如果元素以及在集合中返回 0 , key 对应的 set 不存在返回错误

```
sadd key member
```

实例

```shell
redis 127.0.0.1:6379> sadd redis.net.cn redis
(integer) 1
redis 127.0.0.1:6379> sadd redis.net.cn mongodb
(integer) 1
redis 127.0.0.1:6379> sadd redis.net.cn rabitmq
(integer) 1
redis 127.0.0.1:6379> sadd redis.net.cn rabitmq
(integer) 0
redis 127.0.0.1:6379> smembers redis.net.cn
 
1) "rabitmq"
2) "mongodb"
3) "redis"
```

**注意 : **以上实例中 `rabitmq` 添加了两次 , 但根据集合内元素的唯一性 , 第二次插入的元素将被忽略

集合中最大的成员数为 `2^(32-1)` (4294967295, 每个集合可存储40多亿个成员)

### zset  🍀

Redis zset 和 Set 一样也是string类型元素的集合 , 且不允许重复的成员

不同的是每个元素都会关联一个 double 类型的分数 , redis 正是通过分数来为集合中的成员进行从小到大的排序。

zset 的成员是唯一的 , 但分数 (score) 却可以重复

**zadd 命令**

添加元素到集合 , 元素在集合中存在则更新对应 score

```
zadd key score member 
```

实例

```shell
redis 127.0.0.1:6379> zadd redis.net.cn 0 redis
(integer) 1
redis 127.0.0.1:6379> zadd redis.net.cn 0 mongodb
(integer) 1
redis 127.0.0.1:6379> zadd redis.net.cn 0 rabitmq
(integer) 1
redis 127.0.0.1:6379> zadd redis.net.cn 0 rabitmq
(integer) 0
redis 127.0.0.1:6379> ZRANGEBYSCORE redis.net.cn 0 1000
 
1) "redis"
2) "mongodb"
3) "rabitmq"
```