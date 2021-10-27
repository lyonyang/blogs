# Django - 源码之url








<extoc></extoc>

##  介绍

上一篇对中间件的源码进行了阅读 , 我们知道了 , 当请求到来时 , 首先会应用请求中间件 , 随后就是进行URL匹配 , 去寻找对应的视图了 

在上一篇的代码中 , 实际上我们已经见过了 , 那么这一篇就要对其进行详细的分析了

说先引出其入口

```python
def _get_response(self, request):
	"""
	Resolve and call the view, then apply view, exception, and
	template_response middleware. This method is everything that happens
	inside the request/response middleware.
	"""
	response = None
    
	# 加载settings.ROOT_URLCONF,即根目录中的urls.py
	# 并返回一个 **RegexURLResolver** 对象
	if hasattr(request, 'urlconf'):
		# 一般情况下,在默认request中没有urlconf属性
		urlconf = request.urlconf
		set_urlconf(urlconf)
		resolver = get_resolver(urlconf)
	else:
		resolver = get_resolver()
	# **进行url匹配,查找相关视图**
	resolver_match = resolver.resolve(request.path_info)
	
	# 分解视图函数以及参数
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
```

由上可知 , 在`_get_response()` 中构造了RegexURLResolver对象 , 随后调用该对象的 `resolve()` 方法 , 最后从返回值中获取视图函数与参数

## resolve

```python
def resolve(self, path):
	path = force_text(path)  # path may be a reverse_lazy object
	tried = []
    
    # regex是一个类变量
    # regex = LocaleRegexDescriptor()
    # LocaleRegexDescriptor是一个描述器类,当执行self.regex时会执行__get__方法
    # self.regex返回一个经过编译的正则表达式
	match = self.regex.search(path)
	if match:
         # 去除前缀mysite.url
		new_path = path[match.end():]
         # 遍历urlpatterns
		for pattern in self.url_patterns:
			try:
                 # pattern为url()返回的RegexURLResolver(For include)或RegexURLPattern
				sub_match = pattern.resolve(new_path)
			except Resolver404 as e:
				sub_tried = e.args[0].get('tried')
				if sub_tried is not None:
					tried.extend([pattern] + t for t in sub_tried)
				else:
					tried.append([pattern])
			else:
                  # 未出现异常执行
				if sub_match:
					# Merge captured arguments in match with submatch
                      # 获取对应参数
					sub_match_dict = dict(match.groupdict(), **self.default_kwargs)
					sub_match_dict.update(sub_match.kwargs)

					# If there are *any* named groups, ignore all non-named groups.
					# Otherwise, pass all non-named arguments as positional arguments.
					sub_match_args = sub_match.args
					if not sub_match_dict:
						sub_match_args = match.groups() + sub_match.args

					return ResolverMatch(
						sub_match.func,
						sub_match_args,
						sub_match_dict,
						sub_match.url_name,
						[self.app_name] + sub_match.app_names,
						[self.namespace] + sub_match.namespaces,
					)
				tried.append([pattern])
		raise Resolver404({'tried': tried, 'path': new_path})
	raise Resolver404({'path': path})
```

获取的 `urlpatterns` 中 , `url()` 函数会返回两种对象 , 源码可见 : 

```python
def url(regex, view, kwargs=None, name=None):
    if isinstance(view, (list, tuple)):
        # 第一种,view为一个元组,元组中包含一个列表和元组
        # 这是在进行路由分发时发生的,也就是使用include
        # For include(...) processing.
        urlconf_module, app_name, namespace = view
        return RegexURLResolver(regex, urlconf_module, kwargs, app_name=app_name, namespace=namespace)
    elif callable(view):
        # 第二种,view为一个函数
        return RegexURLPattern(regex, view, kwargs, name)
    else:
        raise TypeError('view must be a callable or a list/tuple in the case of include().')
```

首先我们来看看第二种 , 也就是view为函数的情况 , 其返回一个RegexURLPattern对象

## RegexURLPattern

```python
class RegexURLPattern(LocaleRegexProvider):
    def __init__(self, regex, callback, default_args=None, name=None):
        LocaleRegexProvider.__init__(self, regex)
        self.callback = callback  # the view
        self.default_args = default_args or {}
        self.name = name

   # 摘取如下部分
        
    def resolve(self, path):
        # 完成url解析
        match = self.regex.search(path)
        if match:
            # If there are any named groups, use those as kwargs, ignoring
            # non-named groups. Otherwise, pass all non-named arguments as
            # positional arguments.
            kwargs = match.groupdict()
            args = () if kwargs else match.groups()
            # In both cases, pass any extra_kwargs as **kwargs.
            kwargs.update(self.default_args)
            # ResolverMatch类中定义了__gititem__方法
            return ResolverMatch(self.callback, args, kwargs, self.name)
```

看看这个返回的`ResolverMatch` , 源码如下 : 

```python
class ResolverMatch(object):
    def __init__(self, func, args, kwargs, url_name=None, app_names=None, namespaces=None):
        # 分解出的视图函数
        self.func = func
        # 视图函数参数
        self.args = args
        self.kwargs = kwargs
        self.url_name = url_name

        # If a URLRegexResolver doesn't have a namespace or app_name, it passes
        # in an empty value.
        self.app_names = [x for x in app_names if x] if app_names else []
        self.app_name = ':'.join(self.app_names)
        self.namespaces = [x for x in namespaces if x] if namespaces else []
        self.namespace = ':'.join(self.namespaces)

        if not hasattr(func, '__name__'):
            # CBV
            # A class-based view
            self._func_path = '.'.join([func.__class__.__module__, func.__class__.__name__])
        else:
            # FBV
            # A function-based view
            self._func_path = '.'.join([func.__module__, func.__name__])

        view_path = url_name or self._func_path
        self.view_name = ':'.join(self.namespaces + [view_path])

    def __getitem__(self, index):
        # 通过解包即可依次获得视图函数与各参数
        return (self.func, self.args, self.kwargs)[index]
```

这就是最后在`_get_response()`中获取的结果了 , 对`ResolverMatch` 进行解包

接下来就是第二种情况了 , 也就是view为`include()` 返回的结果 , 它是一个元组 , 形式 : `(list,tuple)`

## include

首先我们需要弄清楚 , include返回的元组中到底有什么内容 , 其源码如下 : 

```python
def include(arg, namespace=None, app_name=None):
    # arg: 
    #	- six.string_types (PY3 : str)
    #	- tuple
    #	- list
    if app_name and not namespace:
        raise ValueError('Must specify a namespace if specifying app_name.')
    if app_name:
        warnings.warn(
            'The app_name argument to django.conf.urls.include() is deprecated. '
            'Set the app_name in the included URLconf instead.',
            RemovedInDjango20Warning, stacklevel=2
        )

    if isinstance(arg, tuple):
        # callable returning a namespace hint
        try:
            urlconf_module, app_name = arg
        except ValueError:
            if namespace:
                raise ImproperlyConfigured(
                    'Cannot override the namespace for a dynamic module that provides a namespace'
                )
            warnings.warn(
                'Passing a 3-tuple to django.conf.urls.include() is deprecated. '
                'Pass a 2-tuple containing the list of patterns and app_name, '
                'and provide the namespace argument to include() instead.',
                RemovedInDjango20Warning, stacklevel=2
            )
            # 获取urlconf模块,应用名,命名空间
            urlconf_module, app_name, namespace = arg
    else:
        # No namespace hint - use manually provided namespace
        urlconf_module = arg

    if isinstance(urlconf_module, six.string_types):
        # urlconf_module为字符串,导入该url模块
        urlconf_module = import_module(urlconf_module)
    # 获取内部的urlpatterns
    patterns = getattr(urlconf_module, 'urlpatterns', urlconf_module)
    # 获取app_name
    app_name = getattr(urlconf_module, 'app_name', app_name)
    if namespace and not app_name:
        warnings.warn(
            'Specifying a namespace in django.conf.urls.include() without '
            'providing an app_name is deprecated. Set the app_name attribute '
            'in the included module, or pass a 2-tuple containing the list of '
            'patterns and app_name instead.',
            RemovedInDjango20Warning, stacklevel=2
        )

    namespace = namespace or app_name

    # Make sure we can iterate through the patterns (without this, some
    # testcases will break).
    if isinstance(patterns, (list, tuple)):
        # list为分发的url
        for url_pattern in patterns:
            # Test if the LocaleRegexURLResolver is used within the include;
            # this should throw an error since this is not allowed!
            if isinstance(url_pattern, LocaleRegexURLResolver):
                raise ImproperlyConfigured(
                    'Using i18n_patterns in an included URLconf is not allowed.')
    # 返回一个元组
    return (urlconf_module, app_name, namespace)
```

include实现了路由分发 , 但是实际上 , 它就是在 `url()` 中又套了一层 `url()` , 在每一个urls中都必须有一个`urlpatterns`  , 通过一层一层的`urlpatterns` , 就可以实现路由分发了 

最后 , 如果我们不使用`include()` , 实际上也是可以实现路由分发的 : 

```python
# 版本一
urlpatterns = [
    url(r'^home/', (
        # 该列表即urlpatterns,可用函数替换掉
        [
            url(r'^index/', views.index),
            url(r'^login/', views.login),
            url(r'^register/', views.register),
        ],
        None, # app_name
        None  # namespace
    )),
]

# 版本二
def get_urlpatterns():
    urlpatterns = [
        url(r'^index/', views.index),
        url(r'^login/', views.login),
        url(r'^register/', views.register),
    ]
    return urlpatterns

urlpatterns = [
    url(r'^home/', (
        get_urlpatterns,
        None, # app_name
        None  # namespace
    )),
]
```

## 小结

在这一章关于URL的源码中 , 印象最深刻的还属 `__get__` 的使用 , 构造描述器类 ( `LocaleRegexDescriptor` )来完成需求 , 以及以解包的方式获取 `__gitItem__` 中的相关值 

`__get__` 示例

```python
class Descriptor:
    
    def __get__(self):
        print("Visit me and execute me.")

class Onwer:
    
    desc = Descriptor()

o = Onwer()
o.d
"""
执行结果:
Visit me and execute me.
"""
```

`__getitem__` 示例

```python
class Foo:
    
    def __getitem__(self, item):
        return ('lyon', 'kenneth', 'even')[item]
f = Foo()
lyon, kenneth, even = f
"""
执行结果:
lyon kenneth even
"""
```