# Python之路 - Django之Settings

## 介绍  🍀

Django项目的配置信息在Django项目建立时就已经为我们创建完成 , 也就是目录下的`settings.py` 文件

由 `python manage.py startproject` 命令生成 , 每个设置都有默认值 , 这些默认值定义在django/conf/global_settings.py中

如需查看修改了哪些设置 , 可使用命令`python manage.py diffsettings` 显示当前settings文件与django默认设置的不同之处

本章配置文件根据Django 1.11x 描述 , 并仅为初始基本配置

## SECRET_KEY  🍀

`SECRET_KEY` 为一个特定的Django安装密钥 , 用于提供加密签名

使用`django-admin startproject` 命令时为每一个项目随机生成 , 如果`SECRET_KEY` 没有设置 , Django将拒绝启动

## DEBUG  🍀

`DEBUG` 配置默认为`True` , 在此状态下会暴露出一些错误信息或者配置信息以方便调试 , 但是上线后应该将其关掉 , 防止配置信息或者敏感错误信息泄漏

```python
DEBUG = False
```

## ALLOWED_HOSTS  🍀

`ALLOWED_HOSTS` 是为了限定请求中的host值 , 以防止黑客构造包来发送请求 , 只有在列表中的host才能访问 , 建议不要使用通配符去配置

注意 : 当DEBUG设置为False时 , 该配置必须配置 , 否则会抛出异常

默认配置为空 , 配置模板如下 : 

```python
ALLOWED_HOSTS = [
    '.example.com',   # 允许是域名或子域名
    '.example.com.',  # 也允许是FQDN或子域名
]
```

## INSTALLED_APPS  🍀

`INSTALLED_APPS` 是一个列表 , 里面是应用中需要加载的自带或者自定义的app包路经列表 , 所以我们每创建一个应用都需要在这里进行添加 , 如下 : 

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
]
```

## MIDDLEWARE  🍀

`MIDDLEWARE` 是一个列表 , 里面为要使用的中间件列表 , 默认如下 : 

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

## ROOT_URLCONF  🍀

`ROOT_URLCONF` 为一个字符串 , 代表你的根URLconf的模块名 , 如下 : 

```python
ROOT_URLCONF = 'mydjango.urls'
```

## TEMPLATES  🍀

`TEMPLATES` 为一个包含所有模板引擎设置的列表 , 列表中的每一项都是一个包含单个引擎选项的字典 , 如下 : 

```python
TEMPLATES = [
    {
        # 要使用的模板后端,内置的模板后端如下,还有django.template.backends.jinja2.Jinja2,
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        
        # 在搜索顺序中引擎应该寻找模板源文件的目录,即绝对路径
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        
        # 设置引擎是否应该在安装的应用程序中查找模板源文件
        'APP_DIRS': True,
        
        # 额外的参数传递给模板后端,可用参数因模板后端而异
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

## WSGI_APPLICATION  🍀

`WSGI_APPLICATION` 为Django内置服务器 (如runserver) 的应用程序对象的完整Python路径

`django-admin startproject` 执行会创建一个简单的`wsgi.py` 应用程序 , 并将此设置指向该应用程序

```python
WSGI_APPLICATION = 'mydjango.wsgi.application'
```

## DATABASES  🍀

`DATABASES` 为一个包含所有数据库配置的字典 , 它是一个嵌套的字典 , 其内容将数据库别名映射到包含单个数据库选项的字典

数据库设置必须配置一个默认数据库 , 还可以指定任意数量的附加数据库

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'USER': 'mydatabaseuser',
        'PASSWORD': 'mypassword',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

## AUTH_PASSWORD_VALIDATORS  🍀

`AUTH_PASSWORD_VALIDATORS` 是一个列表 , 用于检查用户密码强度验证程序的列表

```python
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

## LANGUAGE_CODE  🍀

`LANGEUAGE_CODE` 是一个字符串 , 默认为 `'en-us'` , 即一个表示安装的语言代码的字符串 , 为标准语言ID格式 , 美国英语是 `'en-us'` 

`USE_I18N`  必须激活此设置才能起作用

```python
LANGUAGE_CODE = 'en-us'
```

## TIME_ZONE  🍀

`TIME_ZONE`  表示此安装时区的字符串 , 新版本默认为`'UTC'`  , 这不一定是服务器的时区 , 因为一个服务器可以服务多个Django支持的站点 , 每个站点都有一个单独的时区设置

如果`USE_TZ` 是`False`  , 这是Django存储所有日期时间的时区 , 如果为`True`  , 这是Django会使用显示模板日期时间的默认时区 

```python
TIME_ZONE = 'UTC'
```

## USE_I18N  🍀

`USE_I18N` 为一个bool值 , 指定Django的翻译系统是否应该启动 , 如果设置为`False`  , Django将进行一些优化 , 以避免加载翻译器

```python
USE_I18N = True
```

## USE_L10N  🍀

`USE_L10N` 为一个bool值 , 它指定了默认的数据的本地化格式是否可以在默认情况下使用 , 如果为`True`  , Django将用当前的语言环境来显示数字和日期

```python
USE_L10N = True
```

## USE_TZ  🍀

`USE_TZ` 为一个bool值 , 指定日期时间默认情况下是否是时区感知的 , 如果设置为`True`  , Django将在内部使用时区感知的日期时间

```python
USE_TZ = True
```

## STATIC_URL  🍀

`STATIC_URL` 为一个引用名 , 引用位于`STATIC_ROOT`的静态文件 , `STATIC_ROOT` 如下 : 

```python
STATICFILES_DIRS = (
        os.path.join(BASE_DIR,'static'), # 实际名,即实际文件夹的名字
    )
```

注意 : 引用时 , 只能按照引用名找 , 不能按实际名

静态文件 (static) 主要指 , CSS , JavaScript , Images这样的文件 

更多管理静态文件 : https://docs.djangoproject.com/en/1.11/howto/static-files/

更多settings相关 : https://docs.djangoproject.com/en/1.11/ref/settings/
