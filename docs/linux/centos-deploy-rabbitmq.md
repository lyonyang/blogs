# CentOS安装RabbitMQ

## 安装RabbitMQ

安装 `Erlang` 

```bash
$ yum install epel-release
$ wget https://packages.erlang-solutions.com/erlang/rpm/centos/7/x86_64/esl-erlang_22.1-1~centos~7_amd64.rpm
$ yum install esl-erlang_22.1-1~centos~7_amd64.rpm
```

安装 `RabbitMQ`

```bash
$ wget https://mirrors.huaweicloud.com/rabbitmq-server/v3.7.21/rabbitmq-server-3.7.21-1.el7.noarch.rpm
```

导入GPG密钥

```bash
$ rpm –import https://www.rabbitmq.com/rabbitmq-release-signing-key.asc
```

安装

```bash
$ rpm -Uvh rabbitmq-server-3.7.21-1.el7.noarch.rpm
```

## 启动RabbitMQ

```bash
# 后台启动
$ rabbitmq-server -detached
# 启动管理插件
$ rabbitmq-plugins enable rabbitmq_management
# 关闭管理插件
$ rabbitmq-plugins disable rabbitmq_management
```

## 常用命令

```bash
# 查看用户
$ rabbitmqctl list_users
# 添加管理用户
$ rabbitmqctl add_user admin yourpassword   # 增加普通用户
$ rabbitmqctl set_user_tags admin administrator    # 给普通用户分配管理员角色 
# 创建vhost
$ rabbitmqctl add_vhost test
# 赋予用户vhost操作权限
$ rabbitmqctl set_permissions -p test admin ".*" "
# 查看用户的权限
$ rabbitmqctl list_user_permissions username 
```

