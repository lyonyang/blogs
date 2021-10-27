# 快速开始

我们将创建一个简单的API , 允许管理员用户查看和编辑系统中的用户和组








<extoc></extoc>

## 创建项目

```shell
# 创建项目目录
mkdir tutorial
cd tutorial

# 创建虚拟环境
virtualenv env
source env/bin/activate  # Windows上使用`env\Scripts\activate`

# 安装Django和Django REST framework into the virtualenv
pip install django
pip install djangorestframework

# 创建Django项目和应用
django-admin.py startproject tutorial .  # Note the trailing '.' character
cd tutorial
django-admin.py startapp quickstart
cd ..
```

该项目目录如下 : 

```shell
$ pwd
<some path>/tutorial
$ find .
.
./manage.py
./tutorial
./tutorial/__init__.py
./tutorial/quickstart
./tutorial/quickstart/__init__.py
./tutorial/quickstart/admin.py
./tutorial/quickstart/apps.py
./tutorial/quickstart/migrations
./tutorial/quickstart/migrations/__init__.py
./tutorial/quickstart/models.py
./tutorial/quickstart/tests.py
./tutorial/quickstart/views.py
./tutorial/settings.py
./tutorial/urls.py
./tutorial/wsgi.py
```

同步数据库

```shell
python manage.py migrate
```

## 模型

我们使用Django默认的两个模型 , 用户` (User) `和组 ` (Group) ` , 你可以使用 `Admin` 来进行管理

创建两个超级用户

```shell
python manage.py createsuperuser --emaill Lyon@example.com --username Lyon
python manage.py createsuperuser --emaill Kenneth@example.com --username Kenneth
```

## 序列化器

我们需要定制一些序列化器来决定我们数据的表现形式

在 `quickstart` 应用下新建 `serializers.py` :

```python
from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """ 用户序列化器 """
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    """ 组序列化器 """
    class Meta:
        model = Group
        fields = ('url', 'name')
```

这里使用超链接模型序列化器 , 因为超链接是非常好的RESTful设计 , 当然你也可以使用其他的序列化器

## 视图

`tutorial/quickstart/views.py` 

```python
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from quickstart.serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    允许查看或编辑用户的API
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    允许查看或编辑组的API
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
```

## 路由

`tutorial/urls.py` 

```python
from django.conf.urls import url, include
from rest_framework import routers
from quickstart import views

# 因为使用的是viewsets,所以使用路由器进行注册
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    
    # rest_framework自带的url,login与logout:
    #   - url(r'^login/$', login, login_kwargs, name='login'),
    #   - url(r'^logout/$', logout, name='logout'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
```

## 配置

在 `tutorial/settings.py` 的 `INSTALLED_APPS` 中 , 添加 `rest_framework` 

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'quickstart',
    'rest_framework',  # 此处为添加项
]
```

## 测试API

首先我们运行我们的项目程序 , 随后使用浏览器访问项目服务器地址 , 或者使用命令行工具 , 如 : [httpie](https://github.com/jakubroztocil/httpie) 等

查看我们的API , `http://127.0.0.1:8000/` , 结果如下 : 


![Api Root – Django REST framework](http://oux34p43l.bkt.clouddn.com/Api%20Root%20–%20Django%20REST%20framework.png)

随后我们可以通过API来获取用户数据 , 访问 `http://127.0.0.1:8000/users/` , 结果如下 : 

![User List – Django REST framework](http://oux34p43l.bkt.clouddn.com/User%20List%20–%20Django%20REST%20framework.png)

到这里 , django-rest-framework的简单使用就结束了 , 后续内容请看下一篇