# CentOS安装Prometheus

## 安装Prometheus

```bash
$ wget https://mirrors.bfsu.edu.cn/github-release/prometheus/prometheus/2.33.3%20_%202022-02-11/prometheus-2.33.3.linux-amd64.tar.gz
$ tar -zxvf prometheus-2.33.3.linux-amd64.tar.gz
```

## 安装node-exporter

```bash
$ wget https://github.com/prometheus/node_exporter/releases/download/v1.3.1/node_exporter-1.3.1.linux-amd64.tar.gz
$ tar -zxvf node_exporter-1.3.1.linux-amd64.tar.gz
```

## 启动node-exporter

```bash
$ node_exporter-1.3.1.linux-amd64/node_exporter --web.listen-address 0.0.0.0:9100
$ nohup node_exporter-1.3.1.linux-amd64/node_exporter --web.listen-address 0.0.0.0:9100 &
```

## Promehteus.yml说明

 `prometheus-2.33.3.linux-amd64/prometheus.yml`  

```bash
global    # 此片段指定的是prometheus的全局配置， 比如采集间隔，抓取超时时间等。
rule_files   # 此片段指定报警规则文件， prometheus根据这些规则信息，会推送报警信息到alertmanager中。
scrape_configs    # 此片段指定抓取配置，prometheus的数据采集通过此片段配置。
alerting    # 此片段指定报警配置， 这里主要是指定prometheus将报警规则推送到指定的alertmanager实例地址。
remote_write    # 指定后端的存储的写入api地址。
remote_read    # 指定后端的存储的读取api地址
scrape_interval  # 抓取间隔,默认继承global值。
scrape_timeout   # 抓取超时时间,默认继承global值。
evaluation_interval # 评估规则间隔
external_labels  # 外部一些标签设置
metric_path     # 抓取路径， 默认是/metrics
scheme # 指定采集使用的协议，http或者https。
params # 指定url参数。
basic_auth # 指定认证信息。
*_sd_configs # 指定服务发现配置
static_configs # 静态指定服务job。
relabel_config # relabel设置。
```

## 配置node-exporter

```bash
vim prometheus.yml

scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: "prometheus"

    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.

    static_configs:
      - targets: ["ip:9090"]
	# 添加node-exporter
  - job_name: 'node'

    scrape_interval: 5s

    static_configs:
       # 其它主机上的exporter只用将localhost改为主机IP，不同的主机之间 , 隔开
       - targets: ["ip:9100"] 
```

## 启动Prometheus

```bash
# --config.file 指定配置文件   --storage.tsdb.path 指定数据存放目录
$ cd prometheus-2.33.3.linux-amd64
$ ./prometheus --config.file=prometheus.yml --storage.tsdb.path=/data/prometheus

# 后台启动
$ nohup ./prometheus --config.file=prometheus.yml --storage.tsdb.path=/data/prometheus &
```

访问 `http://ip:9090/targets` 就可以看到 `node` 的相关信息了

不过 `Prometheus` 自带的监控面板内容不太直观 . 我们需要通过 `Grafana` 来进行数据可视化

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

## 配置Grafana

`Grafana` 默认端口为 3000 , 初始账号密码 `admin/admin` , 第一次登录会要求修改密码

点击 `Add your first data source` 添加数据源

选择 `Prometheus` , 填写好相关配置保存之后 

再导入模板 (点击加号后再点击 `import` , 即可进入模板配置页面) , 我们可以使用 `9276` 或者到 `https://grafana.com/grafana/dashboards/` 自己进行选择



