# Django - Django初识








<extoc></extoc>

## 介绍

通过上一篇整理 , 对于Web框架应该清晰了很多 , 当然上一篇仅仅是自定义了一个最low , 最底端的Web框架 , 基本仅能处理特定的HTTP请求 , 那么这一章就开始学习Python Web框架中的王牌——Django

Django本身集成了ORM , 模型绑定 , 模板引擎 , 缓存 , Session等诸多功能

Django是一个基于MVC模式构造的框架 , 但是在Django中 , 控制器接受用户输入的部分由框架自行处理 , 所以 Django 里更关注的是模型 (Model)  , 模板 (Template) 和视图 (Views) , 即MTV模式 , 它们各自的职责如下

| 层次                     | 职责                                       |
| ---------------------- | ---------------------------------------- |
| 模型 (Model) , 即数据存取层    | 处理与数据相关的所有事务 :  如何存取、如何验证有效性、包含哪些行为以及数据之间的关系等 |
| 视图 (View) , 即表现层       | 处理与表现相关的决定 :  如何在页面或其他类型文档中进行显示          |
| 模板 (Template) , 即业务逻辑层 | 存取模型及调取恰当模板的相关逻辑 , 模型与模板的桥梁              |

**安装**

```cmd
$pip install django
```

**获取版本**

```python
>>> import django
>>> django.get_version()
'1.10.8'
```

**添加环境变量**

```
C:\Python3.5\Scripts  - 具体路径自行添加
```

## 创建一个Django项目

我们使用命令行来进行创建 , 命令如下

```cmd
django-admin startproject mysite  - 当前目录下创建
# IDE创建Django程序时本质上都是自动执行了该命令
```

创建成功后可见

```python
mysite
├── mysite             # 对整个程序进行配置
│   ├── __init__.py
│   ├── settings.py    # 配置文件
│   ├── urls.py        # URL对应关系
│   └── wsgi.py        # 一个WSGI兼容的Web服务器入口,以便运行你的项目,上线uwsgi + nginx
├── db.sqlite3         # 默认使用sqlite
└── manage.py          # 用户管理Django的工具
```

**PS : 如果我们使用`Pycharm` 来完成这项操作 , 那么其还会为我们自动创建一个`templates` 文件夹 , 用于存放模板** 

## 启动Django项目

创建完成后我们就可以通过以下命令启动Django项目了

```python
python manage.py runserver 0.0.0.0:8000
'''
0.0.0.0:让其他电脑可连接到开发服务器
8000:端口,如果不说明,默认为8000
'''
```

启动项目后我们就可以在浏览器输入服务器的IP及端口进行访问了 , 即在浏览器输入`http://127.0.0.1:8000` 

![runserver](http://oux34p43l.bkt.clouddn.com/runserver.png?imageMogr2/blur/1x0/quality/75|watermark/2/text/bHlvbi55YW5nQHFxLmNvbQ==/font/YXBhcmFqaXRh/fontsize/560/fill/Izk0ODI4Mg==/dissolve/100/gravity/SouthEast/dx/10/dy/10)

## 创建一个Django模型

Django规定 , 如果要使用应用模型 , 必须要创建一个app

执行如下命令创建app

```cmd
python manage.py startapp blog  - 同样在manage.py所在目录下执行
```

创建完成后就可以看到如下文件了

```python
blog
├── migrations         # 数据库相关目录
|   └── __init__.py     
├── __init__.py        
├── admin.py           # admin后台管理文件
├── apps.py            # 应用文件
├── models.py          # 模型文件
├── tests.py           # 测试文件
└── views.py           # 对整个程序进行配置
```

**PS : 我们每创建一个模型 , 都需要在`settings.py` 中添加配置 , 如下所示** 

```python
# mysite\settings.py
"""截取文件中的片段"""
# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',   # 此行为添加的配置
]
```

## 同步数据库

在同步数据库之前需要先生成同步数据库的脚本 , 一般我们创建一个模型时这一步都自动为我们生成了 , 如果没有 , 则可以使用如下命令生成同步数据库的脚本

```cmd
python manage.py makemigrations
```

而后进行同步数据库

```cmd
python manage.py migrate
```

## 访问admin

django admin是django提供的一个后台管理页面 , 如果我们使用django admin则需要提前创建好后台管理员 (超级用户) , 以及url的配置

创建后台管理员

```cmd
python manage.py createsuperuser
```

配置后台管理url

```python
# mysite\urls.py
urlpatterns = [
    url(r'^admin/', admin.site.urls),
]
'''当然这一步实际上我们创建Django项目时就为我们自动完成了'''
```

于是我们就可以访问admin了 , 即浏览器中访问`http://127.0.0.0:8000/admin/` 

其他命令如下

```cmd
python manage.py flush          - 清空数据库
django-admin.py help startapp   - 查询某个命令的详细信息
python manage.py shell          - 启动交互界面
```

本篇仅仅对Django做一个简单的介绍 , 详细内容见后续文章
