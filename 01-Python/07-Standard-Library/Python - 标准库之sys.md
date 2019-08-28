# Python之路 - 标准库之sys

## 介绍  🍀

`sys`模块为我们提供了对解释器使用或维护的一些变量的访问 , 以及解释器交互的函数 

`sys`模块总体分为四个部分 :  

- Dynamic objects , 动态对象
- Static objects , 静态对象
- Functions , 函数
- Data , 配置

## Dynamic objects  🍀

```python
argv -- command line arguments; argv[0] is the script pathname if known

path -- module search path; path[0] is the script directory, else ''

modules -- dictionary of loaded modules

displayhook -- called to show results in an interactive session

excepthook -- called to handle any uncaught exception other than SystemExit
	To customize printing in an interactive session or to install a custom top-level exception handler, 
    assign other functions to replace these.

stdin -- standard input file object; used by input()

stdout -- standard output file object; used by print()

stderr -- standard error object; used for error messages
      By assigning other file objects (or objects that behave like files)
      to these, it is possible to redirect all of the interpreter's I/O.

last_type -- type of last uncaught exception

last_value -- value of last uncaught exception

last_traceback -- traceback of last uncaught exception
These three are only available in an interactive session after a
traceback has been printed.
```

## Static objects  🍀

```python
builtin_module_names -- tuple of module names built into this interpreter

copyright -- copyright notice pertaining to this interpreter

exec_prefix -- prefix used to find the machine-specific Python library

executable -- absolute path of the executable binary of the Python interpreter

float_info -- a struct sequence with information about the float implementation.

float_repr_style -- string indicating the style of repr() output for floats

hash_info -- a struct sequence with information about the hash algorithm.

hexversion -- version information encoded as a single integer

implementation -- Python implementation information.

int_info -- a struct sequence with information about the int implementation.

maxsize -- the largest supported length of containers.

maxunicode -- the value of the largest Unicode code point

platform -- platform identifier

prefix -- prefix used to find the Python library

thread_info -- a struct sequence with information about the thread implementation.

version -- the version of this interpreter as a string

version_info -- version information as a named tuple

dllhandle -- [Windows only] integer handle of the Python DLL

winver -- [Windows only] version number of the Python DLL

__stdin__ -- the original stdin; don't touch!

__stdout__ -- the original stdout; don't touch!

__stderr__ -- the original stderr; don't touch!

__displayhook__ -- the original displayhook; don't touch!

__excepthook__ -- the original excepthook; don't touch!
```

## Functions  🍀

```python
displayhook() -- print an object to the screen, and save it in builtins._

excepthook() -- print an exception and its traceback to sys.stderr

exc_info() -- return thread-safe information about the current exception

exit() -- exit the interpreter by raising SystemExit

getdlopenflags() -- returns flags to be used for dlopen() calls

getprofile() -- get the global profiling function

getrefcount() -- return the reference count for an object (plus one :-)

getrecursionlimit() -- return the max recursion depth for the interpreter

getsizeof() -- return the size of an object in bytes

gettrace() -- get the global debug tracing function

setcheckinterval() -- control how often the interpreter checks for events

setdlopenflags() -- set the flags to be used for dlopen() calls

setprofile() -- set the global profiling function

setrecursionlimit() -- set the max recursion depth for the interpreter

settrace() -- set the global debug tracing function
```

## Data  🍀

```python
__stderr__ = <_io.TextIOWrapper name='<stderr>' mode='w' encoding='cp9...

__stdin__ = <_io.TextIOWrapper name='<stdin>' mode='r' encoding='cp936...

__stdout__ = <_io.TextIOWrapper name='<stdout>' mode='w' encoding='cp9...

api_version = 1013

argv = ['']

base_exec_prefix = r'C:\Users\Lyon\AppData\Local\Programs\Python\Pytho...

base_prefix = r'C:\Users\Lyon\AppData\Local\Programs\Python\Python35'

builtin_module_names = ('_ast', '_bisect', '_codecs', '_codecs_cn', '_...

byteorder = 'little'

copyright = 'Copyright (c) 2001-2016 Python Software Foundati...ematis...

dllhandle = 1373306880

dont_write_bytecode = False

exec_prefix = r'C:\Users\Lyon\AppData\Local\Programs\Python\Python35'
                        
executable = r'C:\Users\Lyon\AppData\Local\Programs\Python\Python35\py...
                        
flags = sys.flags(debug=0, inspect=0, interactive=0, opt...ing=0, quie...
                  
float_info = sys.float_info(max=1.7976931348623157e+308, max_...epsilo..
                            .
float_repr_style = 'short'
                            
hash_info = sys.hash_info(width=64, modulus=2305843009213693...iphash2...
                          
hexversion = 50660080
                          
implementation = namespace(cache_tag='cpython-35', hexversion=506...in...
                           
int_info = sys.int_info(bits_per_digit=30, sizeof_digit=4)
                           
maxsize = 9223372036854775807
                           
maxunicode = 1114111
                           
meta_path = [<class '_frozen_importlib.BuiltinImporter'>, <class '_fro...
             
modules = {'__main__': <module '__main__' (built-in)>, '_ast': <module...
           
path = ['', r'C:\Users\Lyon\AppData\Local\Programs\Python\Python35\pyt...
        
path_hooks = [<class 'zipimport.zipimporter'>, <function FileFinder.pa...
              
path_importer_cache = {r'C:\Users\Lyon': FileFinder('C:\\Users\\Lyon')...
                       
platform = 'win32'
                       
prefix = r'C:\Users\Lyon\AppData\Local\Programs\Python\Python35'
                       
ps1 = '>>> '
                       
ps2 = '... '
                       
stderr = <_io.TextIOWrapper name='<stderr>' mode='w' encoding='cp936'>
                       
stdin = <_io.TextIOWrapper name='<stdin>' mode='r' encoding='cp936'>
                       
stdout = <_io.TextIOWrapper name='<stdout>' mode='w' encoding='cp936'>
                       
thread_info = sys.thread_info(name='nt', lock=None, version=None)
                       
version = '3.5.2 (v3.5.2:4def2a2901a5, Jun 25 2016, 22:18:55) [MSC v.1...
                       
version_info = sys.version_info(major=3, minor=5, micro=2, releaseleve..
                                .
warnoptions = []
                                
winver = '3.5'
```
更多见 : [sys](https://docs.python.org/3/library/sys.html?highlight=sys#module-sys) — System-specific parameters and functions 