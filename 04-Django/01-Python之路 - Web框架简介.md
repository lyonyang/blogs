# Python之路 - Web框架简介

## 介绍  🍀

框架 (Framework) , 特指为解决一个开发性问题而设计的具有一定约束性的支撑结构 , 使用框架可以帮助我们快速开发特定的系统 , 简单说就是使用别人搭好的舞台 , 你来做表演

对于Web应用 , 本质其实就是一个socket服务端 , 而我们使用的浏览器就是一个socket客户端 , 如下 : 

```python
# 服务端
import socket
def handle_request(client):
    """处理请求函数"""
    buf = client.recv(1024)
    print(buf)
    client.send(b"HTTP/1.1 200 OK\r\n\r\n")
    client.send(b"<h1>Hello,Lyon</h1>")
def main():
    """主函数"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 8000))
    sock.listen(5)
    while True:
        connection, address = sock.accept()
        # 连接成功后直接处理请求
        handle_request(connection)
        connection.close()
if __name__ == '__main__':
    main()
'''
说明:
执行该脚本后,用浏览器(客户端)访问 127.0.0.1:8000
连接成功后服务端直接应答以及发送
<h1>Hello,Lyon</h1>
于是网页就直接显示出了Hello,Lyon的标题
'''
```

上述通过socket实现了其本质 , 而对于真是开发中的Python Web程序来说 , 一般会分为两部分 : 服务器程序和应用程序

服务器程序负责对socket服务器进行封装 , 并在请求到来时 , 对请求的各种数据进行整理 , 如上述代码

应用程序负责具体的逻辑处理

为了方便应用程序的开发 , 就出现了众多的Web框架 , 常见的Python Web框架如下 : 

- Django : 全能型Web框架
- Flask : 一个轻量级的Web框架
- web.py : 一个小巧的Web框架
- Bottle : 和Flask类似的Web框架
- Tornado : Facebook的开源异步Web框架

不同的框架有不同的开发方式 , 但是无论如何 , 开发出的应用程序都要和服务器程序配合 , 才能为用户提供服务

也就是说框架和Web服务器之间进行通信 , 那么首先就需要两者互相支持 , 所以为了使Web服务器能够匹配多个不同的Web框架 , 就需要设立一个标准 , 在Python中这个标准就是WSGI

## WSGI  🍀

WSGI : `WSGI (Web Server Gateway Interface , Web服务器网关接口)` 

它定义了使用Python编写Web应用与Web服务端之间的接口格式 , 实现了Web应用与Web服务器间的解藕

Python标准库提供的独立WSGI服务器称为**wsgiref** , 所以我们可以使用wsgiref模块开发一个自己的Web框架

关于wsgiref模块的更多内容请可以阅读< [Python之路 - wsgiref模块](https://lyonyang.github.io/blogs/01-Python/07-Standard-Library/Python%E4%B9%8B%E8%B7%AF%20-%20wsgiref%E6%A8%A1%E5%9D%97.html) > , 这也是完成下面内容的前提

## 自定义Web框架  🍀

### 框架  🍀

通过Python标准库提供的wsgiref模块开发

```python
# 从simple_server模块中导入make_server函数
from wsgiref.simple_server import make_server
# 处理函数
def index():
    return 'index'
# 处理函数
def login():
    return 'login'

# 路由管理函数
def routers():
    urlpatterns = (
        ('/index/',index),
        ('/login/',login),
    )
    return urlpatterns

# 该函数就是simple_server模块中的demo_app函数,即创建一个app
def RunServer(environ, start_response):
    """
    符合WSGI标准的一个HTTP处理函数
    environ:一个包含所有HTTP请求信息的dict对象
    start_response:一个发送HTTP响应的函数
    注:该函数会在内部调用start_response函数
    """
    
    # start_response接收两个参数,一个是HTTP响应码,如下"200 OK";另一个是一组list表示的HTTP Header,每个Header用一个包含两个str的tuple表示
    start_response('200 OK', [('Content-Type', 'text/html')])
    # 获取路径信息,即url
    url = environ['PATH_INFO']
    urlpatterns = routers()
    func = None
    # 查看路径是否存在
    for item in urlpatterns:
        if item[0] == url:
            func = item[1]
            break
    if func:
        return func()
    else:
        return '404 not found'
if __name__ == '__main__':
    # 创建一个WSGI服务器
    httpd = make_server('', 8000, RunServer)
    print("Serving HTTP on port 8000...")
    # 开始监听HTTP请求
    httpd.serve_forever()
```

### 模板引擎  🍀

在上一步中 , 对于处理函数`login`以及`index`仅仅做了最简单的处理 , 在现实的Web请求中一般会返回一个复杂的符合HTML规则的字符串 , 所以我们一般会将要返回给用户HTML写在指定文件中 , 然后再返回 , 进一步优化如下 : 

```python
# 通过文件处理发送HTML信息
def index():
    # return 'index'
    f = open('index.html')
    data = f.read()
    return data
def login():
    # return 'login'
    f = open('login.html')
    data = f.read()
    return data
```

如上我们实现了静态的页面处理 , 要使其能够给用户返回动态内容 , 我们有两种方法 : 

- 自定义一套特殊的语法 , 进行替换
- 使用开源工具jinja2 , 遵循其指定语法

*Jinja2介绍* : Jinja2是Python下一个被广泛应用的模板引擎 , 他的设计思想来源于Django的模板引擎 , 并扩展了其语法和一系列强大的功能 , 他基于unicode并能在python2.4之后的版本运行 , 包括python3

于是我们可以再进一步

```python
from jinja2 import Template
def index():
    # return 'index'
    # template = Template('Hello {{ name }}!')
    # result = template.render(name='John Doe')
    f = open('index.html')
    result = f.read()
    template = Template(result)
    data = template.render(name='John Doe', user_list=['Lyon', 'Kenneth'])
    return data.encode('utf-8')
def login():
    # return 'login'
    f = open('login.html')
    data = f.read()
    return data
```

以上就完成了一个最简单的Web框架

## MVC和MTV  🍀

> **MVC**

MVC (Model View Controller , 模型-视图-控制器) 是一种Web架构的模式 , 它把业务逻辑 , 模型数据 , 用户界面分离开来 , 让开发者将数据与表现解藕 , 前端工程师可以只改页面效果部分而不用接触后端代码 , DBA(数据库管理员) 可以重新命名数据表并且只需要更改一个地方 , 无序从一大堆文件中进行查找和替换

MVC模式甚至还可以提高代码复用能力 , 现在MVC模式依然是主流

MVC三要素 : 

- Model表示应用程序核心(比如数据库记录列表) , 是应用程序中用于处理应用程序数据逻辑的部分 , 通常模型对象负责在数据库中存取数据
- View显示数据(数据库记录) , 是应用程序中处理数据显示的部分 , 通常视图是依据模型数据创建的
- Controller处理输入(写入数据库记录) , 是应用程序中处理用户交互的部分 , 通常控制器负责从视图读取数据 , 控制用户输入 , 并向模型发送数据

MVC模式同时提供了对HTML , CSS和JavaScript的完全控制

MVC的特点是通信单向的 : 

1. 浏览器发送请求
2. Contorller和Model交互获取数据
3. Contorller调用View
4. View渲染数据返回

> **MTV**

在Python的世界中 , 基本都使用了MVC的变种MTV (Model Templates View , 模型-模板-视图)

MTV三要素 : 

1. Model , 和MVC的Model一样 , 处理与数据相关的所有事务 : 如何存取 , 如何确认有效性 , 包含哪些行为以及数据之间的关系等
2. Template , 处理与表现相关的决定 : 如何在页面或其他类型文档中进行显示出来
3. View , 处理业务逻辑 , 视图就是一个特定URL的回调函数 , 回调函数中描述数据 : 从Model取出对应的数据 , 调用相关的模板 . 它就是Contorller要调用的那个用来做Model和View之间的沟通函数 , 从而完成控制

两者的区别在于 : MVC中的View的目的是「呈现哪一个数据」 , 而MTV的View的目的是「数据如何呈现」

下一篇就开始学习Django啦
