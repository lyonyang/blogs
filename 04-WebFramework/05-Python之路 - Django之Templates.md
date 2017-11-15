# Python之路 - Django之Template
<!-- TOC -->

- [Python之路 - Django之Template](#python之路---django之template)
    - [介绍  🍀](#介绍--🍀)
    - [配置  🍀](#配置--🍀)
    - [用法  🍀](#用法--🍀)
    - [内置后端  🍀](#内置后端--🍀)
        - [DjangoTemplates  🍀](#djangotemplates--🍀)
        - [Jinja2  🍀](#jinja2--🍀)

<!-- /TOC -->
## 介绍  🍀

作为一个Web框架 , Django需要一个方便的方式来动态生成HTML , 最常见的方法就是依赖于模板

Django项目可以配置一个或多个模板引擎 , Django为其自己的模板系统提供内置后端 , 也就是我们所说的Djanog模板语言 , 目前最流行的就是`Jinja2` 

由于历史原因 , 对模板引擎的一般支持和Django模板语言的实现都存在于`django.template` 命名空间中

**warning** : 模板系统对于不受信任的模板作者是不安全的 , 如 : 一个站点不应允许其用户提供自己的模板 , 因为模板作者可以执行诸如XSS攻击和访问可能包含敏感信息的模板变量的属性

当我们使用`Pycharm` 创建一个项目时 , 会自动会我们创建一个`templates` 文件夹 , 就是用来存放我们的模板文件的

## 配置  🍀

模板引擎使用`TEMPLATES` 设置进行配置 , 位于`settings.py` 中 , 如下 : 

```python
TEMPLATES = [
    {
        # 实现Django模板后端API的模板引擎类的Python路径,内置后端是
        # ajango.template.bakcends.django.DjangoTemplates
        # django.template.backends.jinja2.Jinja2
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        
        # 根据搜索顺序定义引擎应该查找模板源文件的目录列表
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        
        # 告诉引擎是否应该在已安装的应用程序中查找模板,每个后端都为其模板应存储在其中的应用程序内的子目录定义一个常规名称
        'APP_DIRS': True,
        
        # 包含后端特定的设置
        'OPTIONS': {
            # 当模板被请求呈现时,可用于填充上下文的可调用Python路经列表
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

## 用法  🍀

在`django.template.loader` 模块中定义了两个函数来加载模板

```python
def get_template(template_name, using=None):
    """
    Loads and returns a template for the given name.

    Raises TemplateDoesNotExist if no such template exists.
    """
    # return:The exact type of the return value depends on the backend that loaded the template. Each backend has its own Template class.
    # How templates are searched and loaded depends on each engine’s backend and configuration.
    # using:engine's NAME,restrict search to a specific template engine
def select_template(template_name_list, using=None):
    """
    Loads and returns a template for one of the given names.

    Tries names in order and returns the first template found.

    Raises TemplateDoesNotExist if no such template exists.
    """
    # select_template() is just like get_template(), except it takes a list of template names. It tries each name in order and returns the first template that exists.
```

Template对象通过调用`get_template()` 和`select_template()` 生成 , 但是必须提供一个`render()` 方法 , render如下 : 

```python
Template.render(context=None, request=None)
	"""使用给定的上下文呈现此模板
	context:是一个dict,默认引擎将使用空的上下文呈现模板
	request:是一个HttpRequest,引擎必须在模板中使用它以及CSRF令牌"""
```

一个搜索算法🌰

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            '/home/html/example.com',
            '/home/html/default',
        ],
    },
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [
            '/home/html/jinja2',
        ],
    },
]
```

如果我们调用`get_template('story_detail.html')` , 那么Django将会寻找以下文件 : 

- /home/html/example.com/story_detail.html ('django' engine)
- /home/html/default/story_detail.html ('django' engine)
- /home/html/jinja2/story_detail.html ('jinja2' engine)

如果调用`select_template(['story_253_detail.html','story_detail.html'])`  , 则Django将会寻找如下文件 : 

- /home/html/example.com/story\_253_detail.html ('django' engine)
- /home/html/default/story\_253\_detail.html ('django' engine)
- /home/html/jinja2/story\_253\_detail.html ('jinja2' engine) 
- /home/html/example.com/story_detail.html ('django' engine)
- /home/html/default/story_detail.html ('django' engine)
- /home/html/jinja2/story_detail.html ('jinja2' engine)

当Django找到一个存在的模板时 , 就会停止寻找

为了减少加载和渲染模板的重复性 , Django提供了一个快捷方式来自动化这个过程 , 即`django.template.loader` 中的`render_to_string()` , 具体如下 : 

```python
def render_to_string(template_name, context=None, request=None, using=None):
    """
    Loads a template and renders it with a context. Returns a string.

    template_name may be a string or a list of strings.
    
    template_name:要加载和渲染的模板名称,如果传入模板名称列表,则Django将会使用select_template()
    context:一个用于呈现模板上下文的dict
    request:一个可选的HttpRequest
    using:一个可选的模板引擎名称,搜索模板将被限制在该引擎
    """
# render_to_string()相当于调用get_template()后并调用其render()方法
```

用法示例 : 

```python
from django.template.loader import render_to_string
rendered = render_to_string('my_template.html', {'foo': 'bar'})
```

**engines**

模板引擎可以使用`django.template.engines`  : 

```python
from django.template import engines
# The lookup key — 'django' in this example — is the engine’s NAME.
django_engine = engines['django']
template = django_engine.from_string("Hello {{ name }}!")
```

## 内置后端  🍀

### DjangoTemplates  🍀

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        
        # DjangoTemplate引擎会在已安装应用程序的模板子目录中寻找模板,这个通用名称是为了向后兼容而保留的
        'APP_DIRS': True,
        
        # 可选配置
        'OPTIONS': {
            
            # 控制是否启动HTML自动转义
            'autoescape':True
            
            # 当模板被请求呈现时,用于填充上下文的可调用Python路径列表.这些可调用对象将请求对象作为参数,并返回一个合并到上下文的列表
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            
            # 打开模板调试模式,默认为DEBUG设置的值
            'debug':True
            
            # 模板加载器的Python路径列表
            'loaders':[
            	(
                	'django.template.loaders.filesystem.Loader',
                	[os.path.join(BASE_DIR, 'templates')],
            	),
        	],    
            
			# 如果变量不存在,模板系统会默认插入引擎string_if_invalid的值
            'string_if_invalid':''
            
            # 用于读取磁盘上的模板文件的字符集,默认utf-8
            'file_charset':'utf-8'
            
            # 一个标签和模板标签模块路径的字典,用于注册模板引擎
            'libraries':{ 
                'myapp_tags':'path.to.myapp.tags',
                'admin.urls':'django.contrib.admin.templatetags.admin_urls',
            },
            
            # 一个要添加到内置插件的模板标签模块
            'builtins': ['myapp.builtins'],
        },
    },
]
```

### Jinja2  🍀

安装

```cmd
pip install Jinja2
```

将`BACKEND` 设置为`django.template.backends.jinja2.Jinja2` 

最重要的OPTIONS条目是`environment`  , 这是一个Python路径 , 可以返回一个Jinja2环境 , 默认为`jinja2.Environment` 

Django添加了几个与Jinja2不同的默认值 :

- `'autoescape'` : True 
- `'loader'` : a loader configured for [`DIRS`](https://docs.djangoproject.com/en/1.11/ref/settings/#std:setting-TEMPLATES-DIRS) and [`APP_DIRS`](https://docs.djangoproject.com/en/1.11/ref/settings/#std:setting-TEMPLATES-APP_DIRS)
- `'auto_reload'` : settings.DEBUG
- `'undefined'` : DebugUndefined if settings.DEBUG else Undefined

Jinja2也接受如DjangoTemplate的`OPTIONS` : 

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': []
        'APP_DIRS': True,       
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

自定义后端 : https://docs.djangoproject.com/en/1.11/topics/templates/#custom-backends

更多: https://docs.djangoproject.com/en/1.11/topics/templates/

origin API : https://docs.djangoproject.com/en/1.11/topics/templates/#origin-api-and-3rd-party-integration

这一篇中主要与模板系统的配置有关 , 所以该篇内容当做一个铺垫 , 下篇将继续对模板系统进行整理

另一篇从技术层面讲解的官方文档 : https://docs.djangoproject.com/en/1.11/ref/templates/api/