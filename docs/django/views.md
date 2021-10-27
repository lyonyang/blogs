# Django - Views








<extoc></extoc>

## 介绍

在前面的文章中已经整理了关于*URLconf* 的相关内容 , 我们知道`url()` 的第二个位置参数是一个视图函数 , 简称视图 , 视图函数其实就是一个简单的Python函数 , 它的作用就是接收Web请求并且返回Web响应

*URLconf* 就像是Django所支撑网站的目录 , 它的本质是URL模式以及要为该URL模式调用的视图函数之间的映射表 , 也就是每一个URL都有相对应的视图进行处理

在Django中当我们创建一个应用时 , 也就是执行命令`python manage.py startapp app_name`  , Django会自动创建一个`views.py` 文件 , 用来存放我们的视图函数

Django对于`views.py` 的文件命名没有特别的要求 , 不在乎这个文件叫什么 , 但是根据约定 , 把它命名成`views.py` 是个好主意 , 这样有利于其他开发者读懂你的代码

## 一个简单视图

我们编写一个简单的视图 , Hello视图

blog\views.py

```python
from django.http import HttpResponse
def hello(request):
    # 视图中必须实现响应
    return HttpResponse("Hello Lyon")
```

mysite\urls.py

```python
from blog import views
urlpatterns = [
    url(r'^hello/', views.hello),
]
```

编写完成后我们就可以通过浏览器进行访问了 , 访问`http://127.0.0.1:8000/hello/` 获取结果

这样我们就完成了一个非常简单的视图 , 接下来分析一下上面的代码 : 

1. 每个视图至少要有一个参数 , 通常被叫做`request` , 这是一个触发这个视图 , 包含当前Web请求信息的对象 , 是`django.http.HttpRequest` 的一个实例
2. 这个视图会返回一个`HttpResponse` 对象 , 其中包含生成的响应 . 每个视图函数都负责返回一个`HttpResponse`对象
3. 在`urls.py` 中我们需要导入视图模块 , 并配置好URL模式


注意 : 当访问`URL/hello/` 时 , Django根据settings.py中的`ROOT_URLCONF` 的设置装载URLconf , 然后按顺序逐个匹配URLconf里的URLpatterns , 直到找到一个匹配的


## HttpRequest

Django使用请求和响应对象来通过系统传递状态

当请求页面时 , Django创建一个`HttpRequest` 包含关于请求的元数据的对象 , 然后Django加载响应的视图 , 将`HttpRequest` 作为视图函数的第一个参数传递 , 而视图则负责返回一个`HttpResponse` 对象 , 这点在上节中已经有说明 

`HttpRequest`对象的属性如果没有特别说明 , 都被认为是只读的 , 下面对`HttpRequest`对象的属性进行说明

### HttpRequest属性

*class* HttpRequest [[source]](https://docs.djangoproject.com/en/1.11/_modules/django/http/request/#HttpRequest)

| 属性                           | 说明                                       |
| ---------------------------- | ---------------------------------------- |
| `HttpRequest.scheme`         | 表示请求方案的字符串(通常为http或https)                |
| `HttpRequest.body`           | 原始Http请求的字节字符串 ,  这对于处理数据的方式与传统的HTML表单很有用 ; 对于处理传统表单数据 , 请使用`HttpRequest.POST`  ; 可以利用`HttpRequest.read()` 进行查看 |
| `HttpRequest.path`           | 表示请求页面的完整路径的字符串 , 不包括scheme和 domain      |
| `HttpRequest.path_info`      | 在某些Web服务器配置下 , 主机名后的URL部分被分成脚本前缀部分和路径信息部分 , 该`path_info`属性始终包含路径的路径信息部分 , 无论使用何种Web服务器 |
| `HttpRequest.method`         | 表示请求中使用的HTTP方法的字符串 , 必须为大写 , 即(`'GET'`或`'POST'`) |
| `HttpRequest.encoding`       | 表示当前编码                                   |
| `HttpRequest.content_type`   | 表示请求的MIME类型的字符串 , 从`CONTENT_TYPE`头部解析    |
| `HttpRequest.content_params` | 包含在`CONTENT_TYPE`头部的键/值参数的字典             |
| `HttpRequest.GET`            | 一个包含所有给定的HTTP GET 参数的字典对象 , 详情阅读 [QueryDict](https://docs.djangoproject.com/en/1.11/ref/request-response/#django.http.QueryDict) |
| `HttpRequest.POST`           | 一个包含所有给定HTTP POST参数的字典对象 , 前提是请求包含表单数据 , 详情阅读 [QueryDict](https://docs.djangoproject.com/en/1.11/ref/request-response/#django.http.QueryDict) |
| `HttpRequest.COOKIES`        | 包含所有cookies的标准Python字典对象 ; keys和values都是字符串 |
| `HttpRequest.FILES`          | 包含所有上传文件的类字典对象 , FILES中的每一个Key都是< input type="file" name="" / >标签中name属性的值 , FILES中的每一个value同时也是一个标准的Python字典对象 , 包含下面三个Keys : filename , 上传文件名，用字符串表示<br /> content_type , 上传文件的Content Type<br />content , 上传文件的原始内容 |
| `HttpRequest.META`           | 包含所有可用HTTP标头的字典                          |
| `HttpRequest.resolver_match` | 一个ResolverMatch的实例 , 它表示已解析的URL<br /> 这个属性只在URL解析发生之后才被设置 , 这意味着它在所有的视图中都可用 , 但在解析发生之前执行的中间件中是不可用的 |

### 应用程序设置的属性

Django本身没有设置这些属性 , 但是如果你的应用程序设置了这些属性 , 就可以使用它们

| 属性                        | 说明                                       |
| ------------------------- | ---------------------------------------- |
| `HttpRequest.current_app` | url模板标签将使用它的值作为`reverse()` 的`current_app`参数 |
| `HttpRequest.urlconf`     | 这将用作当前请求的根URLconf , 会覆盖`ROOT_URLCONF`设置<br /> `urlconf`可以设置为`None`恢复以前中间件所做的任何更改并返回到使用`ROOT_URLCONF` |

### 中间件设置的属性

包含在Django的contrib应用程序中的一些中间件在请求中设置了属性 , 如果在请求中看不到该属性，请确保列出了相应的中间件类[`MIDDLEWARE`](https://docs.djangoproject.com/en/1.11/ref/settings/#std:setting-MIDDLEWARE)

| 属性                    | 说明                                       |
| --------------------- | ---------------------------------------- |
| `HttpRequest.session` | 来自  [SessionMiddleware](https://docs.djangoproject.com/en/1.11/ref/middleware/#django.contrib.sessions.middleware.SessionMiddleware) :  唯一可读写的属性 , 代表当前会话的字典对象 ; 只有激活Django中的session支持时该属性才可用 |
| `HttpRequest.site`    | 来自[CurrentSiteMiddleware](https://docs.djangoproject.com/en/1.11/ref/middleware/#django.contrib.sites.middleware.CurrentSiteMiddleware) : 代表当前网站的实例[`Site`](https://docs.djangoproject.com/en/1.11/ref/contrib/sites/#django.contrib.sites.models.Site)或 [`RequestSite`](https://docs.djangoproject.com/en/1.11/ref/contrib/sites/#django.contrib.sites.requests.RequestSite)通过 [`get_current_site()`](https://docs.djangoproject.com/en/1.11/ref/contrib/sites/#django.contrib.sites.shortcuts.get_current_site) 获取 |
| `HttpRequest.user`    | 来自[AuthenticationMiddleware](https://docs.djangoproject.com/en/1.11/ref/middleware/#django.contrib.auth.middleware.AuthenticationMiddleware) : [AUTH_USER_MODEL](https://docs.djangoproject.com/en/1.11/ref/settings/#std:setting-AUTH_USER_MODEL)代表当前登录用户的一个实例。如果用户当前没有登录，`user `将被设置为一个[AnonymousUser](https://docs.djangoproject.com/en/1.11/ref/contrib/auth/#django.contrib.auth.models.AnonymousUser) 实例 , 可以用 [is_authenticated](https://docs.djangoproject.com/en/1.11/ref/contrib/auth/#django.contrib.auth.models.User.is_authenticated) 进行区分 |

HttpRequest对象的方法点这里 : [Methods](https://docs.djangoproject.com/en/1.11/ref/request-response/#methods)

常用 `get_full_path()`  , 返回path , 加上一个附加的查询字符串(如果使用)

```python
"/music/bands/the_beatles/?print=true"
```

## HttpResponse

`HttpRequest`对象是由Django自动创建的 , 而`HttpResponse` 对象是由我们自己来创建的 , 我们写的视图负责实例化 , 填充和返回一个`HttpResponse` 对象

这个`HttpResponse` 类定义在 ` django.http`模块中

### 用法

**传递字符串**

典型的用法是将页面内容作为字符串传递给HttpResponse构造函数

```python
>>> from django.http import HttpResponse
>>> response = HttpResponse("Here's the text of the Web page.")
>>> response = HttpResponse("Text only, please.", content_type="text/plain")
```

如果想增加内容 , 可以将其当做类似文件对象使用

```python
>>> response = HttpResponse()
>>> response.write("<p>Here's the text of the Web page.</p>")
>>> response.write("<p>Here's another paragraph.</p>")
```

**传递迭代器**

除了传递字符串 , 还可以传递一个迭代器对象 ; 它会立即使用迭代器 , 将其内容存储为字符串 , 然后丢弃

如果需要将响应以迭代器对象传输到客户端 , 则必须使用[StreamingHttpResponse](https://docs.djangoproject.com/en/1.11/ref/request-response/#django.http.StreamingHttpResponse) 类

**设置标题栏**

要设置或删除响应中的标题字段 , 可以将其视为字典

```python
>>> response = HttpResponse()
>>> response['Age'] = 120
>>> del response['Age']
```

注意 : 如果标题字段不存在 , `del` 不会引发KeyError , 这一点与字典不同

**告诉浏览器对待响应作为文件附件**

要告诉浏览器将响应当做文件附件处理 , 可以使用`content_type` 参数并设置`Content-Disposition` 标题

返回一个Excel电子表格

```python
>>> response = HttpResponse(my_data, content_type='application/vnd.ms-excel')
>>> response['Content-Disposition'] = 'attachment; filename="foo.xls"'
```

### 属性

HttpResponse属性

| 属性                           | 说明                                       |
| ---------------------------- | ---------------------------------------- |
| `HttpResponse.content`       | 表示内容的字符串                                 |
| `HttpResponse.charset`       | 表示响应将被编码的字符串的字符串 ,  如果在`HttpResponse`实例化的时候没有给出 , 则会从中提取 `content_type` , 如果不成功 , DEFAULT_CHARSET将使用该 设置 |
| `HttpResponse.status_code`   | 该响应的 [HTTP状态码](https://tools.ietf.org/html/rfc7231.html#section-6) ,  除非reason_phrase明确设置 , 否则修改 `status_code`构造函数外部的值也会修改值 `reason_phrase` |
| `HttpResponse.reason_phrase` | 响应的HTTP原因短语 , 它使用的[HTTP标准的](https://tools.ietf.org/html/rfc7231.html#section-6.1)默认原因短语。 除非明确规定 , `reason_phrase`由价值决定`status_code` |
| `HttpResponse.streaming`     | 此属性存在使中间件可以以不同于常规响应的方式处理流响应 , 一直为False   |
| `HttpResponse.closed`        | 如果响应已经结束则为True                           |

HttpResponse对象方法可见 : [Method](https://docs.djangoproject.com/en/1.11/ref/request-response/#id3)

### HttpResponse子类

Django包含许多HttpResponse处理不同类型HTTP响应的子类 , 这些子类都在`django.http` 中 , 子类如下 : 

- *class* HttpResponseRedirect  [[source\]](https://docs.djangoproject.com/en/1.11/_modules/django/http/response/#HttpResponseRedirect)


- *class* HttpResponsePermanentRedirect  [[source\]](https://docs.djangoproject.com/en/1.11/_modules/django/http/response/#HttpResponsePermanentRedirect)


- *class* HttpResponseNotModified  [[source\]](https://docs.djangoproject.com/en/1.11/_modules/django/http/response/#HttpResponseNotModified)
- *class* HttpResponseBadRequest  [[source\]](https://docs.djangoproject.com/en/1.11/_modules/django/http/response/#HttpResponseBadRequest)
- *class* HttpResponseNotFound  [[source\]](https://docs.djangoproject.com/en/1.11/_modules/django/http/response/#HttpResponseNotFound)
- *class* HttpResponseForbidden  [[source\]](https://docs.djangoproject.com/en/1.11/_modules/django/http/response/#HttpResponseForbidden)
- *class* HttpResponseNotAllowed  [[source\]](https://docs.djangoproject.com/en/1.11/_modules/django/http/response/#HttpResponseNotAllowed)
- *class* HttpResponseGone  [[source\]](https://docs.djangoproject.com/en/1.11/_modules/django/http/response/#HttpResponseGone)
- *class* HttpResponseServerError  [[source\]](https://docs.djangoproject.com/en/1.11/_modules/django/http/response/#HttpResponseServerError)

更多子类相关 : [HttpResponse相关](https://docs.djangoproject.com/en/1.11/ref/request-response/)

https://docs.djangoproject.com/en/1.11/_modules/django/http/response/

## render

为了方便 , Django中有一个shortcuts模块 , 其中收集了跨越多个级别的MVC的帮助函数和类

这里介绍一下其中的`render()`和`redirect()`  :

- render , 对html进行渲染
- redirect , 从当前页面进行跳转

```python
def render(request, template_name, context=None, content_type=None, status=None, using=None):
    """
    Returns a HttpResponse whose content is filled with the result of calling
    django.template.loader.render_to_string() with the passed arguments.
    """
    content = loader.render_to_string(template_name, context, request, using=using)
    return HttpResponse(content, content_type, status)
```

必要参数 :

- request : 用于生成此响应的请求对象
- template_name : 要使用的模板的全名或模板名称的序列 , 如果给出了一个序列 , 将使用存在的第一个模板

可选参数 : 

- context : 要添加到模板上下文的值的字典
- content_type : 用于生成文档的MIME类型 , 默认为`DEFAULT_CONTENT_TYPE`设置的值
- status : 响应的状态码 , 默认为200
- using : `settings.py`中NAME配置的模板引擎使用加载的模板

实例 

```python
from django.shortcuts import render
def my_view(request):
    # View code here...
    return render(request, 'myapp/index.html', {'foo': 'bar',}, content_type='application/xhtml+xml')
```

上述实例相当于

```python
from django.http import HttpResponse
from django.template import loader
def my_view(request):
    # View code here...
    t = loader.get_template('myapp/index.html')
    c = {'foo': 'bar'}
    return HttpResponse(t.render(c, request), content_type='application/xhtml+xml')
```

## redirect

```python
def redirect(to, *args, **kwargs):
    """
    Returns an HttpResponseRedirect to the appropriate URL for the arguments
    passed.
    The arguments could be:
        * A model: the model's `get_absolute_url()` function will be called.
        * A view name, possibly with arguments: `urls.reverse()` will be used
          to reverse-resolve the name.
        * A URL, which will be used as-is for the redirect location.
    By default issues a temporary redirect; pass permanent=True to issue a
    permanent redirect
    """
    if kwargs.pop('permanent', False):
        redirect_class = HttpResponsePermanentRedirect
    else:
        redirect_class = HttpResponseRedirect
    return redirect_class(resolve_url(to, *args, **kwargs))
```

默认返回一个临时的重定向 ; 传递`permanent=True` 可以返回一个永久的重定向

参数 : 

- A model: the model’s [`get_absolute_url()`](https://docs.djangoproject.com/en/1.11/ref/models/instances/#django.db.models.Model.get_absolute_url) function will be called.
- A view name, possibly with arguments: [`reverse()`](https://docs.djangoproject.com/en/1.11/ref/urlresolvers/#django.urls.reverse) will be used to reverse-resolve the name.
- An absolute or relative URL, which will be used as-is for the redirect location.

实例

1. 通过传递一些对象 , 该对象的`get_absolute_url()` 方法将被调用来找出重定向URL

```python
from django.shortcuts import redirect

def my_view(request):
    ...
    object = MyModel.objects.get(...)
    return redirect(object)
```

2. 通过传递一个视图的名称和可选的一些参数 , 该URL将通过reverse()` 方法反向解析

```python
def my_view(request):
    ...
    return redirect('some-view-name', foo='bar')
```

3. 通过传递一个硬编码的URL进行重定向

```python
def my_view(request):
    ...
    return redirect('/some/url/')
```

   也适用于完整的网址

```python
def my_view(request):
    ...
    return redirect('https://example.com/')
```

默认情况下，`redirect()返回一个临时重定向` , 所有上述形式都接受`permanent`参数 ; 如果设置为`True`永久重定向将被返回

```python
def my_view(request):
    ...
    object = MyModel.objects.get(...)
    return redirect(object, permanent=True)
```

更多shortcuts内容 : [Django shortcut functions](https://docs.djangoproject.com/en/1.11/topics/http/shortcuts/)

The Django Book : http://docs.30c.org/djangobook2/index.html