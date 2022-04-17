# CentOS安装Python

## .configure 失败

缺少C++编译器, 解决方法

```shell
$ yum install -y gcc-c++
```

## Python

### 下载源码

Python源码地址 : `https://www.python.org/ftp/python/`

以 `Python 3.6.3` 为例 : 

```shell
$ wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tgz
```

下载完成后解压

```shell
$ tar -zxvf Python-3.6.3.tgz
```

编译安装

```shell
$ ./configure --prefix=/usr/local/python3
$ make 
$ make install
```

