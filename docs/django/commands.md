# Django - Django命令整理








<extoc></extoc>

## 介绍

django-admin是用于管理Django的命令行工具集 , 此外在每个Django项目中会自动为我们生成一个manage.py , 它与django-admin相同 , 但是会帮我们处理以下几件事情 : 

- 它将为你的项目包添加环境变量
- 它用于设置DJANGO_SETTINGS_MODULE环境变量 , 因此它指向项目的settings.py文件

在我们编写项目时 , 通常使用`manage.py`会比`django-admin`方便些 , 但是如果我们需要在多个Django项目的settings文件中切换 , 可以使用`django-admin`加上`DJANGO_SETTINGS_MODULE`或者`--settings`参数

**用法**

```shell
$ django-admin <command> [options]
$ manage.py <command> [options]
$ python -m django <command> [options]
```

对于以上三种方式的命令格式 , 其command与options都是一致的 , 哪一种格式都能达到我们的要求 , 通常我们使用manage.py格式是最多的 , 所以下面就以manage.py为示例了 

```shell
$ python manage.py <command> [options]
```

后续省略开头的python进行示例

## 基础命令

```shell
# 显示使用信息和每个应用的命令列表
$ manage.py help

# 显示包含所有可用命令的列表
$ manage.py help --comands

# 显示某一个命令的描述及可用的命令列表
$ manage.py help <command>

# 获取django版本
$ manage.py version

# 创建Django项目
$ django-admin startproject name [directory]

# 运行所有已安装的测试程序
$ manage.py test

# 启动本地Web服务器
$ manage.py runserver [addrport]

# 将迁移添加到migrations目录
$ manage.py makemigrations

# 迁移数据库
$ manage.py migrate

# 进行数据迁移并返回所执行的SQL语句
$ manage.py sqlmigrate 

# 刷新数据库
$ manage.py flush

# 检查项目中的任何问题,而不进行迁移和访问数据库
$ manage.py check [app_label [app_label ...]] 

# 创建缓存表
$ manage.py createcachetable

# 运行ENGINE设置中指定的数据库引擎命令行客户端
$ manage.py dbshell

# 显示当前setting文件与Django默认settings文件之间的差异
$ manage.py diffsettings       # 显示结果中"###"表示默认设置中没有定义的设置

# 发送测试电子邮件
$ manage.py sendtestemial [email] [email ...]]

# 启动Python交互式解释器
$ manage.py shell -i {ipython,bpython,python}

# 创建应用
$ manage.py startapp name [directory]

# 创建超级用户
$ manage.py createsuperuser

# 指定控制台打印的通知和调试信息量,以migrate为例
$ manage.py migrate --verbosity 2    # --verbosity {0,1,2,3}, -v {0,1,2,3}
'''
0,无输出
1,正常输出(默认)
2,详细输出
3,非常详细输出
'''
```

## 代码执行命令

```python
# 不带参数
from django.core import management
from django.core.management.commands import loaddata

management.call_command('flush', verbosity=0, interactive=False)
management.call_command('loaddata', 'test_data', verbosity=0)
management.call_command(loaddata.Command(), 'test_data', verbosity=0)

# 带参数
# Similar to the command line
management.call_command('dumpdata', '--natural-foreign')

# Named argument similar to the command line minus the initial dashes and
# with internal dashes replaced by underscores
management.call_command('dumpdata', natural_foreign=True)

# `use_natural_foreign_keys` is the option destination variable
management.call_command('dumpdata', use_natural_foreign_keys=True)
```

更多详细内容 : [django-admin and manage.py](https://docs.djangoproject.com/en/1.11/ref/django-admin/) 