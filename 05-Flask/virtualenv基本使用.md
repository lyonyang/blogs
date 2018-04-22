# virtualenv基本使用

## 介绍

随着我们所开发或者管理的项目越来越多 , 这就导致了有可能存在不同版本的Python , 又或者是不同版本的Python库 , 于是问题就出现了 , 库的版本问题颇快了向后兼容性的情况相当常见 , 而且零依赖的正式应用也不大可能存在 , 所以项目中的两个或者更多出现依赖性冲突就会频繁出现

所以 , 为了解决这些冲突 , virtualenv出现了 , virtualenv能够允许多个不同版本的Python安装 , 每一个服务与各自的项目 , 但是它并不是分别独立安装一个Python的副本 , 而是提供了一种方式使得环境保持独立

## 安装virtualenv

实际上 , virtualenv就是一个Python库 , 所以我们可以使用pip等命令进行安装

Mac OS X 或者 Linux 下

```shell
$ sudo pip install virtualenv
```

如果使用Ubuntu , 请尝试

```shell
$ sudo apt-get install python-virtualenv
```

在 Windows 下

```shell
$ pip install virtualenv
```



## 创建虚拟环境

通常我们会先创建一个项目文件夹 , 在其下创建venv虚拟环境 :

```shell
$ mkdir myproject
$ cd myproject
$ virtualenv venv
New python executable in venv/bin/python
Installing distribute............done.
```

指定Python解释器

```shell
$ virtualenv -p /usr/bin/python2.7 venv
```

## 激活虚拟环境

在OS X 和Linux 下

```shell
$ . venv/bin/activate
```

在 Windows 下

```shell
$ venv\scripts\activate
```

## 退出虚拟环境

在OS X 和Linux 下

```shell
$ . venv/bin/deactivate
```

在 Windows 下

```shell
$ venv\scripts\deactivate.bat
```
