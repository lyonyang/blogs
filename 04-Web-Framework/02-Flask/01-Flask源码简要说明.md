# Flask源码简要说明

## 介绍

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
