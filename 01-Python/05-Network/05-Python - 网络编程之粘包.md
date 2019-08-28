# Python之路 - 网络编程之粘包

## 粘包  🍀


由上一篇<[Python之路 - Socket实现远程执行命令](https://lyonyang.gitbooks.io/blog/05-Python%E7%BD%91%E7%BB%9C%E7%BC%96%E7%A8%8B/04-Python%E4%B9%8B%E8%B7%AF%20-%20Socket%E5%AE%9E%E7%8E%B0%E8%BF%9C%E7%A8%8B%E6%89%A7%E8%A1%8C%E5%91%BD%E4%BB%A4.html)>中所出现的问题引出了粘包这个问题 , 粘包到底是什么?

首先 ,  ` 粘包现象只出现在TCP中 `  ,  为什么说只有在TCP中才会发生粘包现象 , 先来详细解释一下TCP与UDP吧

> **TCP** 

TCP (transprot control protocol, 传输控制协议) 是面向连接的 , 面向流的 , 提供高可靠性服务 .  收发两端都有要一一对应的socket(一对一模式) , 因此发送端为了将多个发往接收端的包 , 更有效的发到对方 , 使用了优化方法(Nagle算法) , ` 将多次间隔较小且数据量小的数据 , 合并成一个大的数据块 , 然后进行封包 . ` 必须提供科学的拆包机制 , 才能进行合理的分辨 , 所以说面向流的通信是无消息保护边界的

> **UDP** 

UDP(user datagram protocol, 用户数据报协议) 是无连接的 , 面向消息的 , 提供高效率服务 . 不使用块的合并优化算法 , 由于UDP支持的是一对多的模式 , 所以接收端的skbuff (套接字缓冲区) 采用了链式结构来记录每一个到达的UDP包 , 在每个UDP包中就有了消息头 (消息来源地址 , 端口等信息) , 这样 , 对于接收端来说 , 就容易进行区分处理了 . 即面向的通信是有消息保护边界的

> **区别** 

TCP是基于数据流的 , 于是收发的消息不能为空 , 这就需要在客户端和服务端都添加空消息的处理机制 , 防止程序卡住 , 而UDP是基于数据报的 , 就算收发空内容 , 也不是空消息 , UDP协议会自动帮你封装上消息头

**粘包现象发生的原因** 

粘包分为两种

1. 发送方引起的粘包

   这种情况下引起的粘包是TCP协议本身造成的 , TCP为了提高传输效率 , 发送方往往要收集到足够多的数据后才发送一个TCP段 `(超过时间间隔也会发送,时间间隔是很短的)`  , 如果连续几次需要发送的数据都很少 , 通常TCP会根据优化算法把这些数据合成一个TCP段后一次发送出去 , 所以几次的数据到接收方时就粘成一包了

   如下 :

   ```python
   # 发送方第一次发送
   send(b"I'm ")
   # 立马第二次,不超过时间间隔
   send(b"Lyon")
   -------------
   # 接收
   data = recv(1024)
   # 收到的是两次粘在一起的数据
   print(data.decode())
   # 打印结果: I'm Lyon
   ```

2. 接收方引起的粘包

   这种情况引起的粘包则是因为接收方不及时接收缓冲区的数据包造成的 , 比如发送方一次发送了10字节的数据 , 而接收方只接收了2字节 , 那么剩余的8字节的数据将都在缓冲区等待接收 , 而此时发送方又发送了2字节的数据 , 过了一会接收方接收了20字节(大于剩余10字节) , 接收完毕 , 缓冲区剩余的数据就和第二次发送的数据粘成了一个包 , 产生粘包

   如下 : 

   ```python
   # 发送4字节内容
   send(b"I'm ")
   # 接收1字节,缓冲区还有3字节
   data1 = recv(1)
   print("data1:",data1)
   # 发送4字节内容,粘到缓冲区中剩余的3字节后面
   send(b"Lyon")
   # 接收7字节,接收完毕
   data2 = recv(7)
   print("data2:",data2)
   '''
   打印结果:
   data1:I
   data2:'m Lyon
   '''
   ```

**SO : 所以所谓粘包问题主要还是因为接收方不知道消息之间的界限 , 不知道一次性提取多少字节的数据所造成的** 

## 解决方法  🍀


既然粘包是因为接收方不知道消息界限 , 那么我们就自己创建界限

### low方法  🍀

我们只需要对上一篇中` subprocess_server.py `以及` subprocess_client.py` 做一点点修改就行了

subprocess_server_development.py

```python
import socket
import subprocess
sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('127.0.0.1', 8080))
sock.listen(5)
while True:
    print("Waitting for connection...")
    conn, addr = sock.accept()
    print("{}successful connection...".format(addr))
    while True:
      # 接收指令
        cmd = conn.recv(1024)
        if not cmd:
            print("Client is disconnected...")
            break
        print("The command is {}".format(cmd.decode()))
        # 获取执行结果
        data = subprocess.Popen(cmd.decode(),shell=True,
                                stdout=subprocess.PIPE,
                                stdin=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        # 获取错误句柄
        err = data.stderr.read()
        if err:
            res = err
        else:
            res = data.stdout.read()
        # 发送数据长度
        conn.send(str(len(res)).encode('utf-8'))
        # 防止与两次发送数据粘在一起
        ready = conn.recv(1024)
        if ready == b'OK':
            # sendall连续调用send完成发送
            conn.sendall(res)
    conn.close()
sock.close()
```

subprocess_client_development.py

```python
import socket
sock = socket.socket()
sock.connect(('127.0.0.1', 8080))
while True:
    cmd = input("Please input the command:").strip()
    if not cmd:
        print("Can't empty...")
        continue
    elif cmd == 'exit':
        break
    # 发送指令
    sock.send(cmd.encode('utf-8'))
    # 获取数据长度
    length = sock.recv(1024).decode('utf-8')
    # 发送标志
    sock.send(b'OK')
    recvsize = 0
    data = b''
    # 循环接收
    while recvsize < int(length):
        recvdata = sock.recv(1024)
        recvsize += len(recvdata)
        data += recvdata
    print(data.decode('gbk'))
sock.close()
```

利用这种方式 , 我们需要提前先将数据大小发送过去 , 这无疑会放大网络延迟带来的性能损耗

### 制作报头  🍀

既然需要将大小发送过去 , 那我们是不是可以为字节流加上自定义固定长度报头 , 报头中包换数据大小等信息 , 然后一次直接发送过去 , 对方只要在接收的时候先从取出报头 , 再取数据 

所以我们只需要固定好报头的长度可以了 , 我们可以利用struct模块来制作报头 , 只需对上方法稍作修改

subprocess_struct_server.py

```python
import socket,struct
import subprocess
sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('127.0.0.1', 8080))
sock.listen(5)
while True:
    print("Waitting for connection...")
    conn, addr = sock.accept()
    print("{}successful connection...".format(addr))
    while True:
        cmd = conn.recv(1024)
        if not cmd:
            print("Client is disconnected...")
            break
        print("The command is {}".format(cmd.decode()))
        data = subprocess.Popen(cmd.decode(),shell=True,
                                stdout=subprocess.PIPE,
                                stdin=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        err = data.stderr.read()
        if err:
            res = err
        else:
            res = data.stdout.read()
        # 制作4位固定报头并发送
        conn.send(struct.pack('i', len(res)))
        # 直接循环发送
        conn.sendall(res)
    conn.close()
sock.close()
```

subprocess_struct_client.py

```python
import socket,struct
sock = socket.socket()
sock.connect(('127.0.0.1', 8080))
while True:
    cmd = input("Please input the command:").strip()
    if not cmd:
        print("Can't empty...")
        continue
    elif cmd == 'exit':
        break
    sock.send(cmd.encode('utf-8'))
    res = sock.recv(4)
    # 解开报头取出数据长度
    length = struct.unpack('i', res)[0]
    recvsize = 0
    data = b''
    # 循环接收
    while recvsize < length:
        data += sock.recv(1024)
        recvsize += len(data)
    print(data.decode('gbk'))
sock.close()
```