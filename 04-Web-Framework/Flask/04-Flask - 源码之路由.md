# Flask - 源码之路由

## 介绍  🍀

在分析 Flask 的请求处理流程中 , 已经碰到了一些路由相关的代码了 , 但是并未深入 , 现在就来看看吧

## 添加路由  🍀

通常我们使用 Flask 中的装饰器 `route` 来完成路由注册 , 实际上 , 它也仅仅是一个中介 , 方便我们使用 ; 本质上它只是帮我们调用了 Flask 对象中的 `add_url_rule` 方法 , 如下 : 

```python
def route(self, rule, **options):
    def decorator(f):
        endpoint = options.pop('endpoint', None)
        self.add_url_rule(rule, endpoint, f, **options)
        return f
    return decorator
```

也就是说我们可以这样来注册路由 : 

```python
app = Flask(__name__)
def index():
    pass
app.add_url_rule('/', 'index', index)
```

而 `add_url_rule` 中 , 我们截取重要部分来分析 : 

```python
def add_url_rule(self, rule, endpoint=None, view_func=None,
                 provide_automatic_options=None, **options):
    if endpoint is None:
        endpoint = _endpoint_from_view_func(view_func)
    options['endpoint'] = endpoint
    methods = options.pop('methods', None)

    # if the methods are not given and the view_func object knows its
    # methods we can use that instead.  If neither exists, we go with
    # a tuple of only ``GET`` as default.
    if methods is None:
        # 此处添加GET,在后续会加入OPTIONS和HEAD
        methods = getattr(view_func, 'methods', None) or ('GET',)
    if isinstance(methods, string_types):
        raise TypeError('Allowed methods have to be iterables of strings, '
                        'for example: @app.route(..., methods=["POST"])')
    methods = set(item.upper() for item in methods)

    # Methods that should always be added
    required_methods = set(getattr(view_func, 'required_methods', ()))

    # starting with Flask 0.8 the view_func object can disable and
    # force-enable the automatic options handling.
    if provide_automatic_options is None:
        provide_automatic_options = getattr(view_func,
            'provide_automatic_options', None)

    if provide_automatic_options is None:
        if 'OPTIONS' not in methods:
            provide_automatic_options = True
            required_methods.add('OPTIONS')
        else:
            provide_automatic_options = False

    # Add the required methods now.
    # 此处会将required_methods中的OPTIONS加入methods中
    methods |= required_methods
    # 实例化Rule对象,并不会对rule做出改变
    # 实例化过程中会将 HEAD 加入到methods中
    rule = self.url_rule_class(rule, methods=methods, **options)
    rule.provide_automatic_options = provide_automatic_options
    
    # self.url_map = Map()
    # 所有的路由将全部存储在Map对象中,并且路由的转换工作也将在该对象中完成
    self.url_map.add(rule)
    if view_func is not None:
        old_func = self.view_functions.get(endpoint)
        if old_func is not None and old_func != view_func:
            raise AssertionError('View function mapping is overwriting an '
                                 'existing endpoint function: %s' % endpoint)
        # 将视图函数加入view_functions中,默认为{}
        self.view_functions[endpoint] = view_func
```

## 绑定路由  🍀

我们已经知道 , 路由的转换是利用`Map` 对象来实现的 , `self.url_map.add(rule)` 源码如下 : 

```python
def add(self, rulefactory):
    # Rule.get_rules()是一个生成器,返回Rule实例
    for rule in rulefactory.get_rules(self):
        # Rule.bind()会将url绑定到Map对象,也就是这里self
        # 并且会创建一个正则表达式,其规则将会从Map对象中获取
        rule.bind(self)
        # 将Rule对象加入_rules列表中
        self._rules.append(rule)
        # 加入_rules_by_endpoint中
        self._rules_by_endpoint.setdefault(rule.endpoint, []).append(rule)
    self._remap = True
```

在上面的 `add` 方法中 , 最重要的就是 `rule.bind(self)` , 我们看看细节部分 : 

```python
def bind(self, map, rebind=False):
    if self.map is not None and not rebind:
        raise RuntimeError('url rule %r already bound to map %r' %
                           (self, self.map))
    # 为Rule对象添加map属性
    self.map = map
    if self.strict_slashes is None:
        # map.strict_slashes = True
        self.strict_slashes = map.strict_slashes
    if self.subdomain is None:
        # map.default_subdomain = ''
        self.subdomain = map.default_subdomain
    # 完成正则表达式并存储它
    self.compile()
```

`self.compile()` 如下 : 

```python
def compile(self):
    """Compiles the regular expression and stores it."""
    assert self.map is not None, 'rule not bound'

    if self.map.host_matching:
        domain_rule = self.host or ''
    else:
        domain_rule = self.subdomain or ''

    self._trace = []
    self._converters = {}
    self._static_weights = []
    self._argument_weights = []
    regex_parts = []

    def _build_regex(rule):
        """
        构建正则表达式,并放入regex_parts中
        """
        index = 0
        # parse_rule(rule)会返回一个生成器,迭代时返回(converter, arguments, variable)
        for converter, arguments, variable in parse_rule(rule):
            # 只有使用静态规则时,converter才为None
            if converter is None:
                regex_parts.append(re.escape(variable))
                self._trace.append((False, variable))
                for part in variable.split('/'):
                    if part:
                        self._static_weights.append((index, -len(part)))
            else:
                if arguments:
                    c_args, c_kwargs = parse_converter_args(arguments)
                else:
                    c_args = ()
                    c_kwargs = {}
                # 获取转换器
                convobj = self.get_converter(
                    variable, converter, c_args, c_kwargs)
                regex_parts.append('(?P<%s>%s)' % (variable, convobj.regex))
                self._converters[variable] = convobj
                self._trace.append((True, variable))
                self._argument_weights.append(convobj.weight)
                self.arguments.add(str(variable))
            index = index + 1
    _build_regex(domain_rule)
    regex_parts.append('\\|')
    self._trace.append((False, '|'))
    _build_regex(self.is_leaf and self.rule or self.rule.rstrip('/'))
    if not self.is_leaf:
        self._trace.append((False, '/'))
    if self.build_only:
        return
    regex = r'^%s%s$' % (
        u''.join(regex_parts),
        (not self.is_leaf or not self.strict_slashes) and
        '(?<!/)(?P<__suffix__>/?)' or ''
    )
    self._regex = re.compile(regex, re.UNICODE)
```

## 转换器  🍀

在上面这段代码中 , 主要流程为 : 根据 `url` 中的信息 , 解析使用什么转换器 , 以及含有的变量等 , 再利用转换器的规则 , 生成路由放入 `regex_parts` 中 ; `Map` 对象中提供了一些默认的转换器 : 

```python
# Map对象构造函数上方
default_converters = ImmutableDict(DEFAULT_CONVERTERS)

DEFAULT_CONVERTERS = {
    'default':          UnicodeConverter,
    'string':           UnicodeConverter,
    'any':              AnyConverter,
    'path':             PathConverter,
    'int':              IntegerConverter,
    'float':            FloatConverter,
    'uuid':             UUIDConverter,
}
```

这些转换器都是通过继承 `BaseConverter` 类实现的

```python
class BaseConverter(object):

    """Base class for all converters."""
    regex = '[^/]+'
    weight = 100

    def __init__(self, map):
        self.map = map

    def to_python(self, value):
        """
        路由匹配时,匹配成功后传递给视图函数中参数的值
        """
        return value

    def to_url(self, value):
        """
        使用url_for反向生成URL时,传递的参数经过该方法处理,返回值用于生成URL的参数
        """
        # 用指定的编码对value进行编码
        return url_quote(value, charset=self.map.charset)
```

以 `UnicodeConverter` 为例 : 

```python
class UnicodeConverter(BaseConverter):
    def __init__(self, map, minlength=1, maxlength=None, length=None):
        BaseConverter.__init__(self, map)
        if length is not None:
            length = '{%d}' % int(length)
        else:
            if maxlength is None:
                maxlength = ''
            else:
                maxlength = int(maxlength)
            length = '{%s,%s}' % (
                int(minlength),
                maxlength
            )
        self.regex = '[^/]' + length
        
        
# Rule('/pages/<page>'),
# Rule('/<string(length=2):lang_code>')

@app.route('/<string(length=2):lang_code>')
def string_view(lang_code):
    return lang_code
```

## 自定义转换器  🍀

在 Flask 默认的转换器中 , 并没有支持正则的 , 如果我们需要像 Django 一样 , 支持正则 , 那就需要我们自己来增加这个规则了 , 也就是自定义一个转换器

```python
from flask import Flask,url_for
from werkzeug.routing import BaseConverter

app = Flask(__name__)
class RegexConverter(BaseConverter):
    """
    正则转换器
    """
    def __init__(self, map, regex):
        super(RegexConverter, self).__init__(map)
        self.regex = regex

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return super(RegexConverter, self).to_url(value)

# 添加到Map对象的converters中
app.url_map.converters['regex'] = RegexConverter

@app.route('/index/<regex("\d+"):nid>')
def index(nid):
    return "Index"
```

## 反向生成URL  🍀

在 Django 中 , 利用 `reverse()` 来反向生成 URL , 而在 Flask 中 , 也提供了一个函数可以反向生成 URL : `url_for()`

```python
def url_for(endpoint, **values):
    # 获取应用上下文
    appctx = _app_ctx_stack.top
    # 获取请求上下文
    reqctx = _request_ctx_stack.top

    if appctx is None:
        raise RuntimeError(
            'Attempted to generate a URL without the application context being'
            ' pushed. This has to be executed when application context is'
            ' available.'
        )

    # If request specific information is available we have some extra
    # features that support "relative" URLs.
    if reqctx is not None:
        # 请求上下文对象的url适配器
        url_adapter = reqctx.url_adapter
        blueprint_name = request.blueprint

        if endpoint[:1] == '.':
            if blueprint_name is not None:
                endpoint = blueprint_name + endpoint
            else:
                endpoint = endpoint[1:]

        external = values.pop('_external', False)

    # Otherwise go with the url adapter from the appctx and make
    # the URLs external by default.
    else:
        # 应用上下文适配器
        url_adapter = appctx.url_adapter

        if url_adapter is None:
            raise RuntimeError(
                'Application was not able to create a URL adapter for request'
                ' independent URL generation. You might be able to fix this by'
                ' setting the SERVER_NAME config variable.'
            )

        external = values.pop('_external', True)

    anchor = values.pop('_anchor', None)
    method = values.pop('_method', None)
    scheme = values.pop('_scheme', None)
    appctx.app.inject_url_defaults(endpoint, values)

    # This is not the best way to deal with this but currently the
    # underlying Werkzeug router does not support overriding the scheme on
    # a per build call basis.
    old_scheme = None
    if scheme is not None:
        if not external:
            raise ValueError('When specifying _scheme, _external must be True')
        old_scheme = url_adapter.url_scheme
        url_adapter.url_scheme = scheme

    try:
        try:
            # 通过适配器构建url
            rv = url_adapter.build(endpoint, values, method=method,
                                   force_external=external)
        finally:
            if old_scheme is not None:
                url_adapter.url_scheme = old_scheme
    except BuildError as error:
        # We need to inject the values again so that the app callback can
        # deal with that sort of stuff.
        values['_external'] = external
        values['_anchor'] = anchor
        values['_method'] = method
        values['_scheme'] = scheme
        return appctx.app.handle_url_build_error(error, endpoint, values)

    if anchor is not None:
        rv += '#' + url_quote(anchor)
    return rv
```

## 补充  🍀

关于路由默认的 `methods` 属性 , `Rule` 对象实例化时 , 会完成3次添加 : 

1. 执行 `add_url_rule` , 添加 `GET` 属性
2. 通过 `required_methods` 与 `methods` 并集的结果 , 添加 `OPTIONS` 
3. 实例化 `Rule` 对象时 , 添加 `HEAD` 属性

在 Flask 对象进行实例化时 , 会首先将静态文件路由进行添加

```python
if self.has_static_folder:
    assert bool(static_host) == host_matching, 'Invalid static_host/host_matching combination'
    self.add_url_rule(
        self.static_url_path + '/<path:filename>',
        endpoint='static',
        host=static_host,
        view_func=self.send_static_file
    )
```

自动添加的静态文件规则如下 : 

```python
<Rule '/static/<filename>' (HEAD, OPTIONS, GET) -> static>,
```