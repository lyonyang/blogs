# Flask - 扩展

## 介绍  🍀

Flask 扩展多方面地扩充了 Flask 功能 , 例如它们添加了数据库支持以及其他常见任务

Flask 扩展的生态非常繁荣 , Flask 扩展被列出在 [Flask Extension Registry](http://flask.pocoo.org/extensions/) 上并且我们可以直接用 `easy_install` 或者 `pip` 进行下载安装

下面介绍一些常用的扩展以及它们的使用方式

## Flask-Script  🍀

Django 提供了如下管理命令 : 

```shell
$ python manage.py startapp
$ python manage.py runserver
```

Flask 也可以通过 `Flask-Script` 添加运行服务器 , 设置数据库 , 定制 shell 等功能的命令

安装

```shell
$ pip install flask-script
```

创建 py 文件 `manage.py` , 内容如下 : 

```python
from flask_script import Manager


app = Flask(__name__)
# configure your app

# Manager将跟踪从命令行调用的所有命令和句柄
manager = Manager(app)

if __name__ == "__main__":
    manager.run()
```

随后我们在当前目录下 : 

```shell
>python manage.py --help
# 看来默认有shell和runserver
usage: manage.py [-?] {shell,runserver} ...

positional arguments:
  {shell,runserver}
    shell               Runs a Python shell inside Flask application context.
    runserver           Runs the Flask development server i.e. app.run()

optional arguments:
  -?, --help            show this help message and exit
```

### 创建命令  🍀

接下来我们需要创建我们自己的命令 , 创建命令有三种方式 : 

- 通过实现 `Command` 类
- 使用 `@command` 装饰器
- 使用 `@option` 装饰器

通过 `Command` 类 : 

```python
from flask_script import Command

class Hello(Command):
    "prints hello world"

    def run(self):
        print("hello world")
        
# 将创建的命令添加到Manager实例
manager.add_command('hello', Hello())
```

通过 `@command` 装饰器 : 

```python
@manager.command
def lyon():
    "Just say lyon"
    print("lyon")
```

通过 `@option` 装饰器 : 

```python
# @option用于读复杂命令进行控制
@manager.option('-n', '--name', help='Your name')
def send(name):
    "send name of you"
    print("hello", name)
```

我们再次执行 `python manage.py --help` 

```shell
>python manage.py --help
usage: manage.py [-?] {hello,lyon,send,shell,runserver} ...

positional arguments:
  {hello,lyon,send,shell,runserver}
    hello               prints hello world
    lyon                Just say lyon
    send                send name of you
    shell               Runs a Python shell inside Flask application context.
    runserver           Runs the Flask development server i.e. app.run()

optional arguments:
  -?, --help            show this help message and exit
```

### 添加参数  🍀

大多数命令都采用了在命令行中传递许多命名参数或者位置参数 , 为了方便这一点 , 我们可以使用 Command 类中的 `option_list` 属性 : 

```python
from flask_script import Command, Manager, Option

class Hello(Command):

    option_list = (
        Option('--name', '-n', dest='name'),
    )

    def run(self, name):
        print "hello %s" % name
```

或者定义 `get_options` 方法 : 

```python
class Hello(Command):

    def __init__(self, default_name='Joe'):
        self.default_name=default_name

    def get_options(self):
        return [
            Option('-n', '--name', dest='name', default=self.default_name),
        ]

    def run(self, name):
        print "hello",  name
```

如果使用的是 `@command` 装饰器 , 那么我们直接加在被装饰函数中就可以了 

```python
@manager.command
def verify(verified=False):
    """
    Checks if verified
    """
    print "VERIFIED?", "YES" if verified else "NO"
```

结果如下 : 

```shell
> python manage.py verify
VERIFIED? NO

> python manage.py verify -v
VERIFIED? YES

> python manage.py verify --verified
VERIFIED? YES
```

其次就是创建命令时使用的 `@option` 了 , 也可添加任意多个选项 : 

```python
@manager.option('-n', '--name', dest='name', default='joe')
@manager.option('-u', '--url', dest='url', default=None)
def hello(name, url):
    if url is None:
        print "hello", name
    else:
        print "hello", name, "from", url
```

Documentation : [Read docs @ pythonhosted.org](http://pythonhosted.org/Flask-Script/)

## Flask-DebugToolbar  🍀

Django 有非常知名的 Django-DebugToolbar , 而 Flask 也有对应的替代工具 Flask-DebugToolbar

它会在浏览器上添加右边栏 , 可以快速查看环境变量 , 上下文内容 , 方便调试

安装

```shell
$ pip install flask-debugtoolbar
```

使用前提 : debug 必须药设置为 True

示例

```python
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'a secret key'

toolbar = DebugToolbarExtension(app)

@app.route('/')
def hello():
    return '<body></body>'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9000, debug=app.debug)
```

接下来使用浏览器访问 `http://127.0.0.1:9000/` 就可以看到有右边栏了

Flask-DebugToolbar 内置了很多面板 , 如下 : 

| 面板         | 功能                                                         |
| ------------ | ------------------------------------------------------------ |
| Versions     | 列出安装的包的版本                                           |
| Time         | 显示处理当前请求花费的时间的信息                             |
| HTTP Headers | 显示当前请求的 HTTP 头信息                                   |
| Request Vars | 显示当前请求带的变量 , 包含请求参数 , cookie 信息等          |
| Config       | 显示 app.config 的变量值                                     |
| Templates    | 显示模板请求参数信息                                         |
| SQLAlchemy   | 显示当前请求下的 SQL , 需要设置 SQLALCHEMY_RECORD_QUERIES 为 True |
| Logging      | 显示请求过程中的日志信息                                     |
| Route List   | 列出 Flask 的路由规则                                        |
| Profiler     | 对当前请求添加性能分析 , 默认是关闭的 , 需要点击红色的钩 , 让它变成绿色 |

Documentation : [Read docs @ github.com](https://github.com/mgood/flask-debugtoolbar) 

## Flask-Migrate  🍀

使用关系型数据库时 , 修改数据库模型和更新数据库这样的工作时有发生 , 而且很重要

SQLAlchemy 作者为此开发了迁移框架 Alembic , Flask-Migrate 就是基于 Alembic 做了轻量级封装 , 并集成到 Flask-Script 中 , 所有操作都通过 Flask-Script 命令完成 , 它能跟踪数据库结构的变化 , 把变化的部分应用到数据库中

安装

```shell
$ pip install Flask-Migrate
```

示例

`manage.py`

```python
from flask import Flask
from flask-script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    
manager = Manager(app)
manager.add_command("db",MigrateCommand)

if __name__ == '__main__':
    manager.run()
```

执行命令

```shell
# 初始化
>python manage.py db init
Python35\site-packages\flask_sqlalchemy\__init__.py:794: FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to True or False to suppress this warning.
  'SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and '
Creating directory demo\migrations ... done
Creating directory demo\migrations\versions ... done
Generating demo\migrations\alembic.ini ... done
Generating demo\migrations\env.py ... done
Generating demo\migrations\README ... done
Generating demo\migrations\script.py.mako ... done
Please edit configuration/connection/logging settings in 'demo\\migrations\\alembic.ini' before proceeding.

# 创建迁移脚本
>python manage.py db migrate
Python35\site-packages\flask_sqlalchemy\__init__.py:794: FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to True or False to suppress this warning.
  'SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and '
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'user'
Generating demo\migrations\versions\d121144e719e_.py ... done
```

更新数据库

```shell
>python manage.py db upgrade
Python35\site-packages\flask_sqlalchemy\__init__.py:794: FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to True or False to suppress this warning.
  'SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and '
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> d121144e719e, empty message
```

Documentation : [Read docs @ pythonhosted.org](http://pythonhosted.org/Flask-Migrate/)

## Flask-RESTful  🍀

Flask-RESTful 帮助你快速创建 REST API 服务

安装

```shell
$ pip install flask-restful
```

示例

`config.py` 

```python
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
UPLOAD_FOLDER = '/tmp/permdir'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'a secret key'
```

`manage.py`

```python
from flask import Flask, request
from flask_restful import Resource, Api, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
api = Api(app)
db = SQLAlchemy(app)

parser = reqparse.RequestParser()
parser.add_argument('admin', type=bool, help='Use super manager mode',
                    default=False)

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'address': fields.String
}


class User(db.Model):
    __tablename__ = 'restful_user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(128), nullable=True)


db.create_all()


class UserResource(Resource):
    @marshal_with(resource_fields)
    def get(self, name):
        user = User.query.filter_by(name=name).first()
        return user

    def put(self, name):
        address = request.form.get('address', '')
        user = User(name=name, address=address)
        db.session.add(user)
        db.session.commit()
        return {'ok': 0}, 201

    def delete(self, name):
        args = parser.parse_args()
        is_admin = args['admin']
        if not is_admin:
            return {'error': 'You do not have permissions'}
        user = User.query.filter_by(name=name).first()
        db.session.delete(user)
        db.session.commit()
        return {'ok': 0}


api.add_resource(UserResource, '/users/<name>')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9000, debug=True)
```

利用 `http` 工具在命令行访问 : 

```shell
# 添加数据
>http -f put http://localhost:9000/users/Lyon address='Beijing'
HTTP/1.0 201 CREATED
Content-Length: 16
Content-Type: application/json
Date: Thu, 28 Jun 2018 12:00:18 GMT
Server: Werkzeug/0.12.2 Python/3.5.2

{
    "ok": 0
}

# 删除数据
>http -f delete http://localhost:9000/users/Lyon --print b
{
    "error": "You do not have permissions"
}

# 以管理员身份删除数据
>http -f delete http://localhost:9000/users/Lyon admin=1 --print b
{
    "ok": 0
}

# 查询数据
>http -f get http://localhost:9000/users/Lyon --print b
{
    "address": null,
    "id": 0,
    "name": null
}
```

Documentation : [Read docs @ flask-restful.readthedocs.org](https://flask-restful.readthedocs.org/) 

## Flask-Admin  🍀

有了 Flask-Admin 的帮助 , 我们用很少的代码就能像 Django 那样实现一个管理后台 , 它支持 Pymongo , Peewee , Mongoengine , SQLAlchemy 等数据库使用方法 , 自带了基于模型的数据管理 , 文件管理 , Redis 的页面命令行等类型后台 , 尤其是模型的管理后台 , 甚至可以细粒度定制字段级别的权限

安装

```shell
$ pip install Flask-Admin
```

示例 

[Flask 示例](http://examples.flask-admin.org/) 

Documentation : [Read docs @ flask-admin.readthedocs.org](http://flask-admin.readthedocs.org/en/latest/index.html) 