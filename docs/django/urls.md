# Django - Urls








<extoc></extoc>

## 介绍

如`settings.py` 一样 , `django-admin startproject` 或者`python manage.py startproject` 执行创建时 , 会为我们自动创建其一个名为**URLconf** (URL配置) 的Python模块 , 即`urls.py` 通常把它称为路由系统

`url.py` 是纯Python代码 , 是一个简单的Python模式 (简单的正则表达式) 到Python函数 (你的视图) 之间的映射

如默认下已经有了admin这一条

```python
from django.conf.urls import url

urlpatterns = [
    # 由正则表达是到urls视图函数之间的一个映射
    url(r'^admin/', admin.site.urls),
]
'''
urlpatterns是一个列表
列表中是一个个url()实例
'''
```

url参数介绍

```python
def url(regex, view, kwargs=None, name=None):
"""
regex:一个正则表达式字符串
view:一个可调用对象,通常为一个视图函数或一个指定视图函数路径的字符串
kwargs:可选的要传给视图函数的默认参数,字典形式
name:可选参数name,具体可以查看源码
"""
```

## 请求处理

**Django如何处理一个请求**

当用户从Django支持的站点请求页面时 , 系统会遵循以下的算法来确定要执行的Python代码 : 

1. Django决定是否使用*ROOT_URLCONF*配置 ; 如果传入`HttpRequest`对象具有一个`urlconf`属性(由中间件设置) , 则将使用其值代替*ROOT_URLCONF*设置
2. Django加载Python模块并查找变量`urlpatterns` , 即urls.py中的`django.conf.urls.url()`实例列表
3. Django按顺序遍历每个URL模式 , 并停在与请求的URL匹配的第一个URL模式 , 这意味着找到一个后就不会继续往下找了 , 也就会出现覆盖现象(前面的pattern覆盖后面的pattern)
4. 一旦一个正则表达式匹配 , Django就会导入并调用给定的视图 (视图函数) , 该函数参数如下 : 
   - 一个HttpRequest实例
   - 如果匹配的正则表达式没有返回任何命名组 , 则将正则表达式的匹配作为位置参数提供
   - 关键字参数由任何与正则表达式匹配的命名组组成 , 在可选的kwargs参数中指定的任何参数覆盖到`django.url.urls.url()` 
5. 如果没有正则表达式匹配 , 或者在这个过程中的任何一点引发异常 , Django就会调用一个合适的错误处理视图进行处理

## 基本示例

```python
# 导入url函数
from django.conf.urls import url
# 导入视图模块
from . import views
# url()实例列表
urlpatterns = [
    # r表示Python原生字符串
    url(r'^articles/2003/$', views.special_case_2003),
    url(r'^articles/([0-9]{4})/$', views.year_archive),
    url(r'^articles/([0-9]{4})/([0-9]{2})/$', views.month_archive),
    url(r'^articles/([0-9]{4})/([0-9]{2})/([0-9]+)/$', views.article_detail),
]
```

**说明** 

1. 请求`/articles/2005/03/`匹配列表中的第三个条目 , Django会调用函数`views.month_archive(request, '2005', '03')` 
2. `/articles/2005/3/` 不匹配任何URL模式 , 因为列表中的第三个条目需要两位数的月份
3. `/articles/2003/`将匹配列表中的第一个模式 , 而不是第二个模式 , 因为模式是按顺序测试的 , 而第一个模式是第一个要传递的测试 ; 你可以随意地使用这种排序来插入一些特殊的例子 , 在这里 , Django将调用函数`views.special_case_2003(request)` 
4. `/articles/2003` 将不匹配任何这些模式 , 因为每个模式都要求URL以斜杠 "/" 结尾
5. `/articles/2003/03/03/`将匹配最终模式 , Django会调用函数`views.article_detail(request, '2003', '03', '03')` 

**注意 : 捕获的值是作为位置参数**

## 分组命名

```python
# 导入url函数
from django.conf.urls import url
# 导入视图函数
from . import views
# url()实例列表
urlpatterns = [
    url(r'^articles/2003/$', views.special_case_2003),
    url(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive),
    url(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.month_archive),
    url(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', views.article_detail),
]
```

**说明**

1. 请求`/articles/2005/03/`将调用函数`views.month_archive(request, year='2005',month='03') ` 而不是 `views.month_archive(request, '2005', '03')` 
2. 请求`/articles/2003/03/03/`调用函数 `views.article_detail(request, year='2003', month='03',day='03')` 

**注意 : 捕获的值将作为关键字参数传递 , 而不是位置参数**

**匹配/分组算法**

1. 如果有命名参数 , 则使用命名参数 , 忽略非命名参数
2. 否则 , 它将传递所有非命名参数作为位置参数

## 额外参数

`django.conf.urls.url()` 函数可以接收一个可选的第三个参数 (kwargs) , 它应该是一个额外的关键字参数的字典 , 如下 : 

```python
from django.conf.urls import url
from . import views
urlpatterns = [
    # 传递额外的参数foo
    url(r'^blog/(?P<year>[0-9]{4})/$', views.year_archive, {'foo': 'bar'}),
]
```

在上述例子中 , 对于请求`/blog/2005/`  , Django将调用函数`views.year_archive(request, year='2005', foo='bar')` 

**处理冲突 :** 可能有一个URL模式捕获命名的关键字参数 , 并且还在其额外参数的字典中传递具有相同名称的参数 , 发生这种情况时 , 将使用字典中的参数 , 而不是在URL中捕获的参数

## 反向解析

`django.conf.urls.url()` 函数中的第四个可选参数`name` , 我们可以利用该参数进行反向解析 , 相当于为我们配置的第一个参数 (regex) 取一个别名

实例

```python
from django.conf.urls import url
from . import views
urlpatterns = [
    # 为home取别名为h1
    url(r'^home', views.home, name='h1'),
    # 为index取别名为h2
	url(r'^index/(\d*)', views.index, name='h2'),
]
```

设置名称之后 , 可以在不同的地方进行反向解析 , 如 : 

- 模板中使用生成URL

```html
<!-- 反向解析为action=index/2012 -->
<form action="{% url 'h2' 2012 %}">
    <p>用户:<input type="text" name="user"></p>
    <p>密码:<input type="password" name="pwd"></p>
    <p><input type="submit" value="提交"></p>
</form>
```

- 函数中使用生成URL , `django.urls.reverse('h2', args=(2012,))` 

- model中使用获取URL , 自定义`get_absoulte_url()` 方法

```python
class NewType(models.Model):
    caption = models.CharField(max_length=16)
    def get_absolute_url(self):
        """
        为每个对象生成一个URL应用,
        在对象列表中生成查看详细的URL,使用此方法即可
        """
        # return '/%s/%s' % (self._meta.db_table, self.id)
        # 或
        from django.urls import reverse
        return reverse('NewType.Detail', kwargs={'nid': self.id})
```

## 路由分发

如果所有应用的url都放在`urls.py` 这一个文件中 , 这无疑会对我们管理url造成麻烦 , Django中提供了一个`django.conf.urls.include()` 函数 , 可以为我们提供一个url之间的映射 , 我们把这叫做路由分发 , 如下 :

**myapp/urls.py**

```python
# 导入url函数
from django.conf.urls import url  
# 从应用视图导入homepage函数
from myapp.views import homePage  
urlpatterns = [  
    url(r'homepage', homePage),  
]  
```

**mydjango/urls.py**

```python
# 导入url函数
from django.conf.urls import url
# 导入include函数
from django.conf.urls import include
# 导入admin函数
from django.contrib import admin  
urlpatterns = [  
    url(r'^admin/', admin.site.urls),  
    # 引用myapp下的urls.py
    url(r'^myapp/', include("myapp.urls"))
]  
```

## 命名空间

**mydjango.urls.py**

```python
from django.conf.urls import url,include
 
urlpatterns = [
    url(r'^a/', include('app01.urls', namespace='author-polls')),
    url(r'^b/', include('app01.urls', namespace='publisher-polls')),
]
```

**app01.urls.py**

```python
from django.conf.urls import url
from app01 import views

app_name = 'app01'
urlpatterns = [
    url(r'^(?P<pk>\d+)/$', views.detail, name='detail')
]
```

**app01.views.py**

```python
def detail(request, pk):
    print(request.resolver_match)
    return HttpResponse(pk)
```

以上定义带命名空间的url之后 , 使用name参数生成URL时 , 应该如下 : 

- `v = reverse('app01:detail', kwargs={'pk':11})` 

```html
    {% url 'app01:detail' pk=12 pp=99 %}
```

Django中的路由系统和其他语言的框架有所不同 , 在Django中每一个请求的url都要有一条路由映射 ; 其他大部分的Web框架则是对一类的url请求做一条路由映射 , 从而使路由系统变得简洁

更多URL调度相关 : https://docs.djangoproject.com/en/1.11/topics/http/urls/