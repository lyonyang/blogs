# CentOS安装InfluxDB

## 安装

```bash
$ wget https://dl.influxdata.com/influxdb/releases/influxdb-1.8.2.x86_64.rpm
$ yum localinstall influxdb-1.8.2.x86_64.rpm
```

## 启动

```bash
$ systemctl start influxdb  #启动
$ systemctl restart influxdb  #重启
$ systemctl status influxdb  #查看状态
```

## 创建用户

```bash
$ influx
> CREATE USER root WITH PASSWORD '123456' WITH ALL PRIVILEGES
```

## 配置权限

```bash
$ vim /etc/influxdb/influxdb.conf 
auth-enabled = false # 把这个配置改成 true
$ systemctl restart influxdb  #重启
```

## 登录

```bash
$ influx -username root -password 123456
```

