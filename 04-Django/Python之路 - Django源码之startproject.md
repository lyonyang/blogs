# Python之路 - Django源码之startproject

## 介绍  🍀

django是Python中的一个Web框架 , 它的本质其实就是一个别人已经为我们写好了的 , Python第三方库

而我们使用它也是通过Python中的导入语句 , 将其导入后使用

我们看看django的文件系统

```python
>>> import django
>>> help(django)
Help on package django:

NAME
    django

PACKAGE CONTENTS
    __main__
    apps (package)
    conf (package)
    contrib (package)
    core (package)
    db (package)
    dispatch (package)
    forms (package)
    http (package)
    middleware (package)
    shortcuts
    template (package)
    templatetags (package)
    test (package)
    urls (package)
    utils (package)
    views (package)
```

文档树如下

```python
django
├── apps
├── bin
├── conf
├── contrib
├── core
├── db
├── dispatch
├── forms
├── http
├── middleware
├── templatetages
├── test
├── urls
├── utils
├── views
├── __init__.py
├── __main__.py
└── shortcuts.py
```

分析时 , 源码省略部分以pass带过

## 开始  🍀

在我们使用命令行安装django时 , 通常都会自动为我们添加一个环境变量 , 也就是`django/bin/django-admin.py`这个文件 , 我们可是在命令行输入`django-admin`命令来测试是否已经添加了环境变量

```shell
$ django-admin

Type 'django-admin help <subcommand>' for help on a specific subcommand.

Available subcommands:

[django]
    check
    compilemessages
    createcachetable
    dbshell
    diffsettings
    dumpdata
    flush
    inspectdb
    loaddata
    makemessages
    makemigrations
    migrate
    runserver
    sendtestemail
    shell
    showmigrations
    sqlflush
    sqlmigrate
    sqlsequencereset
    squashmigrations
    startapp
    startproject
    test
    testserver
Note that only Django core commands are listed as settings are not properly configured (error: Requested setting INSTALLED_APPS, but settings are not configured. You must either define the environment variable DJANGO_SETTINGS_MODULE or call settings.configure() before accessing settings.).
```

如果命令行输出以上信息 , 那么就说明环境变量已经添加 , 如果没有 , 那么你就得自己添加了 , 如何添加环境变量可以访问如下链接操作 : [www.baidu.com](www.baidu.com)

现在我们已经知道了django的入口 , 就是`django-admin.py` , 根据命令行的提示我们就可以开始创建我们的Django项目了

```shell
# 用法如下
$ django-admin startproject [-h] [--version] [-v {0,1,2,3}]
                                 [--settings SETTINGS]
                                 [--pythonpath PYTHONPATH] [--traceback]
                                 [--no-color] [--template TEMPLATE]
                                 [--extension EXTENSIONS] [--name FILES]
                                 name [directory]
```

实际上我们使用PyCharm时 , 创建django项目 , 其内部也是帮我们调用了这条命令 , 接下来我们应该看看`django-admin.py`中包含了什么信息了

`django/bin/django-admin.py` 

```python
#!/usr/bin/env python
from django.core import management

if __name__ == "__main__":
    management.execute_from_command_line()
```

在这个入口中 , 我们看到了django真正的入口 , 也就是在这个`management`里面 , 接下来我们看看我们在命令行输出的命令django是如何解析的

## startproject  🍀

以`django-admin startprojec`为例 , 首先我们切换到要存放项目的目录 , 然后在命令行输入一下命令

`````shell
$ django-admin startproject lyonyangproject  
`````

我们来看看这条命令到底是怎么执行的

毋庸置疑 , 创建我们的Django项目 , 将进行一些列复杂的加载工作 , 也就是整个项目所需要的配置等等的导入工作 , 我们将一层层的来观察这些动作

首先`django-admin.py`被执行 , 随后进入了`django/core/management/__init__.py`  , 我们简单提取关键步骤 , 如下图 :

![简单导入流程](http://oux34p43l.bkt.clouddn.com/简单导入流程.png)

有了这个图 , 那么文字说明就好说了 , 在`management.execute_from_command_line()` 执行之前 , 我们看看django做了些什么

- 导入apps , 执行了其中的`apps = Apps(installed_apps=None)`  , 这个apps实例暂时并没有真实的数据 , 它管理着一个存储安装应用的注册表 , 以及维护着一个与models的通道

- 导入settings , 执行`settings = LazySettings()` , 这一步至关重要 , 它所做的事情 , 都隐藏在其基类`LazyObject`中 , 因为`LazySettings()`是没有构造函数的 , 所以只能向它的父亲拿了

  ```python
  empty = object()

  class LazyObject(object):
      # 这个类的作用就是为了延迟实例化
      # Avoid infinite recursion when tracing __init__ (#19456).
      _wrapped = None

      def __init__(self):
          # Note: if a subclass overrides __init__(), it will likely need to
          # override __copy__() and __deepcopy__() as well.
          # 这里并未进行真正意义上的初始化,因为empty是一个空对象
          self._wrapped = empty
          
      ......

  class LazySettings(LazyObject):
      
  	def _setup(self, name=None):
  	"""
  	Load the settings module pointed to by the environment variable. This
  	is used the first time we need any settings at all, if the user has not
  	previously configured the settings manually.
  	"""
      
      # ENVIRONMENT_VARIABLE = "DJANGO_SETTINGS_MODULE"
      # 这个环境变量会在execute函数执行时设置成"[project].settings"
      # 我们的项目就是lyonyangproject.settings
  	settings_module = os.environ.get(ENVIRONMENT_VARIABLE)
  	if not settings_module:
  		desc = ("setting %s" % name) if name else "settings"
  		raise ImproperlyConfigured(
  			"Requested %s, but settings are not configured. "
  			"You must either define the environment variable %s "
  			"or call settings.configure() before accessing settings."
  			% (desc, ENVIRONMENT_VARIABLE))
          
  	# 此时一切就绪,完成真正的实例化
  	self._wrapped = Settings(settings_module)
      
      def __getattr__(self, name):
          # 这一步会在execute()中通过settings.INSTALLED_APPS激活
          """
          Return the value of a setting and cache it in self.__dict__.
          """
          if self._wrapped is empty:
              self._setup(name)
          val = getattr(self._wrapped, name)
          self.__dict__[name] = val
          return val
  ```

导入工作差不多是完成了 , 但是此时这个settings却没有真正初始化 , 我们继续往下观察

导入工作完成后 , 那么就开始执行了 , 也就是调用`execute_from_command_line()`函数了

`management/__init__.py`

```python
def execute_from_command_line(argv=None):
    """
    A simple method that runs a ManagementUtility.
    """
    
    # 实例化ManagementUtility
    utility = ManagementUtility(argv)
    # 调用其execute方法
    utility.execute()
    

class ManagementUtility(object):
    """
    Encapsulates the logic of the django-admin and manage.py utilities.
    """
    def __init__(self, argv=None):
        # 获取命令行参数
        self.argv = argv or sys.argv[:]
        # 执行命令的文件,django-admin.py
        self.prog_name = os.path.basename(self.argv[0])
        self.settings_exception = None
    
    pass
```

`execute()`方法源码如下 : 

```python
def execute(self):
	"""
	Given the command-line arguments, this figures out which subcommand is
	being run, creates a parser appropriate to that command, and runs it.
	"""
	try:
        # 提取子命令名称,如:startproject
		subcommand = self.argv[1]
	except IndexError:
		subcommand = 'help'  # Display help if no arguments were given.

	# Preprocess options to extract --settings and --pythonpath.
	# These options could affect the commands that are available, so they
	# must be processed early.
    
    # 实例化一个特定的参数解析器
	parser = CommandParser(None, usage="%(prog)s subcommand [options] [args]", add_help=False)
    
    # 预处理工作,添加参数
	parser.add_argument('--settings')
	parser.add_argument('--pythonpath')
	parser.add_argument('args', nargs='*')  # catch-all
	try:
		options, args = parser.parse_known_args(self.argv[2:])
        # 设置settings和pythonpath参数
		handle_default_options(options)
	except CommandError:
		pass  # Ignore any option errors at this point.

	try:
        # 正常情况下,我们看到这样的语句差不多可以直接掠过了,因为似乎没有意义
        # 但是settings却是一个特殊的情况,此时它并没有INSTALLED_APPS
        # 所以Python是找不到的,于是就会执行它的__getattr__方法来查找了
        # 于是,在这里就完成了初始化工作
		settings.INSTALLED_APPS
	except ImproperlyConfigured as exc:
		self.settings_exception = exc

	if settings.configured:
		# Start the auto-reloading dev server even if the code is broken.
		# The hardcoded condition is a code smell but we can't rely on a
		# flag on the command class because we haven't located it yet.
        
        # 下面跟Django的启动有关,暂且不说
		if subcommand == 'runserver' and '--noreload' not in self.argv:
			try:
				autoreload.check_errors(django.setup)()
			except Exception:
				# The exception will be raised later in the child process
				# started by the autoreloader. Pretend it didn't happen by
				# loading an empty list of applications.
				apps.all_models = defaultdict(OrderedDict)
				apps.app_configs = OrderedDict()
				apps.apps_ready = apps.models_ready = apps.ready = True

				# Remove options not compatible with the built-in runserver
				# (e.g. options for the contrib.staticfiles' runserver).
				# Changes here require manually testing as described in
				# #27522.
				_parser = self.fetch_command('runserver').create_parser('django', 'runserver')
				_options, _args = _parser.parse_known_args(self.argv[2:])
				for _arg in _args:
					self.argv.remove(_arg)

		# In all other cases, django.setup() is required to succeed.
		else:
            # 配置settings,logging,urlresolvers,以及注册应用
			django.setup()
            
	self.autocomplete()

	if subcommand == 'help':
		if '--commands' in args:
			sys.stdout.write(self.main_help_text(commands_only=True) + '\n')
		elif len(options.args) < 1:
			sys.stdout.write(self.main_help_text() + '\n')
		else:
			self.fetch_command(options.args[0]).print_help(self.prog_name, options.args[0])
	# Special-cases: We want 'django-admin --version' and
	# 'django-admin --help' to work, for backwards compatibility.
	elif subcommand == 'version' or self.argv[1:] == ['--version']:
		sys.stdout.write(django.get_version() + '\n')
	elif self.argv[1:] in (['--help'], ['-h']):
		sys.stdout.write(self.main_help_text() + '\n')
	else:
        # 找到相应子命令,并执行
		self.fetch_command(subcommand).run_from_argv(self.argv)
```

接下来我们看看最后的这个`fetch_command(subcommand)` 和 `run_from_argv(self.argv) ` 

## fetch_command()  🍀

`management/__init__.py` 

```python
    def fetch_command(self, subcommand):
        """
        Tries to fetch the given subcommand, printing a message with the
        appropriate command called from the command line (usually
        "django-admin" or "manage.py") if it can't be found.
        """
        # Get commands outside of try block to prevent swallowing exceptions
        commands = get_commands()
        try:
            # 获取子命令模块对应的前缀,这里是django.core
            app_name = commands[subcommand]
        except KeyError:
            if os.environ.get('DJANGO_SETTINGS_MODULE'):
                # If `subcommand` is missing due to misconfigured settings, the
                # following line will retrigger an ImproperlyConfigured exception
                # (get_commands() swallows the original one) so the user is
                # informed about it.
                
                # 防止未初始化
                settings.INSTALLED_APPS
            else:
                sys.stderr.write("No Django settings specified.\n")
            sys.stderr.write(
                "Unknown command: %r\nType '%s help' for usage.\n"
                % (subcommand, self.prog_name)
            )
            sys.exit(1)
        if isinstance(app_name, BaseCommand):
            # If the command is already loaded, use it directly.
            klass = app_name
        else:
            # load_command_class会返回指定子命令相对应的Command类的实例
            # load_command_class见下一小结
            klass = load_command_class(app_name, subcommand)
        return klass
```

下面详细的解释一下`load_command_class()`

## load_command_class( )  🍀

`management/__init__.py` 

```python
def load_command_class(app_name, name):
    """
    Given a command name and an application name, returns the Command
    class instance. All errors raised by the import process
    (ImportError, AttributeError) are allowed to propagate.
    """
    # app_name:子模块对应的前缀名
    # name:子命令
    # 加载django.core.management.commands.startproject
    module = import_module('%s.management.commands.%s' % (app_name, name))
    # 返回startproject中的Command类的实例
    return module.Command()
```

## run_from_argv( )  🍀

那么到这里 , 准备工作已经全部完成 , 现在就是真正的执行时刻了 , :koala: 

在开始之前还有点事需要说明 , 这个方法存在的位置并不是子命令对应的`Command`中 , 而是在其最高基类`BaseCommand`中 , 所有的`Command`类都必须直接或者间接的继承`BaseCommand`类

对于`run_from_argv`源码就不贴了 , 因为实际上 , 它也不是正主 , `run_from_argv`主要就是设置环境 (比如Python路径和Django配置) , 随后它会调用BaseCommand类的`execute()`方法 , 但这不是绝对 , 因为有的派生类中重写了`execute()` :

```python
def execute(self, *args, **options):
    """
    Try to execute this command, performing system checks if needed (as
    controlled by the ``requires_system_checks`` attribute, except if
    force-skipped).
    """
    
    # 在需要是进行系统检查
    ...
    # 最后会调用Command类中的handle
    output = self.handle(*args, **options)
    ...
```

上述中的`handle()`方法 , 必须在子类中实现 , 原因如下 : 

在`django/core/management/base.py` , BaseCommand类中的`handle()`

```python
def handle(self, *args, **options):
    """
    The actual logic of the command. Subclasses must implement
    this method.
    """
    
    # 执行我?对不起我要给你抛个NotImplementedError
    raise NotImplementedError('subclasses of BaseCommand must provide a handle() method')
```
接下来 , 我们看看`startproject.py`中Command类的`handle()` 

```python
    def handle(self, **options):
        project_name, target = options.pop('name'), options.pop('directory')
        self.validate_name(project_name, "project")

        # Check that the project_name cannot be imported.
        try:
            import_module(project_name)
        except ImportError:
            pass
        else:
            raise CommandError(
                "%r conflicts with the name of an existing Python module and "
                "cannot be used as a project name. Please try another name." % project_name
            )

        # Create a random SECRET_KEY to put it in the main settings.
        options['secret_key'] = get_random_secret_key()
		
        # 加载其基类TemplateCommand中的handle方法
        # PS:TempalteCommand的基类为BaseCommand
        super(Command, self).handle('project', project_name, target, **options)
```

最后TemplateCommand类中的`handle()`会为我们进行Django项目的布局到指定目录 , 至此 , 命令执行完毕 , 我们所看到的所有默认目录也已经创建完毕

## 小结  🍀

到这里对于django项目的开始已经有了基本的了解了 :

1. 在命令行执行django-admin.py相关命令
2. 执行management中的`execute_from_command_line() `函数
3. 实例化ManagementUtility类并调用`execute()`方法
4. 随后就是获取命令行输入的参数实例化相应的Command类
5. 调用类中的`handle()`方法

注意 : 

- django-admin命令并不仅仅根据`django/core/management/commands`来加载 , 而是会将所有的Application下的`management/commands` 都加载进入commands字典中

- 该commands字典是通过 , `management/__init__.py` 中的`get_commands()`函数生成的 

  ```python
  @lru_cache.lru_cache(maxsize=None)
  def get_commands():
  	"""
      Returns a dictionary mapping command names to their callback applications.
      ...
      """
      pass
  ```

到这里 , 我们可以想 , 既然django会到各个应用中去寻找`management/commands`目录 , 再寻找`subcommand` , 那么如果在自己的应用下创建一个`mycommand` , 然后定义一个`Command`类 , 重写`handle()`方法 , 是不是就自定制django-admin命令了

没错 , 这一点在django的官方文档中已经提供相关教程了 , 想要自定制命令就点击下面的教程链接吧 : [Writing custom django-admin commands](https://docs.djangoproject.com/en/1.11/howto/custom-management-commands/) 

