# Flask - 源码之开始

## 介绍  🍀

Flask 中文文档比较齐全 , 阅读源码最好的方式应该是从最简单的应用开始

直接使用官方快速入门中的最小的应用开始 

```python
from flask import Flask
# 实例化Flask对象
# __name__ 为模块名,当前为 __main__
app = Flask(__name__)

# 绑定路由
@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
```

## 绑定路由  🍀

我们首先实例化了 Flask 对象 , 我们传入了一个参数 `import_name` , 该参数的概念是给 Flask 一个属于你的应用程序的概念 , 它用于查找文件系统上的资源 , 可以由扩展名用于改进调试信息等

随后写了一个视图函数 `hello_world` 以及给这个视图函数添加了一个装饰器 ; 当然 , 我们已经知道这个装饰器的作用是添加路由规则 , 我们看看它具体是怎么做的 

`flask.app.Flask.route()` :

```python
def route(self, rule, **options):
    """
    rule:URL规则的字符串
    **options:该参数将在实例化Rule对象时作为参数传入
        - options参数:
        		- defaults=None,默认值,当URL中无参数,函数需要参数时,使用defaults={'page': 1}
        		- subdomain=None,子域名访问,默认由Map对象提供,即为 ''
        		- methods=None,允许的请求方式
                 - build_only=False,如果为True,则URL无法匹配但是仍然会构建
                 - endpoint=None,端点,用于反向生成URL,即:url_for()
                 - strict_slashes=None,对URL最后的 / 符号是否严格要求,默认由Map对象提供,即为True
                 - redirect_to=None,重定向到指定地址
                 - alias=False,如果为True,则作为另一条端点和参数相同的规则的别名
                 - host=None,为整个主机提供匹配规则
    """
    def decorator(f):
        # 获取endpoint参数,默认是为None的
        # endpoint参数用于反向生成url时使用
        endpoint = options.pop('endpoint', None)
        self.add_url_rule(rule, endpoint, f, **options)
        return f
    return decorator
```

`app.route('/') == decorator`  →→ `@app.route('/') == @decorator`  , 于是在此装饰器执行时 , 将执行 `self.add_url_rule()` , 源码如下 : 

`flask.app.Flask.add_url_rule()` :

```python
@setupmethod  # 该装饰器与调试模式有关,我们可以跳过它
def add_url_rule(self, rule, endpoint=None, view_func=None,
                 provide_automatic_options=None, **options):

    if endpoint is None:
        # 返回视图函数的函数名
        endpoint = _endpoint_from_view_func(view_func)
    options['endpoint'] = endpoint
    # 获取options中的methods参数,它是一个列表
    methods = options.pop('methods', None)

    if methods is None:
        # 如果view_func为CBV方式,并且有methods参数,否则使用('GET)
        methods = getattr(view_func, 'methods', None) or ('GET',)
    if isinstance(methods, string_types):
        raise TypeError('Allowed methods have to be iterables of strings, '
                        'for example: @app.route(..., methods=["POST"])')
    # 转换成大写
    methods = set(item.upper() for item in methods)

    # 必要属性
    required_methods = set(getattr(view_func, 'required_methods', ()))

    # 强制启用自动选项处理
    if provide_automatic_options is None:
        provide_automatic_options = getattr(view_func,
            'provide_automatic_options', None)

    if provide_automatic_options is None:
        if 'OPTIONS' not in methods:
            provide_automatic_options = True
            required_methods.add('OPTIONS')
        else:
            provide_automatic_options = False

    # 添加必要属性到methods
    methods |= required_methods
    # 实例化Rule对象
    rule = self.url_rule_class(rule, methods=methods, **options)
    rule.provide_automatic_options = provide_automatic_options
	
    # 生成url并完成绑定
    self.url_map.add(rule)
    if view_func is not None:
        # view_func为视图函数
        old_func = self.view_functions.get(endpoint)
        if old_func is not None and old_func != view_func:
            raise AssertionError('View function mapping is overwriting an '
                                 'existing endpoint function: %s' % endpoint)
        # 将视图函数加入Flask对象的view_functions属性中,以端点为key
        # self.view_functions = {}
        self.view_functions[endpoint] = view_func
```

## 启动WSGI服务器  🍀

到这里 , 好像路由与视图函数都准备好了 , 那么接下来就是启动该应用了 , `app.run()` 

```python
def run(self, host=None, port=None, debug=None,
        load_dotenv=True, **options):
	......
    from werkzeug.serving import run_simple
    try:
        # 启动WSGI应用
        run_simple(host, port, self, **options)
    finally:
        self._got_first_request = False
```

接下来将会执行 `werkzeug.serving.run_simple` 中的 `inner` 

```python
def inner():
    try:
        fd = int(os.environ['WERKZEUG_SERVER_FD'])
    except (LookupError, ValueError):
        fd = None
    # 创建一个服务器实例
    # BaseWSGIServer
    srv = make_server(hostname, port, application, threaded,
                      processes, request_handler,
                      passthrough_errors, ssl_context,
                      fd=fd)
    if fd is None:
        log_startup(srv.socket)
    # 启动服务器
    # BaseWSGIServer.serve_forever()
    srv.serve_forever()
```

`BaseWSGIServer` 继承了`http.server.HTTPServer` , `BaseWSGIServer.serve_forever()` 如下 : 

```python
def serve_forever(self):
    self.shutdown_signal = False
    try:
        # 一次处理一个请求直到服务器关闭
        # 将BaseWSGIServer对象作为参数传入
        HTTPServer.serve_forever(self)
    except KeyboardInterrupt:
        pass
    finally:
        self.server_close()
```

由于 `HTTPServer` 继承自 `socketserver.TCPServer`  , 并且它并没有重写 `serve_forever` , 所以 , 源代码如下 : 

```python
def serve_forever(self, poll_interval=0.5):
    """Handle one request at a time until shutdown.

    Polls for shutdown every poll_interval seconds. Ignores
    self.timeout. If you need to do periodic tasks, do them in
    another thread.
    """
    self.__is_shut_down.clear()
    try:
        # XXX: Consider using another file descriptor or connecting to the
        # socket to wake this up instead of polling. Polling reduces our
        # responsiveness to a shutdown request and wastes cpu at all other
        # times.
        with _ServerSelector() as selector:
            selector.register(self, selectors.EVENT_READ)

            while not self.__shutdown_request:
                ready = selector.select(poll_interval)
                if ready:
                    self._handle_request_noblock()

                self.service_actions()
    finally:
        self.__shutdown_request = False
        self.__is_shut_down.set()
```

到这里 , 我们不妨来对比一下 , 在 Django 中 , 创建服务器实例是由 `wsgiref.simple_server.WSGIServer` 衍生而来 , 而 `WSGIServer` 继承了`http.server.HTTPServer`

而在 Flask 中 , 如上 , 也继承了 `http.server.HTTPServer` 

## 创建服务器实例  🍀

在 `BaseWSGIServer` 进行实例化时 , 与 Django 一样 , 都传入了一个 `RequestHandlerClass` 参数 , 这个参数听名字就知道 , 它是处理请求的核心 , 源码如下 : 

```python
class BaseWSGIServer(HTTPServer, object):

    """Simple single-threaded, single-process WSGI server."""
    # 省略部分代码
    def __init__(self, host, port, app, handler=None,
                 passthrough_errors=False, ssl_context=None, fd=None):
        if handler is None:
            # werkzeug.serving.WSGIRequestHandler
            # Django:django.core.servers.basehttp.WSGIRequestHandler
            handler = WSGIRequestHandler
        # RequestHandlerClass为出去self后第二个参数,handler
        HTTPServer.__init__(self, get_sockaddr(host, int(port),
                                               self.address_family), handler)

```

回到 `serve_forever` 中 , 调用 `self._handle_request_noblock()`  , 随后再调用 `self.process_request(request, client_address)` 

```python
    def process_request(self, request, client_address):
        """Call finish_request.

        Overridden by ForkingMixIn and ThreadingMixIn.

        """
        self.finish_request(request, client_address)
        self.shutdown_request(request)
```

最后调用了 `self.finish_request(request, client_address)` 

```python
def finish_request(self, request, client_address):
    """Finish one request by instantiating RequestHandlerClass."""
    self.RequestHandlerClass(request, client_address, self)
```

## 实例化WSGI请求处理类  🍀

至此 , 在创建服务器实例 , 也就是 `BaseWSGIServer` 时 , 已经将该类传入 , 即 `WSGIRequestHandler` ; 重点来了 , `WSGIRequestHandler` 自身根本没有构造函数 , 它的基类 `socketserver.TCPServer` 还是没有 , 继续往上发现 , 关于 `RequestHandlerClass` 初始化的函数在继承链的顶部 `socketserver.BaseServer` 中 , 其构造函数如下 :


```python
def __init__(self, request, client_address, server):
    self.request = request
    self.client_address = client_address
    self.server = server
    self.setup()
    try:
        # 该函数在WSGIRequestHandler中进行了重构
        self.handle()
    finally:
        self.finish()
```

`WSGIRequestHandler.handler()`  如下 : 


```python
def handle(self):
    """Handles a request ignoring dropped connections."""
    rv = None
    try:
        # 其基类的handler
        rv = BaseHTTPRequestHandler.handle(self)
    except (socket.error, socket.timeout) as e:
        self.connection_dropped(e)
    except Exception:
        if self.server.ssl_context is None or not is_ssl_error():
            raise
    if self.server.shutdown_signal:
        self.initiate_shutdown()
    return rv
```

```python
def handle(self):
    """Handle multiple requests if necessary."""
    self.close_connection = True
    
    # 该方法在WSGIRequestHandler被重写
    self.handle_one_request()
    while not self.close_connection:
        self.handle_one_request()
```

重写源码如下 : 

```python
def handle_one_request(self):
    """Handle a single HTTP request."""
    self.raw_requestline = self.rfile.readline()
    if not self.raw_requestline:
        self.close_connection = 1
    elif self.parse_request():
        # 运行WSGI应用服务器
        return self.run_wsgi()
```

## 视图调度  🍀

摘取 `run_wsgi()` 部分代码如下 : 

```python
def run_wsgi(self):
    if self.headers.get('Expect', '').lower().strip() == '100-continue':
        self.wfile.write(b'HTTP/1.1 100 Continue\r\n\r\n')
    # 环境处理
    self.environ = environ = self.make_environ()
    headers_set = []
    headers_sent = []

    def write(data):
		pass
    def start_response(status, response_headers, exc_info=None):
		pass
    def execute(app):
        # 调用Flask应用实例的__call__方法
        # Flask(__name__)(environ, start_response)
        application_iter = app(environ, start_response)
        try:
            for data in application_iter:
                write(data)
            if not headers_sent:
                write(b'')
        finally:
            if hasattr(application_iter, 'close'):
                application_iter.close()
            application_iter = None

    try:
        # self.server = BaseWSGIServer
        # BaseWSGIServer.app即Flask应用实例
        execute(self.server.app)
	    pass
```

`Flask.__call__` 源码如下 : 

```python
def __call__(self, environ, start_response):
    """The WSGI server calls the Flask application object as the
    WSGI application. This calls :meth:`wsgi_app` which can be
    wrapped to applying middleware."""
    # WSGI服务器调用Flask应用对象作为WSGI应用
    return self.wsgi_app(environ, start_response)
```

```python
def wsgi_app(self, environ, start_response):
    # 请求上下文对象
    ctx = self.request_context(environ)
    error = None
    try:
        try:
            # 将请求上下文对象推入栈中
            # _request_ctx_stack.push(self)
            # self = RequestContext(environ)
            ctx.push()
            # 分派请求
            response = self.full_dispatch_request()
        except Exception as e:
            error = e
            response = self.handle_exception(e)
        except:
            error = sys.exc_info()[1]
            raise
        # 执行Response对象的__call__方法
        # 这里将由werkzeug来进行处理
        # werkzeug.wrappers.BaseResponse.__call__
        # start_response在run_wsgi函数中
        # def __call__(self, environ, start_response):
                """Process this response as WSGI application.

                :param environ: the WSGI environment.
                :param start_response: the response callable provided by the WSGI
                                       server.
                :return: an application iterator
                """
                # app_iter, status, headers = self.get_wsgi_response(environ)
                # start_response(status, headers)
                # return app_iter
        return response(environ, start_response)
    finally:
        if self.should_ignore_error(error):
            error = None
        ctx.auto_pop(error)
```
`self.full_dispatch_request()` 

```python
def full_dispatch_request(self):
    """Dispatches the request and on top of that performs request
    pre and postprocessing as well as HTTP exception catching and
    error handling.

    .. versionadded:: 0.7
    """
    self.try_trigger_before_first_request_functions()
    try:
        request_started.send(self)
        # 请求预处理
        rv = self.preprocess_request()
        if rv is None:
            # 进行视图调度
            rv = self.dispatch_request()
    except Exception as e:
        rv = self.handle_user_exception(e) 
    # 完成请求
    return self.finalize_request(rv)
```

预处理过程如下 : 

```python
def preprocess_request(self):
    """Called before the request is dispatched. Calls
    :attr:`url_value_preprocessors` registered with the app and the
    current blueprint (if any). Then calls :attr:`before_request_funcs`
    registered with the app and the blueprint.

    If any :meth:`before_request` handler returns a non-None value, the
    value is handled as if it was the return value from the view, and
    further request handling is stopped.
    """
    # 从请求上下文栈中获取蓝图
    bp = _request_ctx_stack.top.request.blueprint
    # 预处理函数
    # self.url_value_preprocessors = {}
    funcs = self.url_value_preprocessors.get(None, ())
    if bp is not None and bp in self.url_value_preprocessors:
        funcs = chain(funcs, self.url_value_preprocessors[bp])
    for func in funcs:
        # 执行预处理
        func(request.endpoint, request.view_args)
    # 在处理请求之前调用的函数
    # self.before_request_funcs = {}
    funcs = self.before_request_funcs.get(None, ())
    if bp is not None and bp in self.before_request_funcs:
        funcs = chain(funcs, self.before_request_funcs[bp])
    for func in funcs:
        rv = func()
        if rv is not None:
            # 有返回值请求处理结束
            return rv
```

视图调度 , `self.dispatch_request()`

```python
def dispatch_request(self):
    """Does the request dispatching.  Matches the URL and returns the
    return value of the view or error handler.  This does not have to
    be a response object.  In order to convert the return value to a
    proper response object, call :func:`make_response`.

    .. versionchanged:: 0.7
       This no longer does the exception handling, this code was
       moved to the new :meth:`full_dispatch_request`.
    """
    # 从栈中获取请求上下文对象
    req = _request_ctx_stack.top.request
    if req.routing_exception is not None:
        self.raise_routing_exception(req)
    rule = req.url_rule
    # if we provide automatic options for this URL and the
    # request came with the OPTIONS method, reply automatically
    if getattr(rule, 'provide_automatic_options', False) \
       and req.method == 'OPTIONS':
        return self.make_default_options_response()
    # otherwise dispatch to the handler for that endpoint
    # 通过endpoint参数获取视图函数并调用,视图函数参数从获取的请求上下文对象中获取
    return self.view_functions[rule.endpoint](**req.view_args)
```

视图调度完成后 , 接下来就是完成请求了 , 从 `dispatch_request` 或者 `preprocess_request` 中已经获取了需要的 `rv` , 最后就是执行 `full_dispatch_request()` 中的最后一行 

```python
return self.finalize_request(rv)
```

 `finalize_request()` 源码如下 : 

```python
def finalize_request(self, rv, from_error_handler=False):
    """Given the return value from a view function this finalizes
    the request by converting it into a response and invoking the
    postprocessing functions.  This is invoked for both normal
    request dispatching as well as error handlers.

    Because this means that it might be called as a result of a
    failure a special safe mode is available which can be enabled
    with the `from_error_handler` flag.  If enabled, failures in
    response processing will be logged and otherwise ignored.

    :internal:
    """
    # 将视图返回值转换成response对象
    response = self.make_response(rv)
    try:
        # 请求结束后处理
        response = self.process_response(response)
        request_finished.send(self, response=response)
    except Exception:
        if not from_error_handler:
            raise
        self.logger.exception('Request finalizing failed with an '
                              'error while handling an error')
    # 返回响应
    return response
```

到这里其实我们已经分析的差不多了 , 当 response 对象获取之后 , 一步步往外返回 , 将会返回到  werkzeug 层次 , 当然 werkzeug 也是使用 socketserver 的一部分功能来完成这些操作 , 这一部分就不再分析了

## 小结  🍀

首先 , 从整体来讲 , 我们可以通过与 Django 进行对比 : 

- Django , 使用 wsgiref + socketserver + http
- Flask , 使用 werkzeug + socketserver + http

在传输层 , 两者都是使用的 socketserver , 当然它们在 socketserver 的基础上做了一些不同的改变

那么对于 Flask 运行到处理请求流程如下 : 

1. 创建 Flask 应用对象
2. 添加路由映射
3. 启动服务器
4. 请求来临 , 创建请求上下文对象 , 并压入请求上下文栈
5. 处理请求 , 从栈中获取对象 , 调用视图 (`dispatch_request`)
6. 将视图返回值打包成响应对象
7. 完成响应