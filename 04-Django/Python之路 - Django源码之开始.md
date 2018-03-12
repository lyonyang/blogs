# Python之路 - Django源码之开始
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

首先`django-admin.py`被执行 , 随后进入了`django/core/management/__init__.py`  , 因为`management`也是Python中的一个包 , 源码如下 

`management/__init__.py`

```python
def execute_from_command_line(argv=None):
    """
    A simple method that runs a ManagementUtility.
    """
    utility = ManagementUtility(argv)
    utility.execute()
    
# 继续前进
# 实例化ManagementUtility类
class ManagementUtility(object):
    """
    Encapsulates the logic of the django-admin and manage.py utilities.
    """
    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(self.argv[0])
        self.settings_exception = None
    
    pass

# 调用实例中的execute方法
```

`execute()`方法源码如下 : 

```python
    def execute(self):
        """
        Given the command-line arguments, this figures out which subcommand is
        being run, creates a parser appropriate to that command, and runs it.
        """
        
        # 提取子命令名称,如:startproject
        try:
            subcommand = self.argv[1]
        except IndexError:
            subcommand = 'help'  # Display help if no arguments were given.

        # Preprocess options to extract --settings and --pythonpath.
        # These options could affect the commands that are available, so they
        # must be processed early.
        
        # 接下来一堆操作是进行预处理
        # 包括应用命令行参数解析和环境的创建等,不多说明
		...
        
        # 子命令执行方式
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
            
            # 待到所有的处理工作完成之后,开始执行命令,步骤如下
            """
            1. 通过fetch_command方法获取子命令的实例,流程如下
            	- 已经加载 -> 返回Command实例
            	- 尚未加载 -> load_command_class -> 返回Command实例
            2. 调用Command实例的基类(BaseCommand)中的run_from_argv方法,步骤如下
                1. 调用BaseCommand中的excute()方法
                2. 调用handle()方法,该方法在派生类中被重写
                3. 最后,返回其执行结果
            """
            self.fetch_command(subcommand).run_from_argv(self.argv)
            
```

下面详细的解释一下`load_command_class()` 与`run_from_argv()` 

## load_command_class( )  🍀

`management/__init__.py` 

```python
def load_command_class(app_name, name):
    """
    Given a command name and an application name, returns the Command
    class instance. All errors raised by the import process
    (ImportError, AttributeError) are allowed to propagate.
    """
    module = import_module('%s.management.commands.%s' % (app_name, name))
    return module.Command()
```

可以看到 , 该函数有两个参数 : 

- app_name , 应用名称 , 其来自于`get_commands()`返回的commands字典中 , `subcommand`为键获取该值
- name , 即`subcommand`

通过`importlib`中的`import_module`函数加载 , 所以上述`startproject` , 其app_name就是`django.core` , name就是`startproject`了

也就是`module = django.core.management.commands.startproject` 

于是 , 我们就可以看到Command类了

`management/commands/startproject.py`

```python
class Command(TemplateCommand):
    help = (
        "Creates a Django project directory structure for the given project "
        "name in the current directory or optionally in the given directory."
    )
    missing_args_message = "You must provide a project name."

	pass
```

最后 , 这个类的继承了TemplateCommand类 , 而后 , TemplateCommand又继承了BaseCommand类 , 也就是说 , BaseCommand是所有Command类的祖宗 , 为什么这么说 , 实际上 , 不仅仅是`startproject`命令 , 对于所有的Command类 , 并不是每个都继承了TemplateCommand类 , 但是最高基类一定都为BaseCommand类

## run_from_argv( )  🍀

对于这个方法的源码就不贴出来了 , 像上面说过的一样 , 这个方法里调用了BaseCommand类中的`execute()` , 而在`execute()`又会调用BaseCommand类中的`handle()` , 但是在真实情况下 , 这个`handle()`方法都被各个Command派生类重写了 , 并且必须重写 

在`django/core/management/base.py` , BaseCommand类中的`handle()`如下 :  

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

        super(Command, self).handle('project', project_name, target, **options)
```

我们注意到 , 这个重写的handle中好像并没有实质性的东西 , 仅仅做了个检查已经生成一个SECRET_KEY , 没错 , 因为那些关于整个项目默认创建的东西都在它的基类TemplateCommand的handle中

上述代码的最后一行 , 正将基类TemplateCommand的handle加载过来了

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