# CentOS安装Grafana

## 安装Grafana

```bash
# 官网下载地址: https://grafana.com/grafana/download
$ wget https://dl.grafana.com/enterprise/release/grafana-enterprise-8.4.0.linux-amd64.tar.gz
$ tar -zxvf grafana-enterprise-8.4.0.linux-amd64.tar.gz
```

## 启动Grafana

```bash
$ ./grafana-server
# 后台启动
$ nohup ./grafana-server &
```

`Grafana` 默认端口为 3000 , 初始账号密码 `admin/admin` , 第一次登录会要求修改密码



