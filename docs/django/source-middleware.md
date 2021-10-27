# Django - 源码之middleware








<extoc></extoc>

## 介绍

在关于上一篇`runserver`命令的分析中 , 实际上我们跳过了一步 , 那就是关于中间件加载的

当执行`django-admin runsercer`命令时 , 我们知道会执行`runserver.Command`类的`handle()`方法 , 那么加载中间件的这一步在哪里呢 

它就藏在`WSGIHandler`中 , 并且在实例化时就会执行 , 而我们获取这个实例是通过调用`runserver.Command`类的`get_handler()`方法获取的 , 它在`inner_run`中被调用 , 如下 : 

`runserver.Command.inner_run()`

```python
def inner_run(self, *args, **options):
    
    pass	

    # 截取如下内容
    try:
        # 调用get_handler(),返回一个WSGIHandler实例
        # 注意该实例实现了__call__方法...
        handler = self.get_handler(*args, **options)
        run(self.addr, int(self.port), handler,
            ipv6=self.use_ipv6, threading=threading, server_cls=self.server_cls)
        except socket.error as e:
			pass
```

`get_handler()`

```python
def get_handler(self, *args, **options):
    """
    Returns the default WSGI handler for the runner.
    """
    return get_internal_wsgi_application()
```

随后调用`get_internal_wsgi_application()`  →  `get_wsgi_application()`   → `WSGIHandler()`

其构造函数如下 : 

```python
def __init__(self, *args, **kwargs):
    super(WSGIHandler, self).__init__(*args, **kwargs)
    self.load_middleware()
```

##  load_middleware

```python
    def load_middleware(self):
        """
        Populate middleware lists from settings.MIDDLEWARE (or the deprecated
        MIDDLEWARE_CLASSES).

        Must be called after the environment is fixed (see __call__ in subclasses).
        """
        # 请求中间件
        self._request_middleware = []
        # 视图中间件
        self._view_middleware = []
        # 模板中间件
        self._template_response_middleware = []
        # 响应中间件
        self._response_middleware = []
        # 异常中间件
        self._exception_middleware = []

        if settings.MIDDLEWARE is None:
            # 在django比较老的版本(1.10之前)中使用的是settings.MIDDLEWARE_CLASS
            # 这一部分主要是为了解决兼容性问题
            warnings.warn(
                "Old-style middleware using settings.MIDDLEWARE_CLASSES is "
                "deprecated. Update your middleware and use settings.MIDDLEWARE "
                "instead.", RemovedInDjango20Warning
            )
            
            # convert_exception_to_response会将返回的异常转换成响应,它是一个装饰器
            # self._legacy_get_response函数作用为应用请求中间件
            handler = convert_exception_to_response(self._legacy_get_response)
            
            # 从settings中加载中间件
            for middleware_path in settings.MIDDLEWARE_CLASSES:
                # 导入中间件所在模块
                mw_class = import_string(middleware_path)
                try:
                    # 实例化中间件
                    mw_instance = mw_class()
                except MiddlewareNotUsed as exc:
                    if settings.DEBUG:
                        if six.text_type(exc):
                            logger.debug('MiddlewareNotUsed(%r): %s', middleware_path, exc)
                        else:
                            logger.debug('MiddlewareNotUsed: %r', middleware_path)
                    continue
                # 根据中间件类型,将其process_xxxx方法添加如中间件列表
                if hasattr(mw_instance, 'process_request'):
                    self._request_middleware.append(mw_instance.process_request)
                if hasattr(mw_instance, 'process_view'):
                    self._view_middleware.append(mw_instance.process_view)
                # 后三种加载顺序为后来者居上
                if hasattr(mw_instance, 'process_template_response'):
                    self._template_response_middleware.insert(0, mw_instance.process_template_response)
                if hasattr(mw_instance, 'process_response'):
                    self._response_middleware.insert(0, mw_instance.process_response)
                if hasattr(mw_instance, 'process_exception'):
                    self._exception_middleware.insert(0, mw_instance.process_exception)
        else:
            # 默认我们创建Django项目时,settings.MIDDLEWARE不为None
            # self._get_response()解析请求并调用响应的视图,最后返回响应
            handler = convert_exception_to_response(self._get_response)
            for middleware_path in reversed(settings.MIDDLEWARE):
                # 导入中间件所在模块
                middleware = import_string(middleware_path)
                try:
                    # 实例化中间件
                    # 中间件接收一个get_handler参数,这里为self._get_response
                    mw_instance = middleware(handler)
                except MiddlewareNotUsed as exc:
                    if settings.DEBUG:
                        if six.text_type(exc):
                            logger.debug('MiddlewareNotUsed(%r): %s', middleware_path, exc)
                        else:
                            logger.debug('MiddlewareNotUsed: %r', middleware_path)
                    continue

                if mw_instance is None:
                    raise ImproperlyConfigured(
                        'Middleware factory %s returned None.' % middleware_path
                    )

                if hasattr(mw_instance, 'process_view'):
                    self._view_middleware.insert(0, mw_instance.process_view)
                if hasattr(mw_instance, 'process_template_response'):
				self._template_response_middleware.append(mw_instance.process_template_response)
                if hasattr(mw_instance, 'process_exception'):
                    self._exception_middleware.append(mw_instance.process_exception)
                    
			   # 执行中间件实例中的__call__方法,process_request()与process_response()正藏在这里
                # 该__call__方法是现在MiddlewareMixin中
                """
                    def __call__(self, request):
                        response = None
                        if hasattr(self, 'process_request'):
                            response = self.process_request(request)
                        if not response:
                        	# response = self._get_request(request)
                            response = self.get_response(request)
                        if hasattr(self, 'process_response'):
                            response = self.process_response(request, response)
                        return response
                """
                handler = convert_exception_to_response(mw_instance)

        # We only assign to this when initialization is complete as it is used
        # as a flag for initialization being complete.
        # 最后完成中间件链的加载
        self._middleware_chain = handler
```

在上面的代码清单中 , 我们分成两部分来说 , 因为对于中间件的加载 , 在django1.11之前的版本 , 肯定是不会有这么长的 , 原因在于 , 在django1.11中 , 为了解决与老版本之间的兼容性问题 , 作出了一些调整

在老版本中 , Django会直接应用请求中间件和响应中间件 , 也就是`process_request` , `process_response` , 在早起中间件中 , `process_response`总是会被调用 , 即使在这之前`process_request` 已经发生短路并返回了一个响应

而在新版本中 , 请求经过的中间件和响应经过的中间件层数是一样的 , 也就是说 , 一旦发生短路 , 响应就会按照相反的顺序返回 , 根本不会到达后面的中间件 , 所以这也是为什么在下部分代码中 , 只有视图中间件 , 模板中间件和异常中间件相关的内容了

## self._get_response

那么接下来我们就需要看看关于这后部分三个中间件的细节内容了 , 它们在`self._get_response()`中 , 该方法在初始化时就已经被传入各个中间件中 : 

```python
    def _get_response(self, request):
        """
        Resolve and call the view, then apply view, exception, and
        template_response middleware. This method is everything that happens
        inside the request/response middleware.
        """
        response = None
	   
        if hasattr(request, 'urlconf'):
            urlconf = request.urlconf
            set_urlconf(urlconf)
            resolver = get_resolver(urlconf)
        else:
            resolver = get_resolver()
	    # 进行url匹配,查找相关视图
        resolver_match = resolver.resolve(request.path_info)
        callback, callback_args, callback_kwargs = resolver_match
        request.resolver_match = resolver_match

        # Apply view middleware
        for middleware_method in self._view_middleware:
            # self._view_middleware中为process_view
            # 即各个视图中间件中的process_view方法
            response = middleware_method(request, callback, callback_args, callback_kwargs)
            if response:
                # 如果响应不为空,终止处理
                break
	
        if response is None:
            # 返回视图函数
            wrapped_callback = self.make_view_atomic(callback)
            try:
                # 调用视图函数
                response = wrapped_callback(request, *callback_args, **callback_kwargs)
            except Exception as e:
                # 应用异常中间件
                response = self.process_exception_by_middleware(e, request)

        # Complain if the view returned None (a common error).
        if response is None:
            if isinstance(callback, types.FunctionType):    # FBV
                view_name = callback.__name__
            else:                                           # CBV
                view_name = callback.__class__.__name__ + '.__call__'

            raise ValueError(
                "The view %s.%s didn't return an HttpResponse object. It "
                "returned None instead." % (callback.__module__, view_name)
            )

        # If the response supports deferred rendering, apply template
        # response middleware and then render the response
        elif hasattr(response, 'render') and callable(response.render):
            # 如果响应支持延迟渲染,就应用模板中间件
            for middleware_method in self._template_response_middleware:
                response = middleware_method(request, response)
                # Complain if the template response middleware returned None (a common error).
                if response is None:
                    raise ValueError(
                        "%s.process_template_response didn't return an "
                        "HttpResponse object. It returned None instead."
                        % (middleware_method.__self__.__class__.__name__)
                    )

            try:
                response = response.render()
            except Exception as e:
                response = self.process_exception_by_middleware(e, request)

        return response
```

到这里 , 加载工作就差不多了 , 而在上一篇关于runserver的分析中 , 我们也已经知道 , 当请求来到时 , 会调用`ServerHandler`的最高基类`BaseHandler`中的`run()`方法 , 并且已经将`WSGIHandler()`设置为了`application` , 如下 , 我们再次将`run()`源码贴出来 : 

```python
    def run(self, application):
        """Invoke the application"""
        # Note to self: don't move the close()!  Asynchronous servers shouldn't
        # call close() from finish_response(), so if you close() anywhere but
        # the double-error branch here, you'll break asynchronous servers by
        # prematurely closing.  Async servers must return from 'run()' without
        # closing if there might still be output to iterate over.
        try:
            self.setup_environ()

            # self.result = WSGIHandler()(self.environ, self.start_response)
            # 即调用WSGIHandler类的__call__方法
            self.result = application(self.environ, self.start_response)
            self.finish_response()
        except:
            try:
                self.handle_error()
            except:
                # If we get an error handling an error, just give up already!
                self.close()
                raise   # ...and let the actual server figure it out.
```

现在 , 该亮出这个`__call__`了 : 

```python
def __call__(self, environ, start_response):
	set_script_prefix(get_script_name(environ))
	signals.request_started.send(sender=self.__class__, environ=environ)
    # 实例化请求
	request = self.request_class(environ)
    # 处理请求,返回响应对象
	response = self.get_response(request)

	response._handler_class = self.__class__

	status = '%d %s' % (response.status_code, response.reason_phrase)
	response_headers = [(str(k), str(v)) for k, v in response.items()]
	for c in response.cookies.values():
		response_headers.append((str('Set-Cookie'), str(c.output(header=''))))
	start_response(force_str(status), response_headers)
	if getattr(response, 'file_to_stream', None) is not None and environ.get('wsgi.file_wrapper'):
		response = environ['wsgi.file_wrapper'](response.file_to_stream)
	return response
```

最后 , 我们来看看这个处理请求的函数`get_response()` :

```python
def get_response(self, request):
	"""Return an HttpResponse object for the given HttpRequest."""
	# Setup default url resolver for this thread
	set_urlconf(settings.ROOT_URLCONF)
	# self._middleware_chain在加载时已经完成
    # 被装饰后的self._get_response
	response = self._middleware_chain(request)

	# This block is only needed for legacy MIDDLEWARE_CLASSES; if
	# MIDDLEWARE is used, self._response_middleware will be empty.
	try:
		# Apply response middleware, regardless of the response
		for middleware_method in self._response_middleware:
             # 调用中间件
			response = middleware_method(request, response)
			# Complain if the response middleware returned None (a common error).
			if response is None:
				raise ValueError(
					"%s.process_response didn't return an "
					"HttpResponse object. It returned None instead."
					% (middleware_method.__self__.__class__.__name__))
	except Exception:  # Any exception should be gathered and handled
		signals.got_request_exception.send(sender=self.__class__, request=request)
		response = self.handle_uncaught_exception(request, get_resolver(get_urlconf()), sys.exc_info())

	response._closable_objects.append(request)

	# If the exception handler returns a TemplateResponse that has not
	# been rendered, force it to be rendered.
	if not getattr(response, 'is_rendered', True) and callable(getattr(response, 'render', None)):
         # 渲染模板响应
		response = response.render()

	if response.status_code == 404:
		logger.warning(
			'Not Found: %s', request.path,
			extra={'status_code': 404, 'request': request},
		)

	return response
```

到这里 , 对于中间件的分析就差不多了 , 是时候理一理了

## 小结

首先 , 中间件的加载是在启动时就已经加载完成 , 也就是还没有执行`httpd.serve_forever()`之前就已经完成

每一个中间件都是一个类 , 在 `Django1.10` 以后 通过继承 `MiddlewareMixin` 来保证Django版本之间的兼容 , 这是一个过渡 ; 在每一个中间件中会实现 `process_reqeust()` , `process_view()` , `process_template_response()` , `process_response()` , `process_exception()`

**中间件处理步骤 : **

1. 请求通过请求中间件 , 如果process_request返回的response为空 , 则继续下一步 , 否则应用响应中间件处理传入请求与中间件返回的response
2. 应用视图中间件 (应用之前会进行url匹配查找视图函数) , 如果process_view返回的response为空 , 则继续下一步 , 否则应用响应中间件处理传入请求与中间件返回的response
3. 调用视图函数进行处理
4.  如果视图抛出异常 , 应用异常中间件 , 应用响应中间件处理传入请求与中间件返回的response
5. 如果返回的response支持延迟渲染 , 应用模板中间件
6. 应用响应中间件 , 处理传入请求与中间件返回

