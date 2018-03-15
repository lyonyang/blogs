# Python之路 - 标准库之wsgiref

## 介绍  🍀

wsgiref模块是WSGI规范的一个参考实现 , 它可以用于将WSGI支持添加到Web服务器或框架中 , 它提供了用于操作WSGI环境变量和响应头的实用工具 、 用于实现WSGI服务器的基类 、 用于服务WSGI应用程序的样本HTTP服务器 、以及检查WSGI服务器和应用程序的验证工具 , 以满足WSGI规范(PEP3333)

包内容

```python
handlers        - server/gateway base classes
headers         - WSGI response header tools
simple_server   - a simple WSGI HTTP server
util            - WSGI environment utilities
validate        - WSGI conformance checker
```

## handlers  🍀

这个模块提供了用于实现WSGI服务器和网关的基本处理程序类 . 这些基类处理与WSGI应用程序通信的大部分工作 , 只要它们提供了一个`CGI-like`环境 , 以及输入、输出和错误流

CLASSES

```python
builtins.object
BaseHandler
	"""管理WSGI应用程序的调用"""
	SimpleHandler
    	"""初始化数据流,环境等的处理程序"""
		BaseCGIHandler
        	"""CGI-like系统,使用输入/输出/错误流和环境映射"""
			CGIHandler
            	"""CGI-based调用,通过sys.stdin/stdout/stderr和os.environ"""
				IISCGIHandler
                	"""CGI-based调用与IIS路径错误的解决方法"""
# 由上到下是一个基类到子类的过程
```

以上类中主要的实现在`BaseHandler`中 , 其它几个都是在基类基础上做了简单的实现

FUNCTIONS

```python
read_environ()
	"""读取环境,修改HTTP变量"""
```

本文中所有思维导图全部来自[这里 , 点我吧](https://github.com/minixalpha/SourceLearning/tree/master/wsgiref-0.1.2)

![handlers](http://oux34p43l.bkt.clouddn.com/handlerss.bmp)

对于各个类中的具体实现 , 可以去阅读源代码https://pypi.python.org/pypi/wsgiref

## headers  🍀

这个模块提供了一个类(Headers) , 可以使用mapping-like的接口来方便地操作WSGI响应头 , 也就是一个类似于dict的数据结构 , 并且其实现了dict操作中的`get` , `keys` , `values` 函数

CLASSES

```python
builtins.object
	Headers
class Headers(builtins.object)
     """管理一个HTTP响应头的集合"""
```

headers思维导图

![headers](http://oux34p43l.bkt.clouddn.com/headers.bmp)!

## simple_server  🍀

这个模块实现了一个WSGI应用程序的简单HTTP服务器 (基于HTTP.server) , 每个服务器实例都在给定的主机和端口上提供一个WSGI应用

CLASSES

```python
http.server.BaseHTTPRequestHandler(socketserver.StreamRequestHandler)
	WSGIRequestHandler
#       WSGIRequestHandler继承体系
#         +--------------------+
#         | BaseRequestHandler |
#         +--------------------+
#                   ↓
#         +-----------------------+
#         | StreamRequestHandler  |
#         +-----------------------+
#                   ↓
#         +------------------------+
#         | BaseHTTPRequestHandler |
#         +------------------------+
#                   ↓
#         +--------------------+
#         | WSGIRequestHandler |
#         +--------------------+
http.server.HTTPServer(socketserver.TCPServer)
	WSGIServer
#       WSGIServer继承体系
#         +------------+
#         | BaseServer |
#         +------------+
#               ↓
#         +------------+
#         | TCPServer  |
#         +------------+
#               ↓
#         +------------+
#         | HTTPServer |
#         +------------+
#               ↓
#         +------------+
#         | WSGIServer |
#         +------------+
class WSGIRequestHandler(http.server.BaseHTTPRequestHandler)
	"""HTTP请求处理程序基类"""
class WSGIServer(http.server.HTTPServer)
	"""实现Python WSGI协议的BaseHTTPServer"""
```

FUNCTIONS

```python
demo_app(environ, start_response)
	"""应用程序部分"""
make_server(host, port, app, server_class=<class 'wsgiref.simple_server.WSGIServer'>, handler_class=<class 'wsgiref.simple_server.WSGIRequestHandler'>)
	"""创建一个新的WSGI服务器,监听主机和端口"""
```

simple_server思维导图

![simple_server](http://oux34p43l.bkt.clouddn.com/simple_server.bmp)

simple_server模块主要有两部分内容

1. 应用程序

   函数demo_app是应用程序部分

2. 服务器程序

   服务器程序主要分成Server和Handler两部分 , 另外make_server函数用来生成一个服务器实例

图上可知simple_server中还有一个`ServerHandler`模块 , 它继承于handlers模块中的`SimpleHandler` , 继承体系如下

```python
#        +-------------+
#        | BaseHandler |  
#        +-------------+
#               ↓
#       +----------------+
#       | SimpleHandler  |
#       +----------------+
#               ↓
#       +---------------+
#       | ServerHandler |
#       +---------------+
```

该模块主要完成的功能如下 : 

- 启动服务器
- 模块用户请求
- 处理用户请求

执行`simple_server.py`时内容如下

```python
httpd = make_server('', 8000, demo_app)
sa = httpd.socket.getsockname()
print "Serving HTTP on", sa[0], "port", sa[1], "..."

# M: webbrowser provides a high-level interface to allow displaying Web-based documents 
# to users. Under most circumstances
import webbrowser
webbrowser.open('http://localhost:8000/xyz?abc')

httpd.handle_request()  # serve one request, then exit
```

### demo_app  🍀

```python
demo_app(environ, start_response)
'''
参数说明:
environ:为一个字典
start_response:为一个可调用函数
return:返回一个可迭代对象
另外demo_app中会调用start_response函数
'''
def demo_app(environ,start_response):
    from StringIO import StringIO
    stdout = StringIO()
    print >> stdout, "Hello world!"
    print >> stdout
    h = environ.items()
    h.sort()
    for k,v in h:
        print >> stdout, k,'=',`v`
    start_response("200 OK", [('Content-Type','text/plain')])
    return [stdout.getvalue()]
```

### make_server  🍀

```python
def make_server(host, port, app, server_class=WSGIServer, handler_class=WSGIRequestHandler)
'''
参数说明:
host:主机名
port:端口号
server_class:生成server实例时所使用的基类,默认为WSGIServer
handler_class:用于处理请求的handler类,默认为WSGIRequestHandler
'''
def make_server(host, port, app, server_class=WSGIServer, handler_class=WSGIRequestHandler):
    '''引用no_1y的注释,文尾有详细链接'''
    # no_1y: -> HTTPServer.__init__
    #    -> TCPServer.__init__
    #       -> TCPServer.server_bind
    #           -> TCPServer.socket.bind
    #       -> TCPServer.server_activate
    #           -> TCPServer.socket.listen
    server = server_class((host, port), handler_class)
    # no_1y: conresponding to WSGIRequestHandler.handle()
    #        -> handler.run(self.server.get_app())
    server.set_app(app)
    return server
"""
server_class为WSGIServer,生成时会沿着继承方向到达最底层的TCPServer,并完成对socket的绑定和监听
set_app设置了app,它会在handler_class的handle函数中被取出来,交给handler的run函数执行
"""
```

## util  🍀

这个模块提供了用于处理WSGI环境的各种实用函数 , WSGI环境是一个包含在PEP 3333中描述的HTTP请求变量的字典

CLASSES

```python
builtins.object
	FileWrapper
class FileWrapper(builtins.object):
    """
    将文件类对象转换为迭代器的包装器
    """
```

FUNCTIONS

```python
application_uri(environ)
	"""返回应用程序的基本URI"""
guess_scheme(environ)
	"""返回一个猜测wsgi.url_scheme是否是http或https"""
request_uri(environ, include_query=True)
	"""返回完整的请求URI,包括任意的查询字符串"""
setup_testing_defaults(environ)
	"""用于设置虚拟环境的服务器和应用程序,目的是使WSGI的单元测试更加容易"""
shift_path_info(environ)
	"""将一个名称从PATH_INFO转移到SCRIPT_NAME,并返回它,如果在pathinfo中没有其他路径段，则返回None"""
```

util思维导图

![util](http://oux34p43l.bkt.clouddn.com/util.bmp)

## validate  🍀

在创建新的WSGI应用程序对象 , 框架 , 服务器或中间件时 , 使用wsgiref.validate验证新代码的一致性是很有用的

这个模块提供了一个函数 , 它创建了WSGI应用程序对象 , 它可以验证WSGI服务器或网关和WSGI应用程序对象之间的通信 , 从而检查双方是否符合协议的一致性

简单的说就是检查你对WSGI的实现是否满足标准

思维导图如下

![validate](http://oux34p43l.bkt.clouddn.com/validate.png)

本文主要参考http://blog.csdn.net/on_1y/article/details/18818081

思维导图来自https://github.com/minixalpha/SourceLearning/tree/master/wsgiref-0.1.2
