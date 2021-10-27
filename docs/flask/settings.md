# Flask - 源码之配置








<extoc></extoc>

## 介绍

Flask 中的配置主要使用 `flask/config.py` 中的两个对象 : `Config` , `ConfigAttribute` 

## Config

Config 是 dict 的子类 , 所以它的一些行为跟 dict 一样

```python
# 为了方便阅读,删除部分代码
# 删除部分以 ... 代表
class Config(dict):
    def __init__(self, root_path, defaults=None):
        dict.__init__(self, defaults or {})
        self.root_path = root_path

    def from_envvar(self, variable_name, silent=False):
        """
        更新配置,从环境变量中获取,等价于如下: 
        app.config.from_pyfile(os.environ['YOURAPPLICATION_SETTINGS'])
        """
        rv = os.environ.get(variable_name)
        ...
        return self.from_pyfile(rv, silent=silent)
        
    def from_pyfile(self, filename, silent=False):
        """
        更新配置,从文件中获取配置
        """
        filename = os.path.join(self.root_path, filename)
        # 获取一个module对象
        d = types.ModuleType('config')
        d.__file__ = filename
        try:
            with open(filename, mode='rb') as config_file:
                # 加载配置到,module对象的命名空间中
                exec(compile(config_file.read(), filename, 'exec'), d.__dict__)
        ...
        self.from_object(d)
        return True
    
    def from_object(self, obj):
        """
        更新配置,从对象中获取配置,官方实例:
            app.config.from_object('yourapplication.default_config')
            from yourapplication import default_config
            app.config.from_object(default_config)
        """
        if isinstance(obj, string_types):
            obj = import_string(obj)
        for key in dir(obj):
            # 获取配置模块的属性列表
            if key.isupper():
                self[key] = getattr(obj, key)
                
    def from_json(self, filename, silent=False):
        """
        更新配置,从json文件中获取配置
        类似于from_pyfile,但是返回方式不同
        """
        filename = os.path.join(self.root_path, filename)

        try:
            with open(filename) as json_file:
                obj = json.loads(json_file.read())
        ...
        return self.from_mapping(obj)
    
    def from_mapping(self, *mapping, **kwargs):
        """
        更新配置,
        """
        mappings = []
        if len(mapping) == 1:
            if hasattr(mapping[0], 'items'):
                mappings.append(mapping[0].items())
            else:
                mappings.append(mapping[0])
        ...
        mappings.append(kwargs.items())
        for mapping in mappings:
            for (key, value) in mapping:
                if key.isupper():
                    self[key] = value
        return True
    
    def get_namespace(self, namespace, lowercase=True, trim_namespace=True):
        """
        返回包含自己配置选项的字典
        namespace:配置的命名空间
        """

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, dict.__repr__(self))
```

因为它是字典的子类 , 所以你可以使用 `update()` 一次性更新多个配置

```python
app.config.update(
    DEBUG=True,
    SECRET_KEY='...'
)
```

关于通过 `from_object()` 方法来配置 , 你可以利用继承实现如下 :

```python
# configmodule.py
class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite://:memory:'

class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

# demo.py
app.config.from_object('configmodule.ProductionConfig')
```

## ConfigAttribute

该类的作用就是为config设置一些属性

```python
class ConfigAttribute(object):
    """
    将一个属性转接到Config,
    该类是一个描述器类,即实现了__get__方法的类,
    __get__的作用是,当通过另一个类的实例来访问该对象时,
    将会执行__get__方法,在Flask中如下:
    	class Flask(_PackageBoundObject):
    		testing = ConfigAttribute('TESTING')
    		self.config = self.make_config(instance_relative_config)
    		
    	application = Flask(__name__)
    	# 执行ConfigAttribute中的__get__方法
    	# 该配置在self.config中已被设置
    	application.testing
    """

    def __init__(self, name, get_converter=None):
        self.__name__ = name
        self.get_converter = get_converter

    def __get__(self, obj, type=None):
        """
        obj:即Flask对象
        """
        if obj is None:
            return self
        rv = obj.config[self.__name__]
        if self.get_converter is not None:
            rv = self.get_converter(rv)
        return rv

    def __set__(self, obj, value):
        obj.config[self.__name__] = value
```

## defaults_config

接下来我们看看关于 Flask 的一些默认的设置 , 首先是 Flask 对象中的 `defaults_config` , 它是一个 `ImmutableDict` 对象

`ImmutableDict` 是 werkzeug 中特意构造的一个数据类型 , 不可变字典

```python
default_config = ImmutableDict({
    'ENV':                                  None,   # 由helpers.get_env()获取,默认为production
    
    # 是否启用调试模式
    'DEBUG':                                None,   # 由helpers.get_debug_flag()获取,默认为True
    
    # 是否启用测试模式
    'TESTING':                              False,
    
    # 是否显示启用异常传播
    'PROPAGATE_EXCEPTIONS':                 None,   # 当 TESTING 或 DEBUG 为真时,总是开启的
    
    'PRESERVE_CONTEXT_ON_EXCEPTION':        None,   # 缺省情况下,如果应用在调试模式下运行,
                                                    # 那么请求环境在发生异常时不会被弹出,
                                                    # 以方便调试器内省数据,
                                                    # 可以通过这个配置来禁止这样做,
                                                    # 还可以使用这个配置强制不执行调试,
                                                    # 这样可能有助于调试生产应用(风险大)
    # 密钥
    'SECRET_KEY':                           None,
    
    # 持久化会话的存活时间
    'PERMANENT_SESSION_LIFETIME':           timedelta(days=31),
    
    # 开关x-sendfile
    'USE_X_SENDFILE':                       False,
    
    # 服务器的名称和端口,用于支持子域
    'SERVER_NAME':                          None,
    
    # 应用的路径
    'APPLICATION_ROOT':                     '/',
    
    # 会话cookie的名称
    'SESSION_COOKIE_NAME':                  'session',
    
    # 会话cookie的域
    'SESSION_COOKIE_DOMAIN':                None,
    
    # 会话cookie的路径
    'SESSION_COOKIE_PATH':                  None,
    
    # cookie的httponly标志
    'SESSION_COOKIE_HTTPONLY':              True,
    
    # 设置cookie的安全标志
    'SESSION_COOKIE_SECURE':                False,
    
    # cookie是否使用SameSite属性
    'SESSION_COOKIE_SAMESITE':              None,
    
    # 是否刷新请求
    'SESSION_REFRESH_EACH_REQUEST':         True,
    
    # 拒绝内容长度超过该值的请求,单位为字节
    'MAX_CONTENT_LENGTH':                   None,
    
    # 默认缓存控制的最大期限
    'SEND_FILE_MAX_AGE_DEFAULT':            timedelta(hours=12),
    
    # 反馈坏请求异常
    'TRAP_BAD_REQUEST_ERRORS':              None,
    
    # 是否执行HTTP异常处理
    'TRAP_HTTP_EXCEPTIONS':                 False,
    
    'EXPLAIN_TEMPLATE_LOADING':             False,
    
    # url模式方案
    'PREFERRED_URL_SCHEME':                 'http',
    
    # 是否把对象编码为ASCII
    'JSON_AS_ASCII':                        True,
    
    # 是否按键值排序JSON对象
    'JSON_SORT_KEYS':                       True,
    
    # jsonify响应是否完美打印
    'JSONIFY_PRETTYPRINT_REGULAR':          False,
    
    # json类型
    'JSONIFY_MIMETYPE':                     'application/json',
    
    # 自动重载模板
    'TEMPLATES_AUTO_RELOAD':                None,
    
    # 最大cookie尺寸
    'MAX_COOKIE_SIZE': 4093,
})
```
Flask 对象默认配置 : 

```python
# 静态文静路径
static_url_path=None,
# 静态文件夹
static_folder='static',
static_host=None,
host_matching=False,
subdomain_matching=False,
template_folder='templates',
instance_path=None,
instance_relative_config=False,
root_path=None
```

## 配置加载

那么了解了 `config.py` 中的内容后 , 我们应该想的是 , Flask 到底是如何去加载的

首先在我们实例化 Flask 对象 , 有这么一个操作 : 

```python
# instance_relative_config默认为False
self.config = self.make_config(instance_relative_config)
```

这个 `make_config` 就是加载配置了

```python
    def make_config(self, instance_relative=False):
        # root_path在Flask的基类中已经被设置,就是当前的根目录
        # root_path = get_root_path(self.import_name)
        root_path = self.root_path
        if instance_relative:
            root_path = self.instance_path
        # 这里self.defaults_config在上一小节已经详细说明了
        defaults = dict(self.default_config)
        defaults['ENV'] = get_env()
        defaults['DEBUG'] = get_debug_flag()
        # 返回一个Config对象,即Config(root_path, defaults)
        return self.config_class(root_path, defaults)
```

更多的配置需要在相关应用上介绍