# CentOS安装Supervisor

## 安装

```bash
$ pip install supervisor
```

## 创建配置文件

```bash
$ mkdir /opt/supervisor
$ echo_supervisord_conf > /opt/supervisor/supervisord.conf
```

修改配置文件

```conf
[unix_http_server]
file=/opt/supervisor/supervisor.sock   ; the path to the socket file
;chmod=0700                 ; socket file mode (default 0700)
;chown=nobody:nogroup       ; socket file uid:gid owner
;username=user              ; default is no username (open server)
;password=123               ; default is no password (open server)

;[inet_http_server]         ; inet (TCP) server disabled by default
;port=127.0.0.1:9001        ; ip_address:port specifier, *:port for all iface
;username=user              ; default is no username (open server)
;password=123               ; default is no password (open server)

[supervisord]
logfile=/opt/supervisor/supervisord.log ; main log file; default $CWD/supervisord.log
logfile_maxbytes=50MB        ; max main logfile bytes b4 rotation; default 50MB
logfile_backups=10           ; # of main logfile backups; 0 means none, default 10
loglevel=info                ; log level; default info; others: debug,warn,trace
pidfile=/opt/supervisor/supervisord.pid ; supervisord pidfile; default supervisord.pid
nodaemon=false               ; start in foreground if true; default false
minfds=16384                  ; min. avail startup file descriptors; default 1024
minprocs=600                 ; min. avail process descriptors;default 200

[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[supervisorctl]
serverurl=unix:///opt/supervisor/supervisor.sock ; use a unix:// URL  for a unix socket

[include]
files = /opt/supervisor/*.ini
```

## 启动

先启动 `supervisord` 

```bash
$ supervisord -c /opt/supervisor/supervisord.conf
```

再启动 `supervisorctl`

```bash
$ supervisorctl -c /opt/supervisor/supervisord.conf
$ supervisorctl -c /usr/lib/supervisor/supervisord.conf reload # 重启supervisor
$ supervisorctl -c /usr/lib/supervisor/supervisord.conf restart # 重启某个conf，加 all 指重启全部
$ supervisorctl -c /usr/lib/supervisor/supervisord.conf update # 更新全部conf文件
```

