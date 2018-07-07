# pip升级至10.0.1无法用PyCharm安装module

前提 : 将pip升至 `10.0.1` 版本

**错误日志如下 :** 

```python
Traceback (most recent call last):
  File "E:\pycharm\PyCharm 2016.2.3\helpers\packaging_tool.py", line 184, in main
    retcode = do_install(pkgs)
  File "E:\pycharm\PyCharm 2016.2.3\helpers\packaging_tool.py", line 109, in do_install
    return pip.main(['install'] + pkgs)
AttributeError: module 'pip' has no attribute 'main'
```

**原因 :** 

pip 版本较高 , 而PyCharm版本较低导致的 

解决方案有两种 , 一种就修改python代码 , 让其正确导入 main , 另一种则是将PyCharm升级至2018的版本

以下介绍第一种解决方案 : 

将 `PyCharm\helpers\packaging_tool.py` 中的如下代码 : 

```python
def do_install(pkgs):
    try:
    	import pip
    except ImportError:
        error_no_pip()
    return pip.main(['install'] + pkgs)


def do_uninstall(pkgs):
    try:
    	import pip
    except ImportError:
        error_no_pip()
    return pip.main(['uninstall', '-y'] + pkgs)
```

**修改为 :** 

```python
def do_install(pkgs):
    try:
    	#import pip                               
    	try:
    		from pip._internal import main
    	except Exception:
    		from pip import main
    except ImportError:
        error_no_pip()
    return main(['install'] + pkgs)


def do_uninstall(pkgs):
    try:
    	#import pip
    	try:
    		from pip._internal import main
    	except Exception:
    		from pip import main
    except ImportError:
        error_no_pip()
    return main(['uninstall', '-y'] + pkgs)
```

问题解决 !

