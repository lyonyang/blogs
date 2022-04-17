# CentOS安装ElasticSearch

## 安装JDK

```bash
$ yum list java-11*
yum install java-11-openjdk* -y
java -version
```

## 安装ElasticSearch

```bash
# 因为ElasticSearch无法使用root用户启动, 所以我们可以放到opt下
$ cd /opt/
$ wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.17.0-linux-x86_64.tar.gz
$ tar -zxvf elasticsearch-7.17.0-linux-x86_64.tar.gz
```

## 修改配置

```bash
# /opt/elasticsearch-7.17.0/config/elasticsearch.yml

network.host: 0.0.0.0
http.port: 9200
node.name: node-1
cluster.initial_master_nodes: ["node-1"]
```

## 创建用户和用户组

 `ElasticSearch` 无法使用 `root` 用户启动

创建elsearch用户组及elsearch用户

```bash
$ groupadd elsearch
$ useradd user -g elsearch -p password
```

更改elasticsearch文件夹及内部文件的所属用户及组为elsearch:elsearch

```bash
$ chown -R elsearch:elsearch  /opt/elasticsearch
```

## 启动ElasticSearch

```bash
$ su elsearch 
$ cd /opt/elasticsearch-7.17.0/bin/
$ ./elasticsearch
# 后台启动
$ ./elasticsearch -d
```

