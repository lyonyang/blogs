# Python之路 - Socket实现QQ聊天

## 介绍  🍀

在上一篇中写了最基本版的socket服务端和客户端 , 即仅能通信一次后就自动关闭了 , 显然实际应用中可不是这样的 , 那就来写一个像QQ一样的聊天程序吧

## TCP实现  🍀

因为TCP是有链接的 , 这就导致只能有一个服务端 , 但是可以有多个客户端

tcpqq_server.py

```python
import socket
sock = socket.socket()
sock.bind(('127.0.0.1', 8080))
sock.listen(5)
# 实现链接循环
while True:
    print("Watiting for the link...")
    conn, addr = sock.accept()
    print("Your friend {} is online...".format(addr))
    # 实现通信循环
    while True:
        messages = conn.recv(1024)
        print("Messages from [{}]:{}".format(addr, messages.decode('utf-8')))
        if messages == b'q':
            break
        else:
            while True:
                data = input("Please input the messages to be sent:").strip().encode('utf-8')
                # 注意发送的内容不能为空,否则接收方就会一直等下去
                if not data:
                    print("Can't be empty...")
                    continue
                conn.send(data)
                break
    print("Your friend {} is offline...".format(addr))
    conn.close()
sock.close()
```

tcpqq_client.py

```python
import socket
sock = socket.socket()
sock.connect(('127.0.0.1', 8080))
# 实现通信循环
while True:
    messages = input("Please input your messages to be sent:").strip().encode('utf-8')
    # 注意发送的内容不能为空,否则接收方就会一直等下去
    if not messages:
        print("Can't be empty...")
        continue
    elif messages == b'q':
    	break
    else:
    	sock.send(messages)
        data = sock.recv(1024)
        print("Messages from [{}]:{}".format(('127.0.0.1', 8080), data.decode('utf-8')))
sock.close()
```

当然实际应用中是不会用TCP来完成的 , 而是用UDP , 这里只是模拟 , 并且以上还有有问题没有解决的 , 比如如果发送的消息大于1024字节 , 那么就不能完整接收信息了 , 后续再进行处理 

TCP版本的服务端可以允许同时连入5个客户端 , 值得注意的是并不是同时连入 , 按照顺序排队 , 只有前面的人说完了会连入后序的客户端

## UDP实现  🍀

以为UDP是无链接的 , 所以它可以实现想跟谁说话就跟谁说话

udpqq_server.py

```python
import socket
sock = socket.socket(type=socket.SOCK_DGRAM)
sock.bind(('127.0.0.1', 8080))
# 实现通信循环
while True:
    data, addr = sock.recvfrom(1024)
    print("Receive a message from {}:{}".format(addr, data.decode('utf-8')))
    if data == b'q':
        break
    while True:
        messages = input("Please input the messages to be sent:").strip().encode('utf-8')
        if not messages:
            print("Can't be empty...")
            continue
        sock.sendto(messages, addr)
        break
sock.close()
```

udpqq_client.py

```python
import socket
sock = socket.socket(type=socket.SOCK_DGRAM)
# 实现通信循环
while True:
    messages = input("Please input your messages to be sent:").strip().encode('utf-8')
    if not messages:
        print("Can't be empty...")
        continue
    elif messages == b'q':
        break
    else:
        sock.sendto(messages, ('127.0.0.1',8080))
        data, addr = sock.recvfrom(1024)
        print("Receive a message from {}:{}".format(addr, data.decode('utf-8')))
sock.close()
```

利用UDP实现才更接近现实 , 我们只需要知道他的ip和端口 , 我们就可以跟他讲话 , 在他即可以是服务端 , 也可以是客户端 , 不过必须注意接收和发送流程的问题

以上两种实现方式 , 都只是最基础的版本 , 在UDP中我们可以将所有人的ip和端口放到一个字典里或者其他存储里 , 利用ip和端口就可以实现跟所有人进行聊天了

