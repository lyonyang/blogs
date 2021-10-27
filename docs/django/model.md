# Django - Model








<extoc></extoc>

## 介绍

在我们的Web应用中 , 与数据库的交互不可避免 ; 数据库驱动网站在后台链接数据库服务器 , 从中取出一些数据 , 然后在Web页面用漂亮的格式展示这些数据 , 这就是我们需要的模型(Model)

我们知道Python中的`sqlalchemy` 是一个第三方的ORM框架 , Django中的Model也是通过ORM来进行数据库管理的

特点 : 

- 每个模型都是`django.db.models.Molde` 的一个Python子类
- 模型的每个属性都表示为数据库中的一个字段
- 一旦我们创建一个数据模型 , Django会自动为我们提供一个数据抽象API , [Making queries](https://docs.djangoproject.com/en/1.11/topics/db/queries/)

当我们执行`python manage.py startapp app_name` 命令时 , Django就已经为我们自动创建了一个`models.py` 文件 , 就是用来存放我们的模型定义的

注意 : 我们创建模型前 , 需要将数据库相关配置完成 , 方法见settings整理文章

## 简单示例

首先创建一个应用

```python
python manage.py startapp myapp
```

安装应用

```python
# settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',  # 此行为添加项
]
```

定义模型

```python
# myapp/models.py
# 导入models
from django.db import models
# 必须继承models.Model
class Userinfo(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=20)
```

生成模型

```python
# Django 1.6.x 及以下
python manage.py syncdb
# Django 1.7.x 及以上
python manage.py makemigrations  # 生成同步记录
python manage.py migrate         # 开始同步
```

这里我使用的是Django 1.7.x 及以上版本 , 可见信息如下 : 

```python
# 生成同步记录
mysite>python manage.py makemigrations
No changes detected
# 开始同步
mysite>python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying sessions.0001_initial... OK
# 默认使用sqlite
```

以上的Person模型会在数据库中创建这样一张表 : 

```mysql
CREATE TABLE myapp_userinfo (
    "id" serial NOT NULL PRIMARY KEY,
    "username" varchar(30) NOT NULL,
    "password" varchar(20) NOT NULL
);
```

注意 : 

- 表名称是根据模型中的某些元数据自动生成的 , 也可以重写 , [Table names](https://docs.djangoproject.com/en/1.11/ref/models/options/#table-names)
- id字段是Django自动为我们添加的一个主键 , 也可以重写 ,  [Automatic primary key fields](https://docs.djangoproject.com/en/1.11/topics/db/models/#automatic-primary-key-fields)
- Django会根据`settings.py` 中指定的数据库类型来使用相应的SQL语句

如果我们使用的数据库为MySQL :

- Django对于MySQL默认使用的是MySQLdb模块 , 而Python 3 中是没有MySQLdb的 , 使用的是pymsql , 所以我们需要添加以下内容

- ```python
  # mysite/__init__.py
  import pymysql
  pymysql.install_as_MySQLdb()　

  # settings
  DATABASES = {
      'default': {
      'ENGINE': 'django.db.backends.mysql',
      'NAME':'dbname',
      'USER': 'root',
      'PASSWORD': 'xxx',
      'HOST': '',
      'PORT': '',
      }
  }
  ```

## 添加数据

添加数据需要先创建对象 , 然后再执行save函数 , 相当于SQL中的INSERT

myapp/views.py

```python
# 一步完成:使用create函数
from django.http import HttpResponse
from myapp import models
def add_user(request):
    models.Userinfo.objects.create(username='Lyon', password='123456')
    # models.Userinfo.objects.create(**user1) user1={'username':'Lyon','password':'123465'}
    return HttpResponse('<h1 style="color: blue;">数据添加成功!</h1>')

# 先创建对象后执行操作:使用save函数
from django.http import HttpResponse
from myapp import models
def add_user(request):
    user1 = models.Userinfo(username='Lyon', password='123456')
    user1.save()
    return HttpResponse('<h1 style="color: blue;">数据添加成功!</h1>')
```

mysite/urls.py

```python
from myapp import views
urlpatterns = [
    url(r'^add_user/', views.add_user),
]
```

访问http://127.0.0.1:8000/testdb/ 完成添加

## 查询数据

myapp/views.py

```python
from myapp import models
def select_user(request):
    # 通过objects这个模型管理器的all()获得所有数据行,相当于SQL中的SELECT * FROM
    result = models.Userinfo.objects.all()
    # filter相当于SQL中的WHERE,可设置条件过滤结果
    response1 = models.Userinfo.objects.filter(id=1)
    # 获取单个对象
    response2 = models.Userinfo.objects.get(id=1)
    # 限制返回的数据,相当于SQL中的OFFSET 0 LIMIT 2;
    models.Userinfo.objects.order_by('username')[0:2]
	# 数据排序
    models.Userinfo.objects.order_by("id")
    # 上面的方法可以连锁使用
    models.Userinfo.objects.filter(username="Lyon").order_by("id")
    # all()返回的是一个QuerySet对象,即封装了一行数据的所有属性的对象
    for var in result:
        print(var.id,var.username,var.password)
    print(response1)
    print(response2)
    return HttpResponse('查询成功!')
```

mysite/urls.py

```python
from myapp import views
urlpatterns = [
    url(r'^select_user/', views.select_user),
]
```

## 删除数据

myapp/views.py

```python
from myapp import models
def delete_user(request):
    models.Userinfo.objects.filter(username='Lyon').delete()
    models.Userinfo.objects.all().delete()
    return HttpResponse('删除成功!')
```

mysite/urls.py

```python
from myapp import views
urlpatterns = [
    url(r'^delete_user/', views.delete_user),
]
```

## 更新数据

myapp/views.py

```python
from myapp import models
def update_user(request):
    models.Userinfo.objects.filter(username='Lyon').update(username='Kenneth')
    models.Userinfo.objects.all().update(password='456789')
    return HttpResponse('更新成功!')
```

mysite/urls.py

```python
from myapp import views
urlpatterns = [
    url(r'^update_user/', views.update_user),
]
```

本章仅对Model进行简单的操作介绍

详细参考 : [Model instance reference](https://docs.djangoproject.com/en/1.11/ref/models/instances/)