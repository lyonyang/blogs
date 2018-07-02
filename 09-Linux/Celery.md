# Celery

## 介绍  🍀

Celery 是一个专注于实时处理和任务调度的分布式任务队列 , 所谓任务就是消息 , 消息中的有效载荷中包含要执行任务需要的全部数据

使用 Celery 的常见场景如下 : 

- Web 应用 , 当用户触发的一个操作需要较长时间才能执行完成时 , 可以把它作为任务交给 Celery 去异步执行 , 执行完再返回给用户 , 这段时间用户不需要等待 , 提高了网站的整体吞吐量和响应时间
- 定时任务 , 生产环境经常会跑一些定时任务 , Celery 可以帮助我们快速在不同的机器设定不同中任务
- 其他可以异步执行的任务 , 为了充分提高网站性能 , 对于请求和响应之外的那些不要求必须同步完成的附加工作都可以异步完成 , 比如发送短信/邮件 , 推送消息 , 清理/设置缓存等

Celery 提供的特性 : 

1. 方便地查看定时任务的执行情况 , 比如执行是否成功 , 当前状态 , 执行任务花费的时间等
2. 可以使用功能齐备的管理后台或者命令行添加 , 更新 , 删除任务
3. 方便把任务和配置管理相关联
4. 可选多进程 , Eventlet 和 Gevent 三种模式并发执行
5. 提供错误处理机制
6. 提供多种任务原语 , 方便实现任务分组 , 拆分和调用链
7. 支持多种消息代理和存储后端

## 组件  🍀

Celery包含如下组件 :

-  Celery Beat : 任务调度器 , Beat进程会读取配置文件的内容 , 周期性地将配置中到期需要执行的任务发送给任务队列
- Celery Worker : 执行任务的消费者 , 通常会在多台服务器运行多个消费者来提高执行效率 
- Broker : 消息代理 , 或者叫作消息中间件 , 接受任务生产者发送过来的任务消息 , 存进队列再按序分发给任务消费方(通常是消息队列或者数据库)
- Producer : 调用了Celery提供的API、函数或者装饰器而产生任务并交给任务队列处理的都是任务生产者
- Result Backend : 任务处理完后保存状态信息和结果 , 以供查询 , Celery默认已支持Redis、RabbitMQ、MongoDB、Django ORM、SQLAlchemy等方式

其工作流程如下 : 

![Celery架构](http://oux34p43l.bkt.clouddn.com/Celery架构.png)

## 选择消息代理  🍀

Celery 目前支持 RabbitMQ , Redis , MongoDB , Beanstalk ,SQLAlchemy , Zookeeper 等作为消息代理 , 但适用于生产环境的只有 RabbitMQ 和 Redis

Celery 官方推荐使用 RabbitMQ , Celery 作者 Ask Solem Hoel 最初在 VMware 就是为 RabbitMQ 工作的 , Celery 最初的设计就是基于 RabbitMQ , 所以使用 RabbitMQ 会非常稳定

## Celery 序列化  🍀

在客户端和消费者之间传输数据需要序列化和反序列化 , Celery 支持方案如下 : 

![Celery序列化方案](http://oux34p43l.bkt.clouddn.com/Celery序列化方案.jpg)

## 安装配置 Celery  🍀

为了提供更高的性能 , 选择方案如下 : 

- 选择 RabbitMQ 作为消息代理
- RabbitMQ 的 Python 客户端选择 librabbitmq 这个C库
- 选择Msgpack做序列化
- 选择Redis做结果存储

Celery 提供 bundles 的方式安装 , 也就是安装 Celery 的同时可以一起安装多种依赖 :

```shell
$ pip install "celery[librabbitmq,redis,msgpack]"
```