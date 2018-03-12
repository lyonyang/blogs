# Python之路 - 网络编程之Socket

## C/S架构  🍀

在网络通信中 , 一般是一方求一方应 , 求的一方就是客户端即 ` Client `  , 应的一方就是服务端即` Server ` , 这就是C/S架构 , 在互联网中处处是C/S架构 , 比如我们访问百度 ,  百度就是一个服务端 , 而我们的浏览器就是一个客户端

## Socket  🍀

Socket是应用层与TCP/IP协议族通信的中间软件抽象层 , 它是一组接口 , 是从顶上三层 (osi七层协议的应用层) 进入传输层的接口 ; 顶上三层通常构成所谓的用户进程 , 底下四层却通常作为操作系统内核的一个部分提供

Socket又叫做套接字 , Python中socket为我们封装好了TCP/UDP协议 , 所以我们无需深入理解 , 只要遵循socket的规定去编程就可以了

**创建socket对象** 

创建socket对象就是一个建立TCP的过程 , 即三次握手 , 断开当然就是四次挥手了

![TCP communication](http://oux34p43l.bkt.clouddn.com/TCP%20communication.png)

代码实现

```python
# 导入socket模块
import socket
# 调用socket模块中的socket类实例化出对象
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
'''或者可以使用 from module import * ,可以大幅度减少代码,仅仅提一下,毕竟有弊端'''
# 导入socket模块中的所有内容
from socket import *
# 实例化socket类
sock = socket(AF_INET,SOCK_STREAM,0)
```

**socket类参数说明** 

其构造函数源码

```python
def __init__(self, family=AF_INET, type=SOCK_STREAM, proto=0, fileno=None):
    # 下面内容就不摘了
	pass
```

> *family* : 地址簇

| 参数       | 说明              |
| -------- | --------------- |
| AF_INET  | IPv4 , 即默认为IPv4 |
| AF_INET6 | IPv6            |
| AF_UNIX  | 针对Unix系统进程间通信   |

> *type* : 类型

| 参数             | 说明                                       |
| -------------- | ---------------------------------------- |
| SOCK_STREAM    | 面向流 , 即TCP                               |
| SOCK_DGRAM     | 面向数据报 , 即UDP                             |
| SOCK_RAW       | 原始套接字 , 可处理ICMP,IGMP等网络报文 ; 可以处理特殊的IPv4报文 ; 利用原始套接字 , 可以通过IP_HDRINCL套接字选项由用户构造IP头 |
| SOCK_RDM       | 一种可靠的UDP形式 . SOCK_RAM用来提供对原始协议的低级访问 , 在需要执行某些特殊操作时使用 , 如发送ICMP报文 , SOCK_RAW通常仅限于高级用户或管理员运行的程序使用 |
| SOCK_SEQPACKET | 可靠的连续数据包服务                               |

> *proto* : 协议

| 参数   | 说明                                       |
| ---- | ---------------------------------------- |
| 0    | 与特定的地址家族相关的协议 , 如果是0 , 则系统就会根据地址格式和套接类别 , 自动选择一个合适的协议 |

还有一个*fileno*参数是无需理会的

## 基于TCP  🍀

TCP协议是有链接的 , 面向流的 , 数据传输可靠 , 必须先启动服务端

**TCP服务端** 

1. 创建套接字对象		                	*创建socket对象* 
2. 绑定IP和端口                                         *绑定 bind()* 
3. 开始监听链接                                        *监听 listen()* 
4. 阻塞 , 等待客户端成功连接                  *阻塞 accept()* 
5. 接收请求数据                                        *接收 recv()* 
6. 处理并发送请求数据                            *发送 send()* 
7. 通信完毕 , 关闭链接 , 关闭套接字       *关闭 close()*                    

**TCP客户端** 

1. 创建套接字对象                                     *创建socket对象* 
2. 连接服务端 , 按照IP和端口连接           *连接 connet()* 
3. 发送请求数据                                        *发送 send()* 
4. 接收请求数据                                        *接收 recv()* 
5. 通信完毕 , 关闭套接字                        *关闭 close()* 

简单实例

tcp_server.py

```python
# 导入socket模块
import socket
# 创建socket对象,默认参数就不填了
sock = socket.socket()
# 绑定IP和端口,参数是一个元组(ip,port)
sock.bind(('127.0.0.1', 8080))
# 开始监听,最大监听数为5
sock.listen(5)
# 阻塞,等待连接,返回一个链接通道和一个地址
conn,addr = sock.accept()
# 接收请求数据,接收大小为1024字节
content = conn.recv(1024)
# 打印结果(bytes转成str显示)
print(content.decode())
# 发送请求结果,必须以bytes类型
conn.send(b'Hello Lyon')
# 关闭链接
conn.close()
# 关闭套接字
sock.close()
```

tcp_client.py

```python
# 导入socket模块
import socket
# 创建socket对象
sock = socket.socket()
# 建立链接
sock.connect(('127.0.0.1', 8080))
# 发送请求数据,必须以bytes类型
sock.send(b"I'm Lyon")
# 接收请求结果
content = sock.recv(1024)
# 打印结果
print(content.decode())
# 关闭套接字
sock.close()
```

## 基于UDP  🍀

UDP协议是无链接的 , 面向数据报的 , 数据传输全靠吼 , 不可靠 , 先启动哪一端都不会报错

**UDP服务端** 

1. 创建套接字对象		                	*创建socket对象* 
2. 绑定IP和端口                                         *绑定 bind()* 
3. 接收请求数据                                        *接收 recvfrom()* 
4. 通信完毕 , 关闭套接字       *关闭 close()*                    

**UDP客户端** 

1. 创建套接字对象                                     *创建socket对象* 
2. 发送请求数据                                        *发送 sendto()* 
3. 通信完毕 , 关闭套接字                        *关闭 close()* 

简单实例

udp_server.py

```python
# 导入socket模块
import socket
# 创建socket对象
sock = socket.socket(type=socket.SOCK_DGRAM)
# 绑定ip和端口
sock.bind(('127.0.0.1', 8090))
# 接收请求,返回数据和地址
data,addr = sock.recvfrom(1024)
# 打印请求
print(data.decode())
# 关闭套接字
sock.close()
```

udp_client.py

```python
# 导入socket模块
import socket
# 创建socket对象
sock = socket.socket(type=socket.SOCK_DGRAM)
# 发送请求到指定地址
sock.sendto(b"I'm Lyon", ('127.0.0.1', 8090))
# 关闭套接字
sock.close()
```

## Socket对象方法  🍀

| 方法                                   | 描述                                       |
| ------------------------------------ | ---------------------------------------- |
| s.bind()                             | 绑定地址（host,port）到套接字， 在AF_INET下,以元组（host,port）的形式表示地址。 |
| s.listen()                           | 开始TCP监听。backlog指定在拒绝连接之前，操作系统可以挂起的最大连接数量。该值至少为1，大部分应用程序设为5就可以了。 |
| s.accept()                           | 被动接受TCP客户端连接,(阻塞式)等待连接的到来                |
| s.connect()                          | 主动初始化TCP服务器连接，。一般address的格式为元组（hostname,port），如果连接出错，返回socket.error错误。 |
| s.connect_ex()                       | connect()函数的扩展版本,出错时返回出错码,而不是抛出异常        |
| s.recv()                             | 接收TCP数据，数据以字符串形式返回，bufsize指定要接收的最大数据量。flag提供有关消息的其他信息，通常可以忽略。 |
| s.send()                             | 发送TCP数据，将string中的数据发送到连接的套接字。返回值是要发送的字节数量，该数量可能小于string的字节大小。 |
| s.sendall()                          | 完整发送TCP数据，完整发送TCP数据。将string中的数据发送到连接的套接字，但在返回之前会尝试发送所有数据。成功返回None，失败则抛出异常。 |
| s.recvfrom()                         | 接收UDP数据，与recv()类似，但返回值是（data,address）。其中data是包含接收数据的字符串，address是发送数据的套接字地址。 |
| s.sendto()                           | 发送UDP数据，将数据发送到套接字，address是形式为（ipaddr，port）的元组，指定远程地址。返回值是发送的字节数。 |
| s.close()                            | 关闭套接字                                    |
| s.getpeername()                      | 返回连接套接字的远程地址。返回值通常是元组（ipaddr,port）。      |
| s.getsockname()                      | 返回套接字自己的地址。通常是一个元组(ipaddr,port)          |
| s.setsockopt(level,optname,value)    | 设置给定套接字选项的值。                             |
| s.getsockopt(level,optname[.buflen]) | 返回套接字选项的值。                               |
| s.settimeout(timeout)                | 设置套接字操作的超时期，timeout是一个浮点数，单位是秒。值为None表示没有超时期。一般，超时期应该在刚创建套接字时设置，因为它们可能用于连接的操作（如connect()） |
| s.gettimeout()                       | 返回当前超时期的值，单位是秒，如果没有设置超时期，则返回None。        |
| s.fileno()                           | 返回套接字的文件描述符。                             |
| s.setblocking(flag)                  | 如果flag为0，则将套接字设为非阻塞模式，否则将套接字设为阻塞模式（默认值）。非阻塞模式下，如果调用recv()没有发现任何数据，或send()调用无法立即发送数据，那么将引起socket.error异常。 |
| s.makefile()                         | 创建一个与该套接字相关连的文件                          |

解决` OSError: [Errno 48] Address already in use ` 问题

添加一条socket配置 , 重用ip和端口

```python
import socket
sock = socket.socket()
# 添加在bind前
sock.setsockopt(socket.SOL_SOCKET,SO_REUSEADDR,1)
sock.bind(address)
```

