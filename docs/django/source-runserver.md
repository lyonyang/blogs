# Django - 源码之runserver








<extoc></extoc>

## 介绍

上一篇中 , 我们分析了Django项目从无到有的过程 , 也就是`django-admin startproject`命令 , 随后我们要做的就是启动这个项目 , 也就是执行`django-admin runserver`命令

实际上 , 我们在创建项目时 , 就已经见过这个命令字眼了 , 截取部分代码如下 :

`management/__init__` 

```python
def execute(self):
	"""
	Given the command-line arguments, this figures out which subcommand is
	being run, creates a parser appropriate to that command, and runs it.
	"""
    ......
    # 截取部分片段,为了便于查找,删去部分注释
	if settings.configured:
		if subcommand == 'runserver' and '--noreload' not in self.argv:
			try:
				autoreload.check_errors(django.setup)()
			except Exception:
				apps.all_models = defaultdict(OrderedDict)
				apps.app_configs = OrderedDict()
				apps.apps_ready = apps.models_ready = apps.ready = True
				_parser = self.fetch_command('runserver').create_parser('django', 'runserver')
				_options, _args = _parser.parse_known_args(self.argv[2:])
				for _arg in _args:
					self.argv.remove(_arg)
		# In all other cases, django.setup() is required to succeed.
		else:
			django.setup()
	......
```

在我们第一次创建Django项目时 , 会直接执行`django.setup()` , 在上一篇中 , 关于导入工作中忽略了一条语句 : `from django.utils import autoreload, lru_cache, six` , 这其中的`autoreload`是一个自动加载的触发器 , 它会加载一个配置`RUN_RELOADER = True` ,  这也是我们自动重启服务端的一个开关 , 默认它是开着的

实际上执行runserver与startproject是一样的 , 只不过在配置时 , runserver会进行一些错误检查 , 主要是为了检查其兼容性 , 随后像其他命令一样 , 实例化各自模块中的Command类 , 随后调用`execute()` → `handle()`  , 我们直接从`handle()`开始

## handle

`django/core/management/commands/runserver.py` 

```python
def handle(self, *args, **options):
	# 导入Django配置文件
	from django.conf import settings
	if not settings.DEBUG and not settings.ALLOWED_HOSTS:
		raise CommandError('You must set settings.ALLOWED_HOSTS if DEBUG is False.')
	
	# 判断ipv6是否可用,该方式需要通过add_arguments来添加
	self.use_ipv6 = options['use_ipv6']
	if self.use_ipv6 and not socket.has_ipv6:
		raise CommandError('Your Python does not support IPv6.')
	self._raw_ipv6 = False
	if not options['addrport']:
		# 默认使用本地ip地址,端口为8000
		self.addr = ''
		self.port = self.default_port
	else:
		# 获取addrport中的相关参数
		m = re.match(naiveip_re, options['addrport'])
		if m is None:
			raise CommandError('"%s" is not a valid port number '
							   'or address:port pair.' % options['addrport'])
		self.addr, _ipv4, _ipv6, _fqdn, self.port = m.groups()
		if not self.port.isdigit():
			raise CommandError("%r is not a valid port number." % self.port)
		if self.addr:
			if _ipv6:
				self.addr = self.addr[1:-1]
				self.use_ipv6 = True
				self._raw_ipv6 = True
			elif self.use_ipv6 and not _fqdn:
				raise CommandError('"%s" is not a valid IPv6 address.' % self.addr)
	if not self.addr:
		self.addr = '::1' if self.use_ipv6 else '127.0.0.1'
		self._raw_ipv6 = self.use_ipv6
	# 启动服务器
	self.run(**options)
```

再随后 , 在`run`中会调用`inner_run` , 具体源码如下 : 

```python
def inner_run(self, *args, **options):
	# If an exception was silenced in ManagementUtility.execute in order
	# to be raised in the child process, raise it now.
	autoreload.raise_last_exception()

	threading = options['use_threading']
	# 'shutdown_message' is a stealth option.
	shutdown_message = options.get('shutdown_message', '')
	quit_command = 'CTRL-BREAK' if sys.platform == 'win32' else 'CONTROL-C'

	self.stdout.write("Performing system checks...\n\n")
	self.check(display_num_errors=True)
	# Need to check migrations here, so can't use the
	# requires_migrations_check attribute.
	self.check_migrations()
	now = datetime.now().strftime('%B %d, %Y - %X')
	if six.PY2:
		now = now.decode(get_system_encoding())
	self.stdout.write(now)
	self.stdout.write((
		"Django version %(version)s, using settings %(settings)r\n"
		"Starting development server at %(protocol)s://%(addr)s:%(port)s/\n"
		"Quit the server with %(quit_command)s.\n"
	) % {
		"version": self.get_version(),
		"settings": settings.SETTINGS_MODULE,
		"protocol": self.protocol,
		"addr": '[%s]' % self.addr if self._raw_ipv6 else self.addr,
		"port": self.port,
		"quit_command": quit_command,
	})

	try:
         # 这里最终获取的是WSGIHandler的实例,并且中间件的加载也是在这一步中完成的
		handler = self.get_handler(*args, **options)
         # 我们把实参补全来观察
         # run('127.0.0.1', 8000, WSGIHandler(), False, threading, WSGIServer)
		run(self.addr, int(self.port), handler,
			ipv6=self.use_ipv6, threading=threading, server_cls=self.server_cls)
	except socket.error as e::
        pass # 省略我们直接看看真正的run吧
        
def run(addr, port, wsgi_handler, ipv6=False, threading=False, server_cls=WSGIServer):
    server_address = (addr, port)
    if threading:
        # 重新构造WSGIServer,并继承了socketserver.ThreadingMixIn和原WSGIServer
        httpd_cls = type(str('WSGIServer'), (socketserver.ThreadingMixIn, server_cls), {})
    else:
        httpd_cls = server_cls
        
    # 实例化新的WSGIServer
    httpd = httpd_cls(server_address, WSGIRequestHandler, ipv6=ipv6)
    if threading:
        # 加快自动重启以及防止线程不正常终止
        httpd.daemon_threads = True
    # wsgi_handler=WSGIHandler(),set_app结果:self.application = WSGIHandler()
    httpd.set_app(wsgi_handler)
    # socketserver.serve_forever,至此Web服务器启动
    httpd.serve_forever()
```

## 处理请求

调用`serve_forver()`之后 , 我们的服务端就已经做好随时 "接客" (HTTP请求) 的准备了

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
                      # 处理请求
					self._handle_request_noblock()

				self.service_actions()
	finally:
		self.__shutdown_request = False
		self.__is_shut_down.set()
```

在分析如何处理请求之前 , 我们需要理清由`type`构造的这个新的`WSGIServer` 到底继承了基类的哪些东西 , 因为这关系到在请求处理过程 , 到底会执行该实例的哪一个方法 

由于这个构造出来的新类其继承体系有点庞大 , 所以这里将直接观察其真正的执行方法

`self._handle_reqeust_noblock()` 具体内容如下 : 

```python
def _handle_request_noblock(self):
    """Handle one request, without blocking.

    I assume that selector.select() has returned that the socket is
    readable before this function was called, so there should be no risk of
    blocking in get_request().
    """
    try:
        # 获取请求和客户端地址
        request, client_address = self.get_request()
    except OSError:
        return
    if self.verify_request(request, client_address):
        try:
            # 调用finish_request
            self.process_request(request, client_address)
        except:
            self.handle_error(request, client_address)
            self.shutdown_request(request)
    else:
        self.shutdown_request(request)
```

`self.process_request(request, client_address)` 具体内容如下 : 

```python
def process_request(self, request, client_address):
    self.finish_request(request, client_address)
    self.shutdown_request(request)
```

`self.finish_request(request, client_address)` 具体内容如下 : 

```python
def finish_request(self, request, client_address):
    """Finish one request by instantiating RequestHandlerClass."""
    # self.RequestHandlerClass = WSGIRequestHandler
    self.RequestHandlerClass(request, client_address, self)
```

就像源码注释中所说 , 它将通过实例化一个RequestHandleClass类 , 来处理一个请求 , 这个类就是`WSGIRequestHandler`  , 这个类的构造函数在其最高基类`BaseRequestHandler` 中 , 如下 : 

 ```python
def __init__(self, request, client_address, server):
    self.request = request
    self.client_address = client_address
    self.server = server
    self.setup()
    try:
        self.handle()
    finally:
        self.finish()
 ```

也就是说 , 在实例化时会调用类中的`handler`方法 , 这个方法在WSGIRequestHandler中被重写了 , 如下 : 

```python
def handle(self):
    """Copy of WSGIRequestHandler, but with different ServerHandler"""

    self.raw_requestline = self.rfile.readline(65537)
    if len(self.raw_requestline) > 65536:
        self.requestline = ''
        self.request_version = ''
        self.command = ''
        self.send_error(414)
        return

    if not self.parse_request():  # An error code has been sent, just exit
        return
    # 实例化并设置HTTP环境变量
    handler = ServerHandler(
        self.rfile, self.wfile, self.get_stderr(), self.get_environ()
    )
    handler.request_handler = self      # backpointer for logging
    
    # self.server = httpd = httpd_cls(server_address, WSGIRequestHandler, ipv6=ipv6)
    # self.server.get_app() = WSGIHandler()
    handler.run(self.server.get_app())
```

最后执行run , 该方法来自于`ServerHandler`的最高基类`BaseHandler` , 源码如下 : 

```python
    def run(self, application):
        """Invoke the application"""
        # Note to self: don't move the close()!  Asynchronous servers shouldn't
        # call close() from finish_response(), so if you close() anywhere but
        # the double-error branch here, you'll break asynchronous servers by
        # prematurely closing.  Async servers must return from 'run()' without
        # closing if there might still be output to iterate over.
        try:
            # 设置WSGi环境变量
            self.setup_environ()
            
            # self.result = WSGIHandler()(self.environ, self.start_response)
            # 调用__call__方法,返回结果
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

`WSGIHandler().__call__(self.environ, self.start_response)` 如下 : 

```python
def __call__(self, environ, start_response):
    set_script_prefix(get_script_name(environ))
    signals.request_started.send(sender=self.__class__, environ=environ)
    # 生成请求对象
    request = self.request_class(environ)
    # 根据请求获取响应对象
    response = self.get_response(request)

    response._handler_class = self.__class__
    # 状态码
    status = '%d %s' % (response.status_code, response.reason_phrase)
    # 响应头
    response_headers = [(str(k), str(v)) for k, v in response.items()]
    for c in response.cookies.values():
        response_headers.append((str('Set-Cookie'), str(c.output(header=''))))
    start_response(force_str(status), response_headers)
    if getattr(response, 'file_to_stream', None) is not None and environ.get('wsgi.file_wrapper'):
        response = environ['wsgi.file_wrapper'](response.file_to_stream)
    return response
```

最后`finish_response()` , 返回响应 , 关闭套接字 ; 当然 , 服务器还是继续等待 "客人" 来光临 ! 

```python
def finish_response(self):
    """Send any iterable data, then close self and the iterable

    Subclasses intended for use in asynchronous servers will
    want to redefine this method, such that it sets up callbacks
    in the event loop to iterate over the data, and to call
    'self.close()' once the response is finished.
    """
    try:
        if not self.result_is_file() or not self.sendfile():
            for data in self.result:
                self.write(data)
            self.finish_content()
    finally:
        self.close()
```

## 小结

分析过程中 , 为了避免派生类重写了基类中的方法而导致分析出错 , 不妨将所有方法整合到一个类中 , 虽然这个工作也不好做 , 但是却是不会出错 

我们通过一条 "执行线" 来完成本次小结 : 

```python
django-admin runserver  →  Command()  →  handle()  →  run()  →  
  →  inner_run()  →  self.get_handler(*args, **options)  →  
  →  basehttp.run()  →  httpd  →  httpd.serve_forever()  →   
  →  self.RequestHandlerClass(request, client_address, self)  →  self.handle()  →  
  →  ServerHandler(self.rfile, self.wfile, self.get_stderr(), self.get_environ())  →  
  →  handler.run(self.server.get_app())  →  
  →  WSGIHandler()(self.environ, self.start_response) → __call__
  →  self.finish_response()
```

处理请求过程 : 当一个HTTP请求到达服务器 , `WSGIServer`类会通过调用`WSGIRequestHandler`类的handle()方法来处理HTTP请求 , 在处理请求时 , 会先创建一个WSGI应用程序`(WSGIHandler)`接口的实例 , 随后作为参数传给`ServerHandler`类 , 最后对其进行处理