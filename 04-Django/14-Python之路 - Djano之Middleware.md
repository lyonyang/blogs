# Python之路 - Djano之Middleware

## 介绍

在Django中 , 中间件本质上就是一个类 , 我们可以使用中间件来对请求和响应进行批量处理 , 中间件所在的层次介于WSGI协议与Django URL系统之间 , 它类似一个一个的盒子 , 所有的请求和响应到来时 , 都必须穿过一个一个的盒子 (中间件) , 如下 :

```
请求   → →  中间件1   → →   中间件2   → ... →   响应
                                               ↓ ↓
请求   ← ←  中间件1   ← ←   中间件2   ← ... ←   响应
```

它是一个轻量级 , 底层的 "插件" 系统 , 用于在全局修改Django的输入或输出

每个中间件负责完成某个特定的功能 , 如下为默认Django激活的中间件如下 : 

```python
MIDDLEWARE = [
    # 安全保护中间件
    'django.middleware.security.SecurityMiddleware',
    # 会话中间件
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 通用中间件
    'django.middleware.common.CommonMiddleware',
    # 跨站请求伪造保护中间件
    'django.middleware.csrf.CsrfViewMiddleware',
    # 认证中间件
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 消息中间件
    'django.contrib.messages.middleware.MessageMiddleware',
    # 防止点击劫持中间件
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

我们可以看到`MIDDLEWARE`是一个列表 , 也就是说中间件是有顺序的 , 我们在使用中间件时需要注意中间件的排序 , 因为有的中间件可能需要依赖某一中间件 , 所以其应该放在依赖的中间件之后

对于请求和响应的少量或部分处理 , 我们可以使用装饰器来实现

中间件排序 : [Middleware ordering](https://docs.djangoproject.com/en/1.11/ref/middleware/#middleware-ordering)

内置中间件 :  [built-in middleware reference](https://docs.djangoproject.com/en/1.11/ref/middleware/)

## CSRF

CSRF 即`Cross Site Request Forgery protection` , 中文意思为跨站请求伪造 , 也被称为"One Click Attack"或者 Session Riding , 通常缩写为CSRF或XSRF , 是一种对网站的恶意利用

攻击通过在授权用户访问的页面中包含链接或者脚本的方式工作 , 例如 : 一个网站用户Bob可能正在浏览聊天论坛 , 而同时另一个用户Alice也在此论坛中 , 并且后者刚刚发布了一个具有Bob银行链接的图片消息 ; 设想一下 , Alice编写了一个在Bob的银行站点上进行取款的form提交的链接 , 并将此链接作为图片src ; 如果Bob的银行在cookie中保存他的授权信息 , 并且此cookie没有过期 , 那么当Bob的浏览器尝试装载图片时将提交这个取款form和他的cookie , 这样在没经Bob同意的情况下便授权了这次事务

所以为了防止CSRF的发生 , Django为我们提供了中间件`django.middleware.csrf.CsrfViewMiddleware` 

### CSRF中间件使用

如果要在我们的视图中使用CSRF保护 , 我们需要进行如下操作 :

1. CSRF中间件默认在`MIDDLEWARE`设置中被激活 , CSRF中间件应该在任何视图中间件之前 , 以确保CSRF攻击已被处理
2. 在任何使用POST的表单模板中 , 如果表单用于内部URL , 则需要使用`csrf_token`标记`form`标签 , 如下 : 

```html
<form action="" method="post">
    {% csrf_token %}
</form>
<!--
对于外部URL的POST表单不应该这样做,因为这会导致CSRF令牌被泄漏,从而导致漏洞
-->
```

3. 在相应的视图函数中 , 确保使用`RequestContext` 来渲染响应 , 以便`csrf_token`能够正常使用 , `render()`函数 , 或者contrib应用以及通用视图都是用`RequestContext` 

在Jinja2模板中用`csrf_input`代替了`csrf_token`

注意 : 如果传入的请求未能通过`CsrfViewMiddleware`执行的检查 , 则会向用户发送`403 Forbidden` 响应 ; 这也就是如果我们激活了`CsrfViewMiddleware` 中间件 , 而没添加`csrf_token` 时为什么会出现`403 Forbidden`错误

更多CSRF中间件使用参考 :  [Cross Site Request Forgery protection documentation](https://docs.djangoproject.com/en/1.11/ref/csrf/) 

## 激活中间件

我们如果要使用中间件 , 就需要在Django配置中的`MIDDLEWARE`添加中间件组件

默认时 , Django已经为我们配置好了一些内置的中间件 , 如果我们想要使用自定义的中间件 , 那么我们就需要在该配置中进行添加了 , 如下 : 

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'RbacMiddleware',    # 激活Rbac中间件
]
```

## 自定义中间件

有时候我们需要自定义中间件来达到我们的实际要求 , 其有两种方式 , 即通过类或者函数

通常我们使用类 , 如下 : 

```python
class SimpleMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
```

在我们自定义中间件时需要注意如下 : 

1. `__init__()` 必须接受`get_response`参数 , 旧版中`__init__()`不接受任何参数 , 所以为了兼容性 , 我们应该这样写`def __init__(self, get_response):`
2. 每个请求都会调用一次`__call__()`方法
3. 当Web服务器启动时 , `__init__()`仅会被调用一次

### MiddlewareMixin

上面的写法只适用于Django 1.9及之前的写法 , 在1.10的版本中 , Django为我们提供了`django.utils.deprecation.MiddlewareMixin`以简化`MIDDLEWARE`和旧的`MIDDLEWARE_CLASSES`兼容的中间件类 ; Django 1.10之后的版本使用`MIDDLEWARE`代替`MIDDLEWARE_CLASSES` , Django中包含的所有中间件类都兼容这两种设置

> class MiddlewareMixin

```python
# 自定义中间件类需要继承该类
class MiddlewareMixin(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response
'''
注意:
为了解决版本的兼容问题,
我们不应该由django.utils.deprecation中来导入MiddlewareMixin,
因为在之后的版本MiddlewareMixin将会被剔除
'''
```

如果与`MIDDLEWARE_CLASSES`一起使用 , 在不会使用`__call__()`方法 ; Django会直接调用`process_request()`和`process_response()`

在大多数情况下 , 继承这种混合将足以使旧式中间件与新系统兼容 , 具有足够的向后兼容性

### 钩子函数

在请求阶段中 , 调用视图之前 , Django会按照`MIDDLEWARE`中定义的顺序自顶向下应用中间件 , 我们需要用到以下两个钩子函数 : 

- process_request()
- process_view()

在响应阶段中 , 调用视图之后 , 中间件会按照相反的顺序应用 , 自底向上 , 我们需要用到以下三个钩子函数 : 

- process_exception() , 仅当视图抛出异常时使用
- process_template_response() , 仅用于模板响应
- process_response()

如下图 : 

![MIDDLEWARE](D:\桌面\MIDDLEWARE.png)

我们可以将这些中间件比作为一个洋葱 , 每个中间件类都是一个"洋葱层" 

如果请求通过洋葱的所有层 , 一直到核心的视图 , 随后响应会按照相反的顺序原路返回

如果其中某一层短路并返回响应 , 那么将不能到达视图 , 而是直接在短路层就返回响应

#### process_request()

```python
process_request(request):
    """
    request:是一个HttpRequest对象
    """
```

在Django决定执行哪个视图之前 , 将会先调用`process_request()`

`process_request()`应该返回一个None或者一个HttpResponse对象 , 返回说明如下 : 

- 如果返回None , Django会继续处理这个请求 , 执行其它中间件的`process_request()` , 然后执行中间件的`process_view()` , 最后执行对应的视图
- 如果返回一个HttpResponse对象 , Django就不会去调用其他的中间件的`request_view`或`request_exception`或对应的视图 , 而是直接转变到响应阶段 , 按照原路返回

#### process_view()

```python
process_view(request, view_func, view_args, view_kwargs):
    """
    request:一个HttpRequest对象,与我们在前面视图函数中的request一样
    view_func:是Django会调用的一个Python函数
    view_args:一个会传递到视图的位置参数列表
    view_kwargs:一个会传递到视图的关键字参数字典
    view_args和view_kwargs都不包含第一个视图函数request
    """
```

`process_view()`会在Django调用视图之前被调用 , 它返回一个None或一个HttpResponse对象 , 返回说明如下 : 

- 如果返回None , Django将会继续处理这个请求 , 执行其它的`process_view()`中间件然后调用对应的视图 
- 如果返回一个HttpResponse对象 , Django就不会去调用其它中间件的`process_view()`或`process_exception()`或对应的视图 , 它将转变至响应阶段 , 并返回结果

```note
Note

Accessing request.POST inside middleware before the view runs or in process_view() will prevent any view running after the middleware from being able to modify the upload handlers for the request, and should normally be avoided.

The CsrfViewMiddleware class can be considered an exception, as it provides the csrf_exempt() and csrf_protect() decorators which allow views to explicitly control at what point the CSRF validation should occur.
```

#### process_exception()

```python
process_exception(request, exception):
    """
    request:一个HttpRequest对象
    exception:是一个被视图中的方法抛出来的exception对象
    """
```

当一个视图抛出异常时 , Django会调用process_exception()来处理 ; `process_exception()`应该返回None或者HttpResponse对象 , 如果返回HttpResponse对象 , 则将应用模板响应和响应中间件 , 并将生成的响应返回给浏览器 , 否则Django会使用默认异常处理方式进行处理

注意 : 在处理响应期间 , 中间件的执行顺序是倒序执行的 , 所以如果异常中间件返回响应 ,  那么下一层中间件的`process_exception`方法将不会调用 , 因为在上一层已经捕捉完成

#### process_template_response()

```python
process_template_response(request, response):
    """
    request:是一个HttpRequest对象
    response:是一个TemplateResponse对象(或等价的对象),
    		 由Django视图或者中间件返回
    """
```

这个方法必须返回一个实现了render方法的响应对象 , 它可以修改给定的response对象 , 通过修改`response.tmplate_name`和`response.context_data`或者它可以创建一个全新的`TemplateResponse`对象(或等价的对象) 

并且一旦所有的模板响应中间件被调用 , 响应会自动被渲染

#### process_response()

```python
process_response(request,response):
    """
    request:一个HttpRequest对象
    response:Django视图或者中间件返回的HttpResponse或者StreamingHttpResponse对象
    """
```

`process_response()`在所有响应返回浏览器之前被调用

这个方法必须返回HttpResponse或者StreamingHttpResponse对象 , 它可以改变已有的response , 或者创建并返回新的HttpResponse或StreamingHttpResponse对象

`process_response`不像`process_request`和`process_view`那样会因为前一个中间件返回的HttpResponse而被跳过 , `process_response`方法总是会被调用 , 这意味着你的`process_response`方法不能依赖于`process_request`方法中的设置

## 处理流响应

不像`HttpResponse` , `StreamingHttpResponse`并没有`content`属性 , 所以 , 中间件再也不能假设所有响应都带有`content`属性 , 如果它们需要访问内容 , 他们必须测试是否为流式响应 , 并相应地调整自己的行为 , 如下 : 

```python
if response.streaming:
    response.streaming_content = wrap_streaming_content(response.streaming_content)
else:
    response.content = alter_content(response.content)
```

注意 : 

我们需要假设`streaming_content`可能会大到在内存中无法容纳 , 响应中间件可能会把它封装在新的生成器中 , 但是一定不要销毁它 , 封装一般如下 : 

```python
def wrap_streaming_content(content):
    for chunk in content:
        yield alter_content(chunk)
```

## RBAC案例

rbac即Role-Based Access Control , 基于角色的权限访问控制 , 这种控制极大地简化了权限的管理 , 下面为rbac中我们自定义使用的中间件案例 : 

```python
import re
from django.shortcuts import redirect,HttpResponse
from django.conf import settings

class MiddlewareMixin(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response

# 继承MiddlewareMixin类
class RbacMiddleware(MiddlewareMixin):

    def process_request(self,request):
        # 获取当前请求的URL
        current_url = request.path_info

        # 当前请求不需要执行权限验证
        for url in settings.VALID_URL:
            if re.match(url,current_url):
                return None
        # 获取Session中保存当前用户的权限
        permission_list = request.session.get("permission_url_list")
        if not permission_list:
            return redirect('/login/')

        # 判断是否具有权限并设置标志位
        flag = False
        for db_url in permission_list:
            regax = "^{0}$".format(db_url)
            if re.match(regax, current_url):
                flag = True
                break
        # 最后如果具有权限那么继续走向下一个中间件或者视图
        # 否则,返回响应
        if not flag:
            return HttpResponse('无权访问')
'''
注意:
对于钩子函数是否定义在于我们自己,但是要注意中间件的工作原理,
比如在这里我们没有定义process_response方法,
但是在MiddlewareMixin类的__call__方法中,
使用了get_response方法
'''
```

更多中间件相关 : [middleware usage guide](https://docs.djangoproject.com/en/1.11/topics/http/middleware/) 