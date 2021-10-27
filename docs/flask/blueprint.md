# Flask - 源码之蓝图








<extoc></extoc>

## 介绍

首先 , 我们得说说蓝图的作用

蓝图 `(Blueprint)` 实现了应用的**模块化** , 使用蓝图让应用层次清晰 , 开发者可以更容易的开发和维护项目 , 蓝图通常作用于相同的 URL 前缀 , 比如`/user/:id` , `/user/profile` 这样的地址都以 `/user` 开头 , 那么他们就可以放在一个模块中

## 构建蓝图

我们从示例开始 : 

`myapplication/simple_page.py`

```python
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

# Blueprint类与Flask类一样,都继承了_PackageBoundObject
# Blueprint相当于Flask的子应用
simple_page = Blueprint('simple_page', __name__,
                        template_folder='templates')

@simple_page.route('/', defaults={'page': 'index'})
@simple_page.route('/<page>')
def show(page):
    try:
        return render_template('pages/%s.html' % page)
    except TemplateNotFound:
        abort(404)
```

`Blueprint` 类与 `Flask` 类非常相似 , 它就像是一个应用 , 上面代码中 , 首先实例化一个应用对象 , 虽然绑定路由与视图函数 , 然而它与 Flask 的不同之处就在于 , `route` 完成的操作并没有真的完成路由的添加 , 而是完成了一个函数的添加 , 我们看看源码 : 

```python
def route(self, rule, **options):
    def decorator(f):
        # 与Flask类中的route方法不同的是,蓝图中将视图函数的函数名作为endpoint
        endpoint = options.pop("endpoint", f.__name__)
        self.add_url_rule(rule, endpoint, f, **options)
        return f
    return decorator
```

`Blueprint.add_url_rule()` 如下 : 

```python
def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
    if endpoint:
        assert '.' not in endpoint, "Blueprint endpoints should not contain dots"
    if view_func and hasattr(view_func, '__name__'):
        assert '.' not in view_func.__name__, "Blueprint view function name should not contain dots"
    # 传入一个匿名函数,该函数将在蓝图注册时被调用
    self.record(lambda s:
        s.add_url_rule(rule, endpoint, view_func, **options))
```

`Blueprint.record()` 如下 : 

```python
def record(self, func):
    if self._got_registered_once and self.warn_on_modifications:
        from warnings import warn
        warn(Warning('The blueprint was already registered once '
                     'but is getting modified now.  These changes '
                     'will not show up.'))
    # 将函数追加到deferred_functions中
    self.deferred_functions.append(func)
```

至此 , 我们已经完成了一个蓝图的构建 , 但是此时路由并没有注册 , 它仅仅将注册路由的函数放入 `deferred_functions` 中 , 等待蓝图注册时被调用

## 注册蓝图

现在我们需要把构建好的蓝图注册到我们的应用中 , 如下 : 

```python
from flask import Flask
from myapplication.simple_page import simple_page

app = Flask(__name__)
app.register_blueprint(simple_page)
```

`Flask.register_blueprint()` 如下 : 

```python
def register_blueprint(self, blueprint, **options):
    first_registration = False

    if blueprint.name in self.blueprints:
        assert self.blueprints[blueprint.name] is blueprint, (
            'A name collision occurred between blueprints %r and %r. Both'
            ' share the same name "%s". Blueprints that are created on the'
            ' fly need unique names.' % (
                blueprint, self.blueprints[blueprint.name], blueprint.name
            )
        )
    else:
        # 注册蓝图到Flask应用对象
        self.blueprints[blueprint.name] = blueprint
        self._blueprint_order.append(blueprint)
        first_registration = True
    # 将回调在构建蓝图实例时的延迟函数,即deferred_functions中的函数
    # 函数为:lambda s: s.add_url_rule(rule, endpoint, view_func, **options)
    # s为flask.blueprints.BlueprintSetupState实例
    blueprint.register(self, options, first_registration)
```

`Blueprint.register()` 具体如下 : 

```python
def register(self, app, options, first_registration=False):
    self._got_registered_once = True
    # 创建一个flask.blueprints.BlueprintSetupState实例
    state = self.make_setup_state(app, options, first_registration)

    if self.has_static_folder:
        state.add_url_rule(
            self.static_url_path + '/<path:filename>',
            view_func=self.send_static_file, endpoint='static'
        )

    for deferred in self.deferred_functions:
        # 调用flask.blueprints.BlueprintSetupState实例的add_url_rule方法
        deferred(state)
```

`flask.blueprints.BlueprintSetupState.add_url_rule()` 如下 : 

```python
def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
    if self.url_prefix is not None:
        if rule:
            rule = '/'.join((
                self.url_prefix.rstrip('/'), rule.lstrip('/')))
        else:
            rule = self.url_prefix
    options.setdefault('subdomain', self.subdomain)
    if endpoint is None:
        endpoint = _endpoint_from_view_func(view_func)
    defaults = self.url_defaults
    if 'defaults' in options:
        defaults = dict(defaults, **options.pop('defaults'))
    # 使用flask.Flask.add_url_rule方法
    # 第二个参数为endpoint参数,为蓝图名称.视图名称,simple_page.show
    self.app.add_url_rule(rule, '%s.%s' % (self.blueprint.name, endpoint),
                          view_func, defaults=defaults, **options)
```

如果是使用蓝图注册路由 , 那么第一个路由同样是设置静态文件路由 , 在 `flask.blueprints.Blueprint.register()` 中可见如下内容 : 

```python
if self.has_static_folder:
    state.add_url_rule(
        self.static_url_path + '/<path:filename>',
        view_func=self.send_static_file, endpoint='static'
    )
```

该蓝图注册到应用时 , 路由注册规则如下 : 

```shell
# 可以在flask.Flask.add_url_rule中
# line 1215:self.url_map.add(rule)下添加一行输出代码:
#	  print(rule.__repr()) 
# 随后启动应用,就能得到如下信息
# 我们也可以输出flas.Flask.view_functions属性查看绑定的视图函数,这里就不说明了

<Rule '/static/<filename>' (HEAD, OPTIONS, GET) -> static>,
<Rule '/<page>' (HEAD, OPTIONS, GET) -> simple_page.show>,
<Rule '/' (HEAD, OPTIONS, GET) -> simple_page.show>
```

蓝图还可以在不同的位置挂载 : 

```python
app.register_blueprint(simple_page, url_prefix='/pages')
```

生成规则如下 : 

```shell
<Rule '/static/<filename>' (HEAD, OPTIONS, GET) -> static>,
<Rule '/pages/<page>' (HEAD, OPTIONS, GET) -> simple_page.show>,
<Rule '/pages/' (HEAD, OPTIONS, GET) -> simple_page.show>
```

## 蓝图资源

蓝图也可以提供资源 , 有时候你会只为他提供的资源而引入一个蓝图 

### 蓝图资源文件夹

我们可以通过访问 `Blueprint` 对象的 `root_path` 属性来访问蓝图资源文件夹 : 

```python
>>> simple_page.root_path
'/Users/username/TestProject/myapplication'
```

并且你可以使用 `open_response()` 函数快速获取文件资源 : 

```python
with simple_page.open_resource('static/style.css') as f:
    code = f.read()
```

### 静态文件

与 `Flask` 一样 , `Blueprint` 可以通过 `static_folder` 关键字参数提供一个指向文件系统上文件夹的路径 , 这可以是一个绝对路径 , 也可以是相对于蓝图文件夹的相对路径 : 

```python
admin = Blueprint('admin', __name__, static_folder='static')
```

### 模板

同样的 , 蓝图也提供模板 : 

```python
admin = Blueprint('admin', __name__, template_folder='templates')
```

总而言之 , 蓝图相当于 `Flask` 应用实例下的 `"Flask"` 应用实例 ("子应用") , 它能将你的项目理想化

对于 `Blueprint` 对象中的方法 , 你不妨看看 , 也许有你想要的功能