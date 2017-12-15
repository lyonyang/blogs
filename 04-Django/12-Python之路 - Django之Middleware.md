# Python之路 - Django之Middleware
<!-- TOC -->

- [Python之路 - Django之Middleware](#python之路---django之middleware)
    - [Introduce  🍀](#introduce--🍀)
    - [Writing your own middleware  🍀](#writing-your-own-middleware--🍀)
    - [Activating middleware  🍀](#activating-middleware--🍀)
    - [Middleware order and layering  🍀](#middleware-order-and-layering--🍀)
    - [Other middleware hooks  🍀](#other-middleware-hooks--🍀)
        - [process_view()  🍀](#process_view--🍀)
        - [process_exception()  🍀](#process_exception--🍀)
        - [process_template_response()  🍀](#process_template_response--🍀)
    - [Dealing with streaming responses  🍀](#dealing-with-streaming-responses--🍀)
    - [Exception handling  🍀](#exception-handling--🍀)

<!-- /TOC -->
## Introduce  🍀

在Django中 , 中间件其实就是一个类 , 他们可以介入Django的请求和响应处理过程 , 如下 : 

```python
请求   → →  中间件   → →   响应
    	 	 		       ↓
请求   ← ←  中间件   ← ←   响应
```

Django会根据自己的规则在合适的时机执行中间件中相应的方法

它是一个轻量级 , 底层的"插件"系统 , 用于在全局修改Django的输入或输出

每个中间件组件负责完成某个特定的功能 , 例如 , Django包含的一个中间件组件`AuthenticationMiddleware` , 它使用会话将用户和请求关联起来

## Writing your own middleware  🍀

一个中间件工程是一个可调用的 , 它采用一个`get_response` 可调用并返回一个中间件 , 中间件是一个可调用的函数 , 它接受请求并返回响应 , 就像视图一样

中间件可以写成一个如下所示的功能 : 

```python
def simple_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware
```

或者它可以写成一个类(通常使用方式) , 其实例是可调用的 , 如下 : 

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

Django提供的`get_response` 方法可以是实际的视图 (如果这是最后列出的中间件) , 或者它可能是链中的下一个中间件 ; 当前的中间件不需要知道或者关心它究竟是什么 , 只是它代表了接下来的任何事情

`get_response()`方法不会是实际的视图 , 而是来自处理程序的包装器方法 , 它负责应用视图中间件 , 用适当的URL参数调用视图 , 并应用模板响应和异常的中间件

中间件可以在Python任意路径下存放 , 但是要住在将路径需要加在`settings.py` 的`MIDDLEWARE` 配置中

**_\_init\_\_(get_response)**

中间件工厂必须接收`get_response` 参数 , 你也可以初始化中间件的全局状态 , 需要注意如下事项 : 

- Django只使用`get_response` 参数初始化你的中间件
- 与每个请求一次调用`__call__()` 方法不同 , 当Web服务器启动时 , `__init__()` 仅被调用一次

```
在Django1.10中的改变:
在旧版本中,Web服务器响应其第一个请求之前,才调用__init__()
在旧版本中,__init__()不接受任何参数,所以为了你的中间件能够向下兼容,请使用get_response可选参数(get_response=None)
```

**标记中间件为未使用**

在启动时确定是否该使用中间件是有用的 , 在这些情况下 , 你的中间件的`__init__()` 方法可能会引发`MiddlewareNotUsed` 

当DEBUG配置改为True时 , Django将从进程中删除该中间件, 并将调试信息记录到 [django.request](https://docs.djangoproject.com/en/1.11/topics/logging/#django-request-logger) 记录器中

## Activating middleware  🍀

上一步我们仅仅是定义中间件 , 其还无法使用 , 我们需要激活中间件 , 即将其加到Django

的`settings`中的`MIDDLEWARE` 列表中

在`MIDDLEWARE` 中 , 每个中间件组件由一个字符串表示 : 完整的Python路径到中间件工厂的类或函数名称 , 例如 , 我们使用`django-admin startproject` 命令创建工程的时候生成的默认列表如下 : 

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

Django安装不需要任何中间件 , 即MIDDLEWARE可以是空的 , 但是强烈建议使用`CommonMiddleware` 

`MIDDLEWARE` 中的顺序很重要 , 因为中间件可以依赖于其他中间件 , 例如[`AuthenticationMiddleware`](https://docs.djangoproject.com/en/1.11/ref/middleware/#django.contrib.auth.middleware.AuthenticationMiddleware) 在会话中存储经过身份验证的用户 , 所以它必须在[`SessionMiddleware`](https://docs.djangoproject.com/en/1.11/ref/middleware/#django.contrib.sessions.middleware.SessionMiddleware) 之后运行

对于中间件的排序问题 , 可见 :  [Middleware ordering](https://docs.djangoproject.com/en/1.11/ref/middleware/#middleware-ordering) 

## Middleware order and layering  🍀

在请求阶段 , 在调用视图之前 , Django以`MIDDLEWARE` (自上而下) 定义的顺序应用中间件

我们可以把中间比作一个洋葱 : 

每个中间件类都是"洋葱"的一层 , 而在"洋葱"的核心有视图 , 如果请求通过"洋葱"的所有层 (每个调用`get_response` 将请求传递到下一层) , 一直到核心的视图 , 响应则将通过在每一层 (以相反的顺序) 的路上退出

如果其中一个层决定段落并返回响应而不掉用其`get_response` , 那么该层(包括视图)内的"洋葱"层都不会看到请求或响应 ; 响应将只返回通过请求传递的相同的层

总之 , 在请求穿过中间件的过程中不能返回响应 , 否则就会短路了 , 即从当前层以反方向返回

## Other middleware hooks  🍀

除了前面描述的基本请求/响应中间件模型 , 我们还可以向基于类的中间件添加三种其他特殊方法 : 

### process_view()  🍀

```python
process_view(request, view_func, view_args, view_kwargs):
    """
    process_view()会在Django调用视图之前被调用,它返回一个None或一个HttpResponse对象
    request:一个HttpRequest对象,与我们在前面视图函数中的request一样
    view_func:是Django会调用的一个Python函数
    view_args:一个会传递到视图的位置参数列表
    view_kwargs:一个会传递到视图的关键字参数字典
    view_args和view_kwargs都不包含第一个视图函数request
    """
```

如果`process_view()` 返回一个None , Django将会继续处理这个请求 , 执行其它的`process_view()` , 然后调用对应的视图 ; 如果它返回一个HttpResponse对象 , Django不会打扰调用相应的视图 , 它将应用响应中间件到HttpResponse并返回

注意 : 

- 访问请求 , 在视图运行之前或者在`process_view()`中 , 在中间件发布后 , 将阻止任何在中间件之后运行的视图能修改请求的上传处理程序 , 并且通常应该避免这种情况
- 类CsrfViewMiddleware可以被认为是个例外 , 因为它提供`csrf_exempt()` 和`csrf_protect()` 两个装饰器 , 允许视图显示控制在哪个点需要开启CSRF验证

### process_exception()  🍀

```python
process_exception(request, exception):
    """
    当一个视图抛出异常时,Django会调用process_exception()来处理
    request:一个HttpRequest对象
    exception:是一个被视图中的方法抛出来的exception对象
    """
```

`process_exception` 返回None或者一个HttpResponse对象 ; 如果它返回一个HttpResponse对象 , 则将应用模板响应和响应中间件 , 并将生成的响应返回给浏览器 ; 否则 , 就会以默认错误处理方式进行处理 , 可见 [default exception handling](https://docs.djangoproject.com/en/1.11/ref/views/#error-views) 

在请求期间 , 中间件执行顺序是顺序执行的 ; 而在响应期间 , 中间件执行顺序是倒序执行的

### process_template_response()  🍀

```python
process_template_response(request, response):
    """
    这个方法必须返回一个实现了render方法的响应对象,
    它可以修改给定的response.template_name对象,
    通过修改response和response.context_data或者它可以创建一个全新的TemplateResponse或等价的对象
    request:是一个HttpRequest对象
    response:是一个TemplateResponse对象(或等价的对象),由Django视图或者中间件返回
    """
```

如果响应的实例有`render()` 方法 , `process_template_response()` 在视图刚好执行完毕之后被调用 , 这表明了它是一个`TemplateResponse` 对象

你不需要显示渲染响应 , 一旦所有的模板响应中间件被调用 , 响应会自动被渲染

在一个响应的处理期间 , 中间件以相反的顺序运行 , 包括`process_template_response()` 

## Dealing with streaming responses  🍀

不像HttpResponse , StreamingHttpResponse并没有content属性 , 所以中间件再也不能假设所有响应都带有content属性 ; 如果它们需要访问内容 , 他们必须测试是否为流响应 , 并相应地调整自己的行为

```python
if response.streaming:
    response.streaming_content = wrap_streaming_content(response.streaming_content)
else:
    response.content = alter_content(response.content)
```

我们需要假设`streaming_content` 可能会大到在内存中无法容纳 , 响应中间件可能会把封装在新的生成器中 , 但是一定不要销毁它 , 封装一般实现如下 : 

```python
def wrap_streaming_content(content):
    for chunk in content:
        yield alter_content(chunk)
```

## Exception handling  🍀

Django自动将视图或中间件引发的异常转换为具有错误状态代码的适当HTTP响应 

这种转换发生在每个中间件之前和之后 , 因此每个中间件总是可以依靠`get_response()`  

来获取某种HTTP响应 , 中间件不需要担心在`try/except` 中调用`get_response()` , 并处理由稍后的中间件或视图引发的异常

即使链中的下一个中间件引发了一个HTTP 404 异常 , 你的中间件也不会看到这个异常 , 相反 , 它将得到一个带有404标致代码的HttpResponse对象

Django 中的内置中间件 : https://docs.djangoproject.com/en/1.11/ref/middleware/