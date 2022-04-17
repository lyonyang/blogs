# CentOS安装Nginx

## 安装依赖

```shell
$ sudo yum install gcc-c++

$ sudo yum install -y openssl openssl-devel pcre pcre-devel zlib zlib-devel
```

## 安装Nginx

```shell
$ wget https://nginx.org/download/nginx-1.19.9.tar.gz

# 解压
$ tar -zxvf nginx-1.19.9.tar.gz

$ cd nginx-1.19.9

# 编译安装, 指定目录 /usr/local/nginx
$ sudo ./configure --prefix=/usr/local/nginx --with-http_stub_status_module --with-http_ssl_module

$ sudo make

$ sudo make install
```

## 默认Nginx配置

**创建日志目录**

```shell
$ sudo mkdir -p /data/logs/nginx/error /data/logs/nginx/logs /data/logs/nginx/info /data/logs/nginx/access 
```

**配置文件**

```yaml
user  root;
worker_processes auto;
error_log  /data/logs/nginx/error/log;
pid        /data/logs/nginx/logs/nginx.pid;
worker_rlimit_nofile 51200;

events {
        use epoll;
        worker_connections 51200;
        multi_accept on;
}

http {
        include       mime.types;
        default_type  application/octet-stream;
        uwsgi_connect_timeout 600s;
        server_names_hash_bucket_size 512;
        client_header_buffer_size 32k;
        large_client_header_buffers 4 32k;
        client_max_body_size 1000m;
        client_header_timeout 600s;
    	  client_body_timeout 600;
        sendfile   on;
        tcp_nopush on;

        keepalive_timeout 1800;
        tcp_nodelay on;

        send_timeout 600;

        fastcgi_connect_timeout 600;
        fastcgi_send_timeout 600;
        fastcgi_read_timeout 600;
        fastcgi_buffer_size 256k;
        fastcgi_buffers 16 256k;
        fastcgi_busy_buffers_size 512k;
        fastcgi_temp_file_write_size 512k;
		    fastcgi_intercept_errors on;

        gzip on;
        gzip_min_length  1k;
        gzip_buffers     4 16k;
        gzip_http_version 1.1;
        gzip_comp_level 2;
        gzip_types     text/plain application/javascript application/x-javascript text/javascript text/css application/xml;
        gzip_vary on;
        gzip_proxied   expired no-cache no-store private auth;
        gzip_disable   "MSIE [1-6]\.";

        limit_conn_zone $binary_remote_addr zone=perip:10m;
		limit_conn_zone $server_name zone=perserver:10m;

        server_tokens off;
        log_format _main '$remote_addr $http_host "$time_iso8601" $request_method $http_cookie "$http_token" "$uri" "$args" "$request_body" $status $body_bytes_sent $request_time "$http_user_agent"';

	      access_log /data/logs/nginx/access/log.pipe _main;
}
```

## 启动Nginx

```bash
# 启动nginx
$ /usr/local/nginx -c /usr/local/nginx/conf/nginx.conf
# 重启nginx
$ /usr/local/nginx -s reload
# 检查nginx配置
$ /usr/local/nginx -t
```

