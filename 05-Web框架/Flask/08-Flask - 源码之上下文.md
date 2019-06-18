# Flask - 源码之上下文

## 介绍  🍀

阅读本文时 , 请先了解[ Flask 本地线程](https://lyonyang.github.io/blogs/04-Web-Framework/02-Flask/07-Flask%E6%BA%90%E7%A0%81%E4%B9%8B%E6%9C%AC%E5%9C%B0%E7%BA%BF%E7%A8%8B.html) 相关内容 

在 Flask 中实现了两种上下文对象 : 应用上下文与请求上下文 , 它们两者都是本地线程的

**应用上下文**

应用上下文存在的主要原因是 , 在过去 , 没有更好的方式来在请求上下文中附加一堆函数 , 因为 Flask 设计的支柱之一是你可以在一个 Python 进程中拥有多个应用

那么代码如何找到 "正确的" 应用呢 ?  解决这个问题常用的方法是使用 `current_app` 代理 (基于 `werkzeug.local.Local` 实现的 `LocalProxy` 对象) ,  它被限制在当前请求的应用引用  

应用上下文的典型应用场景是缓存一些在发生请求之前要使用到的资源 , 比如生成数据库连接和缓存一些对象

**请求上下文**

本地线程解决了请求对象在函数之间传递的问题 , 但是为了依赖注入或者尝试重用与请求相关的值的代码 , 我们需要一个有效的请求上下文

请求上下文发生在 HTTP 请求开始 , WSGIServer 调用 `Flask.__call__()` 之后 

## 开始示例  🍀

先看一个简单的例子 

```python
from flask import Flask, request

app = Flask(__name__)


@app.route('/people/')
def people():
    name = request.args.get('name')
    return "People Page!"

if __name__ == '__main__':
    app.run()
```

我们先细想一下 , 这里先引用了 `flask.request` , 但是直到用户访问 `/people/` 时才通过 `request.args.get('name')` 获得请求的 `name` 字段 , 而在引用时这个请求还没有发生 , 那么请求上下文是怎么获得的呢 ? 

其流程是这样的 : 

- 用户访问产生请求
- 在发生请求的过程中向 `_request_ctx_stack` 推入这个请求上下文对象 , 它会变成栈顶 , request 就会成为这个请求上下文 , 也就包含了本次请求相关的信息和数据
- 在视图函数中使用 request 就可以使用 `request.args.get('name')` 了

`flask.request` 就是获取一个名为 `_request_ctx_stack` 的栈顶对象的 `LocalProxy` 实例 : 

```python
# partial函数的作用是返回一个给定参数的函数
from functools import partial
from werkzeug.local import LocalStack, LocalProxy

# _lookup_req_object的name参数将固定为'request'
request = LocalProxy(partial(_lookup_req_object, 'request'))

def _lookup_req_object(name):
    # 获取_request_ctx_stack栈顶对象,也就是RequestContext对象
    top = _request_ctx_stack.top
    if top is None:
        raise RuntimeError(_request_ctx_err_msg)
    # 获取RequestContext.request属性值
    return getattr(top, name)
```

上面已经说过 , 请求上下文发生在 HTTP 请求开始 , 而请求的开始则是 `Flask.__call__()` 开始 , WSGIServer 将会调用 Flask 应用对象作为 WSGI 应用 , 也就是会调用 `Flask.wsgi_app()` :

```python
def wsgi_app(self, environ, start_response):
    # 实例化请求上下文对象
    ctx = self.request_context(environ)
    error = None
    try:
        try:
            # 将请求上下文对象压入栈中,在这之前会先将应用上下文压入栈中
            ctx.push()
            # 返回response对象
            response = self.full_dispatch_request()
        except Exception as e:
            error = e
            response = self.handle_exception(e)
        except:
            error = sys.exc_info()[1]
            raise
        # 调用BaseResponse的__call__方法
        # 交给WSGI服务器处理
        return response(environ, start_response)
    finally:
        if self.should_ignore_error(error):
            error = None
        ctx.auto_pop(error)
```

`RequestContext.push()` 如下 : 

```python
def push(self):
    """Binds the request context to the current context."""
    # 获取栈顶
    top = _request_ctx_stack.top
    if top is not None and top.preserved:
        top.pop(top._preserved_exc)

    # Before we push the request context we have to ensure that there
    # is an application context.
    app_ctx = _app_ctx_stack.top
    if app_ctx is None or app_ctx.app != self.app:
        # 生成应用上下文AppContext
        app_ctx = self.app.app_context()
        # 将应用上下文推入栈中
        app_ctx.push()
        self._implicit_app_ctx_stack.append(app_ctx)
    else:
        self._implicit_app_ctx_stack.append(None)

    if hasattr(sys, 'exc_clear'):
        sys.exc_clear()
    # 将请求上下文推入栈中
    _request_ctx_stack.push(self)

    if self.session is None:
        session_interface = self.app.session_interface
        self.session = session_interface.open_session(
            self.app, self.request
        )

        if self.session is None:
            self.session = session_interface.make_null_session(self.app)
```

可以看到在 `RequestContext.push()` 中 , 并不是仅仅将请求上下文压入了栈中 , 同时它还生成了应用上下文并压入了栈中

也就是说 , 事实上在 Web 应用环境中 , 请求上下文和应用上下文是一一对应的 , 请求上下文和应用上下文都是本地线程的

## 全局变量  🍀

Flask 中有 6 个全局变量 : 2 个本地线程变量和 4 个上下文变量 

它们都储存在 `flask.globals.py` : 

```python
# context locals
# 请求上下文栈,存储请求上下文,基于werkzeug的本地线程实现的栈结构
_request_ctx_stack = LocalStack()
# 应用上下文栈,存储应用上下文,基于werkzeug的本地线程实现的栈结构
_app_ctx_stack = LocalStack()

# 应用上下文,它是当前app的实例对象
current_app = LocalProxy(_find_app)
# 请求上下文,它封装了客户端发出的HTTP请求中的内容
request = LocalProxy(partial(_lookup_req_object, 'request'))
# 请求上下文,它存储了用户会话
session = LocalProxy(partial(_lookup_req_object, 'session'))
# 应用上下文,它是处理请求时用作临时存储的对象
g = LocalProxy(partial(_lookup_app_object, 'g'))
```

 `LocalStack()` 的内是在 `werkzeug.local.Local()` 的基础上实现栈的一个结果 , 而 `werkzeug.local.Local()` 在上一篇中已经分析过了

`LocalProxy()` 是一个代理对象 , 如通过它来获取请求上下文对象中的 `request` 属性

关于 `LocalProxy` 的一些说明 : 

`LocalProxy` 传入一个函数为参数 , 其构造函数如下  

```python
def __init__(self, local, name=None):
    # _类名__属性名为私有属性的另一表现形式,此处等价于如下:
    #    self.__local = local
    object.__setattr__(self, '_LocalProxy__local', local)
    object.__setattr__(self, '__name__', name)
    if callable(local) and not hasattr(local, '__release_local__'):
        # "local" is a callable that is not an instance of Local or
        # LocalManager: mark it as a wrapped function.
        object.__setattr__(self, '__wrapped__', local)
```

`LocalProxy` 不会进行额外的操作 , 它会将对其本身的操作转接到上下文对象

我们也可以利用 `LocalStack` 与 `LocalProxy` 自己来实现一个全局可访问的 `current_user` :

```python
from werkzeug.local import LocalStack, LocalProxy
from flask import Flask
import random

app = Flask(__name__)

_user_err_msg = '''\
Working outside of login user.\
'''
_user_stack = LocalStack()


def get_current_user():
    top = _user_stack.top
    if top is None:
        raise RuntimeError(_user_err_msg)
    return top


current_user = LocalProxy(get_current_user)


@app.before_request
def before_request():
    users = ['Lyon', 'Kenneth']
    user = random.choice(users)
    _user_stack.push(user)


@app.teardown_appcontext
def teardown(exc=None):
    _user_stack.pop()


@app.route('/user')
def user_view():
    return current_user.__str__()


if __name__ == '__main__':
    app.run()
```

服务启动后 , 我们多次访问 `http://127.0.0.1:5000/user` 可观察响应

## 请求上下文  🍀

在我们使用 `flask.request` 之前 , 我们必须保证在 `_request_ctx_stack` 中有 `RequestContext` 对象 , 因为在 Flask 中 , 请求的处理是从创建 `RequestContext` 对象 , 并将该对象压入 `_request_ctx_stack` 栈开始的

```python
# ctx = self.request_context(environ)
# environ是由WSGIRequestHandler.make_enviro()制造而来

class RequestContext(object):
    """
    请求上下文中包含了请求相关的所有信息
    """
    def __init__(self, app, environ, request=None):
        # Flask应用实例
        self.app = app
        if request is None:
            # 实例化Request对象
            request = app.request_class(environ)
        self.request = request
        # 为请求创建一个URL适配器
        self.url_adapter = app.create_url_adapter(self.request)
        self.flashes = None
        self.session = None
        # 一个隐式的应用上下文栈
        self._implicit_app_ctx_stack = []
        # 显示上下文是否被保留
        self.preserved = False

        # remembers the exception for pop if there is one in case the context
        # preservation kicks in.
        self._preserved_exc = None

        # 请求后执行函数
        self._after_request_functions = []
        # 将Request对象与URL连接
        self.match_request()
```

既然是上下文对象 , 也就以为着在 `RequestContext` 中必然定义了 `__enter__` 与 `__exit__` :

```python
def __enter__(self):
    # 将RequestContext对象压入栈中并返回
    self.push()
    return self

def __exit__(self, exc_type, exc_value, tb):
    # 关闭上下文环境时从栈中弹出
    self.auto_pop(exc_value)

    if BROKEN_PYPY_CTXMGR_EXIT and exc_type is not None:
        reraise(exc_type, exc_value, tb)
```

所以我们可以使用 `with` 来开启上下文环境 

```python
from flask import Flask
from flask.globals import _request_ctx_stack

app = Flask(__name__)

# 如果你在请求开始前或者请求结束后查看请求上下文栈中的stack
# 很不幸,请求开始前还没有这一属性
# 请求结束后,这一属性也被销毁,因为请求上下文对象销毁了
with app.test_request_context('/?next=http://example.com/') as rqc:
    print(rqc.request)
    print(_request_ctx_stack._local.stack)
"""
执行结果:
<Request 'http://localhost/?next=http:%2F%2Fexample.com%2F' [GET]>
[<RequestContext 'http://localhost/?next=http:%2F%2Fexample.com%2F' [GET] of ex1>]
"""
```

### 回调与错误  🍀

在 Flask 中 , 请求处理时如果发生了一个错误将会发生什么事 ? 这个特殊的行为如下:

1. 在每个请求之前 , 执行 `before_request()` 上绑定的函数 , 如果这些函数中的某个返回了一个响应 , 其它的函数将不再被调用 , 任何情况下 , 这个返回值都将替换视图函数的返回值 (这一步就像 Django 中的中间件一样)
2. 如果 `before_request()` 上绑定的函数没有返回一个响应 ,  常规的请求处理将会生效 , 匹配的视图函数有机会返回一个响应
3. 视图的返回值之后会被转换成一个实际的响应对象 , 并交给 `after_request()` 上绑定的函数适当地替换或修改它
4. 在请求的最后 , 会执行 `teardown_request()` 上绑定的函数 ,  这总会发生 , 即使在一个未处理的异常抛出后或是没有请求前处理器执行过 (例如在测试环境中你有时会想不执行请求前回调)

在生产模式中 , 如果一个异常没有被捕获 , 将调用 500 internal server 的处理 , 在生产模式中 , 即便异常没有被处理过 , 也会冒泡给 WSGI 服务器 , 如此 , 像交互式调试器这样的东西可以提供丰富的调试信息

## 应用上下文  🍀

应用上下文会按需自动创建和销毁 , 如在将请求上下文对象压入栈中时 , 如果应用上下文栈中没有 , 则会先创建应用上下文 , 它不会在线程间移动 , 并且也不会在请求间共享

应用上下文通常是用来缓存那些用于请求之前创建或者请求使用情况下的资源 , 例如数据库连接是注定要使用应用上下文 .  存储的东西时应该为应用程序上下文选择唯一的名称 , 因为这是一个 Flask 应用和扩展之间共享的地方

```python
class AppContext(object):
    """The application context binds an application object implicitly
    to the current thread or greenlet, similar to how the
    :class:`RequestContext` binds request information.  The application
    context is also implicitly created if a request context is created
    but the application is not on top of the individual application
    context.
    """

    def __init__(self, app):
        self.app = app
        self.url_adapter = app.create_url_adapter(None)
        #: The class that is used for the :data:`~flask.g` instance.
        #:
        #: Example use cases for a custom class:
        #:
        #: 1. Store arbitrary attributes on flask.g.
        #: 2. Add a property for lazy per-request database connectors.
        #: 3. Return None instead of AttributeError on unexpected attributes.
        #: 4. Raise exception if an unexpected attr is set, a "controlled" flask.g.
        #:
        #: In Flask 0.9 this property was called `request_globals_class` but it
        #: was changed in 0.10 to :attr:`app_ctx_globals_class` because the
        #: flask.g object is now application context scoped.
        
        # app_ctx_globals_class = _AppCtxGlobals
        self.g = app.app_ctx_globals_class()

        # 引用计数,以追踪被压入栈的次数
        self._refcnt = 0
```

