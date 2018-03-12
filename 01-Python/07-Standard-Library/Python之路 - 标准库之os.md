# Python之路 - 标准库之os

## 介绍  🍀

`os`模块为我们提供了与操作系统相关的诸多接口

在Python中 , 使用字符串类型来表示文件名 , 命令行参数和环境变量

`os`模块功能总体分为以下几个部分 : 

- 当前进程和用户操作
- 文件描述符操作
- 文件和目录操作
- 进程管理
- 调度程序接口 (仅在一些Unix平台上)
- 系统信息处理

总体概况

```python
DESCRIPTION
    This exports:
      - all functions from posix, nt or ce, e.g. unlink, stat, etc.
      - os.path is either posixpath or ntpath
      - os.name is either 'posix', 'nt' or 'ce'.
      - os.curdir is a string representing the current directory ('.' or ':')
      - os.pardir is a string representing the parent directory ('..' or '::')
      - os.sep is the (or a most common) pathname separator ('/' or ':' or '\\')
      - os.extsep is the extension separator (always '.')
      - os.altsep is the alternate pathname separator (None or '/')
      - os.pathsep is the component separator used in $PATH etc
      - os.linesep is the line separator in text files ('\r' or '\n' or '\r\n')
      - os.defpath is the default search path for executables
      - os.devnull is the file path of the null device ('/dev/null', etc.)
```

注意 : 在`os`模块中有很多方法只有在Unix系统上才能使用

由于`os`模块提供的方法太多 , 所以本文仅介绍一些在windows下常用的方法

## OS  🍀

```python
os.getcwd()
"""
Return a string representing the current working directory.
"""

os.chdir(path)
"""
Change the current working directory to path.
"""

os.curdir
"""
The constant string used by the operating system to refer to the current directory. 
This is '.' for Windows and POSIX. Also available via os.path.
"""

os.pardir
"""
The constant string used by the operating system to refer to the parent directory. 
This is '..' for Windows and POSIX. Also available via os.path.
"""

os.makedirs(name, mode=0o777, exist_ok=False)
"""
Recursive directory creation function. Like mkdir(), 
but makes all intermediate-level directories needed to contain the leaf directory.
"""

os.removedirs(name)
"""
Remove directories recursively. 
Works like rmdir() except that, 
if the leaf directory is successfully removed, 
removedirs() tries to successively remove every parent directory mentioned in path until an error is raised
"""

os.rmdir(path, *, dir_fd=None)
"""
Remove (delete) the directory path. 
Only works when the directory is empty, otherwise, OSError is raised. 
In order to remove whole directory trees, shutil.rmtree() can be used.
"""

os.listdir(path='.')
"""
Return a list containing the names of the entries in the directory given by path. 
The list is in arbitrary order, and does not include the special entries '.' and '..' even if they are present in the directory.
"""

os.remove(path, *, dir_fd=None)
"""
Remove (delete) the file path. 
If path is a directory, OSError is raised. Use rmdir() to remove directories.
"""

os.rename(src, dst, *, src_dir_fd=None, dst_dir_fd=None)
"""
Rename the file or directory src to dst.
"""

os.stat(path, *, dir_fd=None, follow_symlinks=True)
"""
Get the status of a file or a file descriptor.
"""

os.sep
"""
The character used by the operating system to separate pathname components. 
This is '/' for POSIX and '\\' for Windows.
"""

os.linesep    
"""
The string used to separate (or, rather, terminate) lines on the current platform. 
This may be a single character, such as '\n' for POSIX, or multiple characters, for example, '\r\n' for Windows.
"""

os.pathsep
"""
The character conventionally used by the operating system to separate search path components (as in PATH), such as ':' for POSIX or ';' for Windows. 
Also available via os.path.
"""

os.name
"""
The name of the operating system dependent module imported. 
The following names have currently been registered: 'posix', 'nt', 'java'.
"""

os.system(command)
"""
Execute the command (a string) in a subshell.
"""

os.popen(cmd, mode='r', buffering=-1)
"""
Open a pipe to or from command cmd. 
The return value is an open file object connected to the pipe, 
which can be read or written depending on whether mode is 'r' (default) or 'w'.
"""

os.environ
"""
A mapping object representing the string environment.
"""
```

更多`os`模块相关 :  [os](https://docs.python.org/3/library/os.html?highlight=os#module-os) — Miscellaneous operating system interfaces

## OS.Path  🍀

```python
os.path.abspath(path)
"""
Return a normalized absolutized version of the pathname path. 
On most platforms, this is equivalent to calling the function normpath() as follows: normpath(join(os.getcwd(), path)).
"""

os.path.exists(path)
"""
Return True if path refers to an existing path or an open file descriptor. 
Returns False for broken symbolic links. 
"""

os.path.isabs(path)
"""
Return True if path is an absolute pathname.
"""

os.path.isfile(path) 
"""
Return True if path is an existing regular file.
"""

os.path.isdir(path) 
"""
Return True if path is an existing directory.
"""

os.path.join(path, *paths)
"""
Join one or more path components intelligently.
"""

os.path.getatime(path) 
"""
Return the time of last access of path.
"""

os.path.getmtime(path)
"""
Return the time of last modification of path.
"""

os.path.getsize(path)
"""
Return the size, in bytes, of path. 
Raise OSError if the file does not exist or is inaccessible.
"""
```

更多`os.path`相关 : [os.path](https://docs.python.org/3/library/os.path.html#module-os.path) — Common pathname manipulations

补充 : 

- 如果需要读取命令行上所有文件中的所有行 , 可以查看[`fileinput`](https://docs.python.org/3/library/fileinput.html#module-fileinput) 模块
- 如果需要创建临时文件和目录 , 可以查看[`tempfile`](https://docs.python.org/3/library/tempfile.html#module-tempfile) 模块
- 关于文件和文件集合的高级操作 , 可以查看[`shutil`](https://docs.python.org/3/library/shutil.html#module-shutil) 模块