# CentOS安装Kafka

## 安装JDK

```bash
$ yum list java-1.8*
yum install java-1.8.0-openjdk* -y
java -version
```

## 安装Zookeeper

```bash
$ wget https://mirrors.bfsu.edu.cn/apache/zookeeper/zookeeper-3.7.0/apache-zookeeper-3.7.0-bin.tar.gz
$ tar -zxvf apache-zookeeper-3.7.0-bin.tar.gz
```

修改 `zookeeper` 配置

```bash
$ cp apache-zookeeper-3.7.0-bin/conf/zoo_sample.cfg  apache-zookeeper-3.7.0-bin/conf/zoo.cfg
$ vim apache-zookeeper-3.7.0-bin/conf/zoo.cfg

dataDir=apache-zookeeper-3.7.0-bin/data		#修改数据存放目录
dataLogDir=apache-zookeeper-3.7.0-bin/log
```

启动 `zookeeper` 

```bash
$ cd apache-zookeeper-3.7.0-bin/bin
# 后台启动
$ nohup apache-zookeeper-3.7.0-bin/bin/zkServer.sh start &
```

## 安装Kafka

```bash
$ wget https://archive.apache.org/dist/kafka/2.8.0/kafka_2.12-2.8.0.tgz
$ tar -zxvf kafka_2.12-2.8.0.tgz
```

修改 `Kafka` 配置

```bash
$ vim kafka_2.12-2.8.0/config/server.properties

# broker 的编号，如果集群中有多个 broker，则每个 broker 的编号需要设置的不同
broker.id=0
# 31 行
listeners=PLAINTEXT://your.host.name:9092
# 123 行，修改 zookeeper.connect 为自己的 IP:PORT
zookeeper.connect=localhost:2181/kafka
# 存放消息日志文件的地址
log.dirs=/data/kafka-logs
```

`server.properties` 配置详解

```bash
//当前机器在集群中的唯一标识，和zookeeper的myid性质一样（broker.id和host.name每个节点都不相同）
broker.id=0

//当前kafka对外提供服务的端口默认是9092
listeners=PLAINTEXT://hostname:9092

//这个参数默认是关闭的，在0.8.1有个bug，DNS解析问题，失败率的问题。
host.name=hadoop1

//这个是borker进行网络处理的线程数
num.network.threads=3

//这个是borker进行I/O处理的线程数
num.io.threads=8

//发送缓冲区buffer大小，数据不是一下子就发送的，先回存储到缓冲区了到达一定的大小后在发送，能提高性能
socket.send.buffer.bytes=102400

//kafka接收缓冲区大小，当数据到达一定大小后在序列化到磁盘
socket.receive.buffer.bytes=102400

//这个参数是向kafka请求消息或者向kafka发送消息的请请求的最大数，这个值不能超过java的堆栈大小
socket.request.max.bytes=104857600

//消息存放的目录，这个目录可以配置为“，”逗号分割的表达式，上面的num.io.threads要大于这个目录的个数这个目录，
//如果配置多个目录，新创建的topic他把消息持久化的地方是，当前以逗号分割的目录中，那个分区数最少就放那一个
log.dirs=/home/hadoop/log/kafka-logs

//默认的分区数，一个topic默认1个分区数
num.partitions=1

//每个数据目录用来日志恢复的线程数目
num.recovery.threads.per.data.dir=1

//默认消息的最大持久化时间，168小时，7天
log.retention.hours=168

//轮转时间，当需要删除指定小时之前的数据时，该设置项很重要
log.roll.hours=12

//这个参数是：因为kafka的消息是以追加的形式落地到文件，当超过这个值的时候，kafka会新起一个文件
log.segment.bytes=1073741824

//每隔300000毫秒去检查上面配置的log失效时间
log.retention.check.interval.ms=300000

//是否启用log压缩，一般不用启用，启用的话可以提高性能
log.cleaner.enable=false

//设置zookeeper的连接端口
zookeeper.connect=192.168.123.102:2181,192.168.123.103:2181,192.168.123.104:2181

//设置zookeeper的连接超时时间
zookeeper.connection.timeout.ms=6000
```

启动 `Kafka`

```bash
$ nohup kafka_2.12-2.8.0/bin/kafka-server-start.sh kafka_2.12-2.8.0/config/server.properties
```

## 测试

```bash
# topic 是发布消息的 category，以单节点的配置创建了一个叫 dblab01 的 topic.可以用 list 列出所有创建的 topics，来查看刚才创建的主题是否存在
kafka_2.12-2.8.0/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test

kafka_2.12-2.8.0/bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic test

kafka_2.12-2.8.0/bin/kafka-topics.sh --list --zookeeper localhost:2181

kafka_2.12-2.8.0/bin/kafka-console-producer.sh --broker-list PLAINTEXT://localhost:9092 --topic test

kafka_2.12-2.8.0/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning
```

