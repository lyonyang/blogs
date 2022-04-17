# CentOS搭建Gitlab

## 下载镜像

```shell
$ wget https://mirrors.tuna.tsinghua.edu.cn/gitlab-ce/yum/el7/gitlab-ce-14.4.2-ce.0.el7.x86_64.rpm --no-check-certificate
```

## 安装

```shell
$ yum install -y gitlab-ce-14.4.2-ce.0.el7.x86_64.rpm
```

安装成功之后会在 `/opt/gitlab` 目录下

安装依赖服务

```shell
$ yum -y install policycoreutils openssh-server openssh-clients postfix

# 设置开机启动
$ systemctl enable postfix && systemctl start postfix
```

## 修改配置文件

获取相应 `SSL` 证书 , 并将证书存放到 `/etc/gitlab/ssl/` 下

配置文件地址 : `/etc/gitlab/gitlab.rb` 

```shell
external_url 'https://gitlab.domain.com'
nginx['enable'] = true
nginx['redirect_http_to_https'] = true    #http重定向到https
nginx['ssl_certificate'] = "/etc/gitlab/ssl/gitlab.com.pem"    #放置对应的证书密钥
nginx['ssl_certificate_key'] = "/etc/gitlab/ssl/gitlab.com.key" #放置对应的证书密钥
```

## 启动

```shell
# 加载配置
$ gitlab-ctl reconfigure

# 启动
$ gitlab-ctl restart|start
```

## 汉化包

Gitlab 12 版本以上不需要汉化

```shell
wget https://gitlab.com/xhang/gitlab/-/archive/12-3-stable-zh/gitlab-12-3-stable-zh.tar.gz
cp  -r gitlab-12-3-stable-zh/*   /opt/gitlab/embedded/service/gitlab-rails/
```

重新启动

## 备份

```shell
$ gitlab-rake gitlab:backup:create
```

## 恢复

```shell
# 停止相关数据连接服务
$ gitlab-ctl stop unicorn        
$ gitlab-ctl stop sidekiq
```

```shell
$ gitlab-rake gitlab:backup:restore BACKUP=1636682101_2021_11_12_12.3.9
```

