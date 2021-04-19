# Flask - 源码简要说明


<extoc></extoc>

## 介绍  🍀

内容概况

```shell
flask
├── json
│   ├── __init__.py
│   └── tag.py
├── __init__.py
├── __main__.py      
├── _compat.py       # 实现关于Python版本兼容性的配置
├── app.py           # 实现WSGI应用程序对象,即Flask
├── blueprints.py    # 蓝图
├── cli.py           # 实现简单的命令行应用程序
├── config.py        # 实现与配置相关的对象
├── ctx.py           # 实现上下文相关的对象
├── debughelpers.py  # debug模式相关
├── globals.py       # 定义了所有的全局对象
├── helpers.py       
├── logging.py       
├── sessions.py
├── signals.py       # 基于blinker的信号
├── templating.py
├── testing.py
├── views.py         # 提供了类似于Djando的CBV
└── wrappers.py      # 实现了WSGI包装器,即request和response
```

## 阅读指引  🍀

本目录下为 Flask 源码阅读相关 , 读者应该对 WSGI 和 socketserver 有一定的了解 , 因为在某些部分这可能成为阻碍 , 相对而言 , Flask 的源码比 Django 要简单得多 , 因为 Django 过于庞大 , 并且耦合度高

如果您有一定的 Web 框架基础 , 对于 Flask 框架的学习可能会变得简单 , 您可以通过阅读源码来获得更多的灵感 , 该目录文章为本人学习交流所撰 , 欢迎交流

如果您没有 Web 框架基础 , 那么您不妨通过 Flask 官方的文档来进行学习 , 链接在此 : [Flask官方文档](http://flask.pocoo.org/docs/1.0/) ; [中文文档](http://www.pythondoc.com/flask/index.html) , 该文档翻译不一定准确 , 但是可以借鉴

更多 Flask 相关中文翻译 : http://www.pythondoc.com/