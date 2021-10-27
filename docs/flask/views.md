# Flask - 源码之视图








<extoc></extoc>

## 介绍

在 Flask 请求处理流程中 , 视图的调用是由 `dispatch_request()` 方法来控制的 

如果我们使用 FBV 的方式 , 由于请求方法是由我们定义条件语句控制的 , 所以 `dispatch_request()` 可以直接使用 , 但是如果我们像 Django 那样来使用 , 那么我们就需要重写 `dispatch_request() ` 了 , 不过在 Flask 中 , 已经有相关的类帮我们实现了

在 `flask.views.py` 中已经帮我们实现了 CBV , 我们可以继承他们来使用

```python
class View(object):
    """
    使用该类必须重写dispatch_reqeust方法,
    该类中有一个decorators属性,可以放入一些装饰器,
    装饰器将会自动装饰在视图上
    """
    pass
class MethodViewType(type):
    """
    该类为MethodView类的元类,它决定了视图的methods属性
    """
    pass
class MethodView(with_metaclass(MethodViewType, View)):
    """
    为我们已经实现了dispatch_request方法,我们可以直接使用
    """
    pass

```

## View

```python
class View(object):
    methods = None

    provide_automatic_options = None

    # 视图装饰器有关
    decorators = ()

    def dispatch_request(self):
        """
        子类必须继承
        """
        raise NotImplementedError()

    @classmethod
    def as_view(cls, name, *class_args, **class_kwargs):
        """
        将类转换成视图
        """
        def view(*args, **kwargs):
            # 实例化视图类
            self = view.view_class(*class_args, **class_kwargs)
            # 通过dispatch_request方法来控制类中方法的调用
            return self.dispatch_request(*args, **kwargs)

        if cls.decorators:
            view.__name__ = name
            view.__module__ = cls.__module__
            for decorator in cls.decorators:
                view = decorator(view)

        view.view_class = cls
        view.__name__ = name
        view.__doc__ = cls.__doc__
        view.__module__ = cls.__module__
        view.methods = cls.methods
        view.provide_automatic_options = cls.provide_automatic_options
        return view
```

实例

```python
from flask import Flask, request, render_template
from flask.views import View

app = Flask(__name__)


class BaseView(View):
    def get_template_name(self):
        raise NotImplementedError

    def render_template(self, context):
        return render_template(self.get_template_name(), **context)

    def dispatch_request(self):
        if request.method != "GET":
            return "UNSUPPORTED!"

        context = {'users': self.get_users()}
        return self.render_template(context)


class UserView(BaseView):
    def get_template_name(self):
        return 'user.html'

    def get_users(self):
        return [{
            'username': 'Lyon',
            'avatar': 'https://github.com/lyonyang/blogs/blob/master/assets/avatar/one.jpg'
        }]


app.add_url_rule('/users', view_func=UserView.as_view('userview'))

if __name__ == '__main__':
    app.run()
```

## MethodViewType

```python
class MethodViewType(type):
    """Metaclass for :class:`MethodView` that determines what methods the view
    defines.
    """

    def __init__(cls, name, bases, d):
        super(MethodViewType, cls).__init__(name, bases, d)
        # d为视图参数的字典
        # MethodView使用该元类时,会将空字典传入d
        if 'methods' not in d:
            methods = set()
            # http_method_funcs = frozenset(['get', 'post', 'head',
            #             'options','delete', 'put', 'trace', 'patch'])
            for key in http_method_funcs:
                # 如果视图中定义了属性方法,那么就在methods中添加对应属性
                if hasattr(cls, key):
                    methods.add(key.upper())

            if methods:
                cls.methods = methods
```

## MethodView

```python
class MethodView(with_metaclass(MethodViewType, View)):
    def dispatch_request(self, *args, **kwargs):
        meth = getattr(self, request.method.lower(), None)

        if meth is None and request.method == 'HEAD':
            meth = getattr(self, 'get', None)

        assert meth is not None, 'Unimplemented method %r' % request.method
        return meth(*args, **kwargs)
```

实例

```python
from flask import Flask, jsonify, abort, g
from flask.views import MethodView

app = Flask(__name__)


def user_required(f):
    def decorator(*args, **kwargs):
        if not g.user:
            abort(401)
        return f(*args, **kwargs)

    return decorator


class UserAPI(MethodView):
    decorators = [user_required,]

    def get(self):
        return jsonify({
            'username': 'Lyon',
            'avatar': 'https://github.com/lyonyang/blogs/blob/master/assets/avatar/one.jpg'
        })

    def post(self):
        return "UNSUPPORTED!"


app.add_url_rule('/user', view_func=UserAPI.as_view('userview'))

if __name__ == '__main__':
    app.run()
```