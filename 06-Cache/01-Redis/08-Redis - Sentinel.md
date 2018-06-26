# Redis - Sentinel

## 介绍  🍀

Sentinel (哨岗 , 哨兵) 是 Redis 的高可用性 (high availability) 解决方案 : 由一个或多个 Sentinel 实例组成的 Sentinel 系统可以监视任意多个主服务器 , 并在被监视的主服务器进入下线状态时 , 自动将下线主服务器属下的某个从服务器升级为新的主服务器 , 然后由新的主服务器代替已下线的主服务器继续处理命令请求

## 启动并初始化Sentinel  🍀

启动一个 Sentinel 可以使用命令 : 

```shell
$ redis-sentinel /path/to/your/sentinel.conf
```

或者命令 : 

```shell
$ redis-sentinel /path/to/your/sentinel.conf --sentinel
```

当一个 Sentinel 启动时 , 它需要执行以下步骤 : 

1. 初始化服务器
2. 将普通 Redis 服务器使用的代码替换成 Sentinel 专用代码
3. 初始化 Sentinel 状态
4. 根据给定的配置文件 , 初始化 Sentinel 的监视主服务器列表
5. 创建连向主服务器的网络连接

## 初始化服务器  🍀

因为 Sentinel 本质上只是一个运行在特殊模式下的 Redis 服务器 , 所以启动 Sentinel 的第一步 , 就是初始化一个普通的 Redis 服务器 ; 不过 , 因为 Sentinel 执行的工作和普通 Redis 服务器执行的工作不同 , 所以 Sentinel 的初始化过程和普通 Redis 服务器的初始化过程并不完全相同

例如 , 普通服务器在初始化时会通过载入 RDB 文件或者 AOF 文件来还原数据库状态 , 但是因为 Sentinel 并不适用数据库 , 所以初始化 Sentinel 时就不会载入 RDB 文件或者 AOF 文件

Sentinel 模式下 Redis 服务器主要功能的使用情况如下 : 

| 功能                                                | 使用情况                                                     |
| --------------------------------------------------- | ------------------------------------------------------------ |
| 数据库和键值对方面的命令 , 不如 SET , DEL , FLUSHDB | 不使用                                                       |
| 事务命令 , 比如 MULTI 和 WATCH                      | 不使用                                                       |
| 脚本命令 , 比如 EVAL                                | 不使用                                                       |
| RDB 持久化命令 , 比如 SAVE 和BGSAVE                 | 不使用                                                       |
| AOF 持久化命令 , 比如 BGREWRITEAOF                  | 不使用                                                       |
| 复制命令 , 比如 SLAVEOF                             | Sentinel 内部可以使用 , 但客户端不可以使用                   |
| 发布与订阅命令 , 比如 PUBLISH 和 SUBSCRIBE          | SUBSCRIBE , PSUBSCRIBE , UNSUBSCRIBE , PUNSUBSCRIBE 四个命令在 Sentinel 内部和客户端都可以使用 , 但 PUBLISH 命令只能在 Sentinel内部使用 |
| 文件事件处理器 (负责发送命令请求 , 处理命令回复)    | Sentinel 内部使用 , 但关联的文件事件处理器和普通 Redis 服务器不同 |
| 时间事件处理器 (负责执行 serverCron函数)            | Sentinel 内部使用 , 时间事件的处理器仍然是 serverCron 函数 , serverCron 函数会调用 sentinel.c/sentinelTimer 函数 , 后者包含了 Sentinel 要执行的所有操作 |

初始化 Sentinel 的最后一步是创建连向被监视主服务器的网络连接 , Sentinel 将成为主服务器的客户端 , 它可以向主服务器发送命令 , 并从命令回复中获取相关的信息

对于每个被 Sentinel 监视的主服务器来说 , Sentinel 会创建两个连向主服务器的异步网络连接 : 

- 一个是命令连接 , 这个连接专门用于主服务器发送命令 , 并接收命令回复
- 另一个是订阅连接 , 这个连接专门用于订阅主服务器的 `__sentinel__:hello` 频道

Sentinel 默认会以每十秒一次的频率 , 通过命令连接向被监视的主服务器发送 INFO 命令 , 并通过分析 INFO 命令的回复来获取主服务器的当前信息

通过分析主服务器返回的 INFO 命令回复 , Sentinel 可以获取以下两方面的信息 : 

- 一方面是关于主服务器本身的信息 , 包括 `run_id` 域记录的服务器运行 ID , 以及 role 域记录的服务器角色
- 另一方面是关于主服务器属下所有从服务器的信息 , 每个从服务器都由一个 "slave" 字符串开头的行记录 , 每行的 `ip=` 域记录了从服务器的 IP 地址 , 而 `port=` 域则记录了从服务器的端口号 , 根据这些 IP 地址和端口号 , Sentinel 无须用户提供从服务器的地址信息 , 就可以自动发现从服务器

## 检测主观下线状态  🍀

在默认情况下 , Sentinel 会以每秒一次的频率向所有与它创建了命令连接的实例 (包括主服务器 , 从服务器 , 其他 Sentinel 在内) 发送 PING 命令 , 并通过实例返回的 PING 命令回复来判断实例是否在线

Sentinel 配置文件中的 `down-after-milliseconds` 毫秒内 , 连续向 Sentinel 返回无效回复 , 那么 Sentinel 会修改这个实例所对应的实例结构 , 在结构的 flags 属性中打开 SRI_S_DOWN 标识 , 以此来标识这个实例已经进入主观下线状态

用户设置的 `down-after-milliseconds` 选项的值 , 不仅会被 Senitinel 用来判断主服务器的主观下线状态 , 还会被用于判断主服务器属下的所有从服务器 , 以及所有同样监视这个主 服务器的其他 Sentinel 的主观下线状态 

## 检测客观下线状态  🍀

当 Sentinel 将一个主服务器判断为主观下线之后 , 为了确认这个主服务器是否真的下线了 , 它会向同样监视这一主服务器的其他 Sentinel 进行询问 , 看它们是否也认为主服务器已经进入了下线状态 (可以是主观下线或者客观下线) , 当 Sentinel 从其他 Sentinel 那里接收到足够数量的已下线判断之后 , Sentinel 就会将从服务器判定为客观下线 , 并对主服务器执行故障转移操作

## 选举领头 Sentinel  🍀

当一个主服务器被判断为客观下线时 , 监视这个下线主服务器的各个 Sentinel 会进行协商 , 选举出一个领头 Sentinel , 并由领头 Sentinel 对下线主服务器执行故障转移操作

故障转移操作包括以下三个步骤 : 

1. 在已下线主服务器属下的所有从服务器里面 , 挑选一个从服务器 , 并将其转换为主服务器
2. 让已下载主服务器属下的所有从服务器改为复制新的主服务器
3. 将已下线主服务器设置为新的主服务器的从服务器 , 当这个旧的主服务器重新上线时 , 它就会成为新的主服务器的从服务器