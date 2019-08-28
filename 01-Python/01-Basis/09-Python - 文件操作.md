# Python之路 - 文件操作

## 介绍  🍀

在磁盘上读写文件的功能都是由操作系统提供的 , 现代操作系统不允许普通的程序直接操作磁盘 , 所以 , 读写文件就是请求操作系统打开一个文件对象 (通常称为文件描述符) ; 然后 , 通过操作系统提供的接口从这个文件对象中读取数据 (读文件) , 或者把数据写入这个文件对象 (写文件) 

在Python中我们进行文件操作需要首先利用`open()` 函数获取一个文件流来操作文件

这个流就是我们所使用的文件描述符 , 是一个I/O通道

## open()  🍀

```python
open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
    """
    file:文件名
    mode:模式
    buffering:设置缓冲策略
    encoding:指定使用编码
    errors:指定处理编码和解码错误的方式
    newline:控制通用换行模式的工作方式(只适用文本模式)
    closefd:如果为False并且给出了文件描述符而不是文件名,则文件关闭时,文件描述符将保持打开;如果给定文件名,则closefd必须为True,否则将抛出异常
    opener:自定义开启器
    """
```

对于上述参数中 , 我们主要需要了解的就是`file` , `mode` , `encoding` 这三个

对于mode , 有以下模式 : 

| Character | Meaning                                  |
| --------- | ---------------------------------------- |
| `'r'`     | open for reading (default)               |
| `'w'`     | open for writing, truncating the file first |
| `'x'`     | open for exclusive creation, failing if the file already exists |
| `'a'`     | open for writing, appending to the end of the file if it exists |
| `'b'`     | binary mode                              |
| `'t'`     | text mode (default)                      |
| `'+'`     | open a disk file for updating (reading and writing) |
| `'U'`     | [universal newlines](https://docs.python.org/3.5/glossary.html#term-universal-newlines) mode (deprecated) |

常使用的就是`'r'` , `'w'` , `'a'` , `'+'` , `'b'` , 当然还可以组合使用 , 下面进行详细介绍 : 

- r , 只读模式 , 文件必须已经存在
- r+ , 可读可写模式 , 文件必须已经存在
- w , 只写模式 , 会重新创建 , 意味着文件如果已存在会被空文件覆盖
- w+ , 可写可读模式 , 同样会创建文件
- a , 追写模式 , 文件不存在参考'w'
- a+ , 追写并可读模式 , 文件不存在参考'w'
- b , 以二进制的模式进行处理 (Linux可忽略 , Windows处理二进制文件时需标注)  , 可以用该模式来读取图片 , 视频等等
  - rb , 同r
  - wb , 同w 
  - ab , 同a

简单实例

file.txt

```txt
A man is not old until his regrets take place of his dreams.  

Nothing can help us endure dark times better than our faith.

No one but ourselves can degrade us. 
```

实例

```python
f = open('file.txt','r')
contents = f.read
print(contents)
'''
执行结果:
A man is not old until his regrets take place of his dreams.  

Nothing can help us endure dark times better than our faith.

No one but ourselves can degrade us. 
'''
```

## file-like object  🍀

io模块提供了Python处理各种类型I/O的主要工具 , 有三种主要类型 , 即`文本I/O` , `二进 制I/O`和`原始I/O` , 这些是通用类别 , 并且可以为它们中的每一个使用各种后备存储

三种主要类型详细见 :  [`TextIOBase`](https://docs.python.org/3.5/library/io.html?highlight=io#io.TextIOBase) ,  [`BufferedIOBase`](https://docs.python.org/3.5/library/io.html?highlight=io#io.BufferedIOBase) ,  [`RawIOBase`](https://docs.python.org/3.5/library/io.html?highlight=io#io.RawIOBase) 

属于这些类别中的任何一个的具体对象称为`file-like object` 

创建这些类别的具体对象最简单的方法就是使用内置的`open()` 函数 , 其也被定义在io模块中 , 下面仅介绍一些这些类别对象常用的方法 :

```python
detach()
'''
Separate the underlying binary buffer from the TextIOBase and return it.

After the underlying buffer has been detached, the TextIOBase is in an unusable state.

Some TextIOBase implementations, like StringIO,
 may not have the concept of an underlying buffer and calling this method will raise UnsupportedOperation.

New in version 3.1.
'''

read(size)
'''
Read and return at most size characters from the stream as a single str. 
If size is negative or None, reads until EOF.
'''

readline(size=-1)
'''
Read until newline or EOF and return a single str. 
If the stream is already at EOF, an empty string is returned.

If size is specified, at most size characters will be read.
'''

readlines(hint=-1)
'''
Read and return a list of lines from the stream. hint can be specified to control the number of lines read: no more lines will be read if the total size (in bytes/characters) of all lines so far exceeds hint.

Note that it’s already possible to iterate on file objects using for line in file: ... without calling file.readlines().
'''

readable()
'''
Return True if the stream can be read from. 
If False, read() will raise OSError.
'''

write(s)
'''
Write the string s to the stream and return the number of characters written.
'''

writable()
'''
Return True if the stream supports writing. 
If False, write() and truncate() will raise OSError.
'''

writelines(lines)
'''
Write a list of lines to the stream.
Line separators are not added, 
so it is usual for each of the lines provided to have a line separator at the end.
'''

seek(offset[, whence])
'''
Change the stream position to the given offset. 
Behaviour depends on the whence parameter. 
The default value for whence is SEEK_SET.

SEEK_SET or 0: seek from the start of the stream (the default); 
offset must either be a number returned by TextIOBase.tell(), or zero. 
Any other offset value produces undefined behaviour.
SEEK_CUR or 1: “seek” to the current position; 
offset must be zero, which is a no-operation (all other values are unsupported).
SEEK_END or 2: seek to the end of the stream; 
offset must be zero (all other values are unsupported).
Return the new absolute position as an opaque number.

New in version 3.1: The SEEK_* constants.
'''

tell()
'''
Return the current stream position as an opaque number. 
The number does not usually represent a number of bytes in the underlying binary storage.
'''

close()
'''
Flush and close this stream. 
This method has no effect if the file is already closed. 
Once the file is closed, 
any operation on the file (e.g. reading or writing) will raise a ValueError.

As a convenience, it is allowed to call this method more than once; 
only the first call, however, will have an effect.
'''

fileno()
'''
Return the underlying file descriptor (an integer) of the stream if it exists. An OSError is raised if the IO object does not use a file descriptor.
'''

flush()
'''
Flush the write buffers of the stream if applicable. 
This does nothing for read-only and non-blocking streams.
'''

isatty()
'''
Return True if the stream is interactive (i.e., connected to a terminal/tty device).
'''

seek(offset[, whence])
'''
Change the stream position to the given byte offset. 
offset is interpreted relative to the position indicated by whence. 
The default value for whence is SEEK_SET. Values for whence are:

SEEK_SET or 0 – start of the stream (the default); 
offset should be zero or positive
SEEK_CUR or 1 – current stream position; 
offset may be negative
SEEK_END or 2 – end of the stream; 
offset is usually negative
Return the new absolute position.

New in version 3.1: The SEEK_* constants.

New in version 3.3: Some operating systems could support additional values, 
like os.SEEK_HOLE or os.SEEK_DATA. 
The valid values for a file could depend on it being open in text or binary mode.
'''

seekable()
'''
Return True if the stream supports random access. 
If False, seek(), tell() and truncate() will raise OSError.
'''

truncate(size=None)
'''
Resize the stream to the given size in bytes (or the current position if size is not specified). 
The current stream position isn’t changed. 
This resizing can extend or reduce the current file size. 
In case of extension, the contents of the new file area depend on the platform (on most systems, additional bytes are zero-filled). 
The new file size is returned.

Changed in version 3.5: Windows will now zero-fill files when extending.
'''
```

注意 : 当使用完文件后一定要记得使用`close()` 方法将其关闭 ; 其次在进行文件操作时要注意文件描述符所在的位置

## with  🍀

为了避免打开文件后忘记手动关闭 , 可以通过管理上下文 , 即使用`with`语句 , 如下 :

```python
with open('filepath','mode') as f:
    pass
```

在Python 2.7以上的版本 , 支持同时对多个文件同时进行上下文管理 , 如下 : 

```python
with open('filepath1','mode') as f1,open('filepath2','mode') as f2:
    pass
```

更多文档资料 : https://docs.python.org/3.5/library/io.html?highlight=io#module-io