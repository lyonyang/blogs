# RabbitMQ

## 介绍  🍀

RabbitMQ 是一个实现了 AMQP 协议标准的开源消息代理和队列服务器 , 和 Beanstalkd 不同的是 , 它是企业级消息系统 , 自带了集群 , 管理 , 插件系统等特性 , 在高可用性 , 可扩展性性 , 易用性等方面做得很好 , 现在被互联网公司广泛使用

安装服务端

```shell
$ sudo apt-get install rabbitmq-server -yq
```

安装客户端

```shell
$ pip install pika
```

## AMQP  🍀

AMQP (Advanced Message Queuing Protocol , 高级消息队列协议) 是一个异步消息传递所使用的应用层协议规范 , 它的设计初衷是为了摆脱商业 MQ 高额费用和不同 MQ 供应商的接口不统一的问题 , 所以一开始就设计成开放标准 , 以解决企业复杂的消息队列需求问题

基本概念 : 

1. 消息 : 消息实际包含两部分内容 : 
   1. 有效载荷 , 也就是传输的数据 , 数据类型可以纯文本也可以是 JSON
   2. 标签 , 它包含交换机的名字和可选的主题标记等 , AMQP 仅仅描述了标签 , 而RabbitMQ 决定了把这个消息发给哪个消费者
2. 发布者 : 也就是生产者 , 它创建消息并且设置标签
3. 消费者 : 消费者连接到代理服务器上 , 接收消息的有效载荷 (注意 , 消费者并不需要消息中的标签)

在 AMQP 模块中 , 为了保证消息被正确取出并执行 , 消息投递失败后会重发 , 于是有了一个消息确认的概念 : 当一个消息从队列中投递给消费者后 , 消费者会通知消息代理 (Broker) , 这个通知可以是自动完成的 , 也可以由处理消息的应用来执行 , 当消息确认 (Ack) 被启用的时候 , 消息代理不会完全将消息从队列中删除 , 除非收到来自消费者的确认回执

AMQP 工作流程如下 : 

![工作流程](http://oux34p43l.bkt.clouddn.com/工作流程.png)

消息发布者发送消息 , 交换机拿到消息后会将它路由给队列 , 它使用哪种路由算法是由交换机类型和被称作 "绑定" 的规则所决定的 , 目前 RabbitMQ 提供了如下四种交换机 : 

1. 直接交换机 : 根据消息携带的路由建将消息投递给对应队列
2. 主题交换机 : 通过对消息的路由建和队列到交换机的绑定模式之间的匹配 , 将消息路由给一个或多个队列
3. 扇形交换机 : 将消息路由给绑定到它身上的所有队列 , 且不理会绑定的路由建 , 扇形交换机用来处理消息的广播路由
4. 头交换机 : 一般用不到 , 允许匹配 AMQP 的头而非路由建 , 和直接交换机差不多 , 但是性能差很多

## 简单示例  🍀

发布者

```python
import sys

import pika

# %2F是被转义的/,这里使用了默认的虚拟主机,默认的guest这个账号和密码
parameters = pika.URLParameters('amqp://guest:guest@localhost:5672/%2F')

# connection就是所谓的消息代理
connection = pika.BlockingConnection(parameters)  
# 获得信道
channel = connection.channel()  

# 声明交换机,指定交换类型为直接交换,最后2个参数表示想要持久化的交换机
channel.exchange_declare(exchange='web_develop', exchange_type='direct',
                         passive=False, durable=True, auto_delete=False)
if len(sys.argv) != 1:
    # 使用命令行参数作为消息体
    msg = sys.argv[1]  
else:
    msg = 'hah'

# 创建一个消息, delivery_mode为2表示让这个消息持久化, 重启RabbitMQ也不会丢失
props = pika.BasicProperties(content_type='text/plain', delivery_mode=2)
# basic_publish表示发送路由键为xxx_routing_key,消息体为haha的消息给web_develop这个交换机
channel.basic_publish('web_develop', 'xxx_routing_key', msg,
                      properties=props)
# 关闭连接
connection.close()  
```

消费者

```python
import pika


# 处理接收到的消息的回调函数
# method_frame携带了投递标记, header_frame表示AMQP信息头的对象
# body为消息实体
def on_message(channel, method_frame, header_frame, body):
    # 消息确认, 确认之后才会删除消息并给消费者发送新的消息
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)
    print body

parameters = pika.URLParameters('amqp://guest:guest@localhost:5672/%2F')
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.exchange_declare(exchange='web_develop', exchange_type='direct',
                         passive=False, durable=True, auto_delete=False)
# 声明队列, 如果没有就创建
channel.queue_declare(queue='standard', auto_delete=True)
# 通过路由键将队列和交换机绑定
channel.queue_bind(queue='standard', exchange='web_develop',
                   routing_key='xxx_routing_key')

# 订阅队列
channel.basic_consume(on_message, 'standard')  

try:
    # 开始消费
    channel.start_consuming()  
except KeyboardInterrupt:
    # 退出消费
    channel.stop_consuming()  

connection.close()
```

[官方教程](http://www.rabbitmq.com/getstarted.html)