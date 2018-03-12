# Python之路 - Socketserver实现多并发

## 阅读指引  🍀

在上面的整理篇章中 , 简单的网络编程基本已经会了 , 一个TCP , 一个UDP , 然后就是粘包问题

但是在上述中有一个问题 , 在现实生活中 , 一个服务端肯定常常需要同时服务好几个客户端 , 而上述篇章中并没有实现一对多同时进行的情况 , TCP中只能等前一个链接断开后续的才能连上 , 没连上就一直等 ; UDP则是接一次发一次 , 并不能同时接两次发两次 . 为了处理这个问题 , 即实现并发 (后续文章详细讲解) , Python中有一个socketserver模块可以满足我们的要求

## socketserver  🍀

Python提供了两个级别访问的网络服务:

1. 低级别的网络服务支持基本的socket , 它提供了标准的BSD Socket API , 可以访问底层操作系统Socket接口的全部方法
2. 高级别的网络服务模块socketserver , 它提供了服务器中心类 , 可以简化网络服务器的开发

socket就不用说了 , now socketserver

我们知道基于TCP的套接字 , 关键就是两个循环 , 一个链接循环(多人) , 一个通信循环(多消息)

在socketserver模块中分为两大类 : server类 (解决链接问题) 和request类 (解决通信问题) 

如果想进一步了解 , 可以看看官方文档 , < [socketserver官方文档 ](https://docs.python.org/3/library/socketserver.html?highlight=socketserver#module-socketserver)>

## 实现多并发  🍀

multi_socketserver_server.py

```python
import socketserver
class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        # 创建一个链接,继承于socketserver中的BaseRequestHandler类
        conn = self.request
        # 发送登录提示
        conn.sendall(b"Welcome to login...")
        print("Client connect...")
        while True:
            print("Waitting for recving message...")
            # 接收消息
            message = conn.recv(1024)
            print(message.decode('utf-8'))
            # 收到exit就退出
            if message == "exit":
                break
            # 回复消息
            data = input("Reply message:")
            # 发送消息
            conn.sendall(data.encode('utf-8'))
if __name__ == "__main__":
  　# 实例化
    server = socketserver.ThreadingTCPServer(('127.0.0.1', 999, ), MyServer)
    # 调用serve_forever方法
    server.serve_forever()
'''
def serve_forever(self, poll_interval=0.5):
	"""
	Handle one request at a time until shutdown.
    Polls for shutdown every poll_interval seconds. Ignores
    self.timeout. If you need to do periodic tasks, do them in
    another thread.
	"""
'''
```

multi_socketserver_client.py

```python
# 就是一个简单的TCP客户端
import socket
sock = socket.socket()
# 连接服务端
sock.connect(('127.0.0.1', 999, ))
login = sock.recv(1024)
print(login.decode('utf-8'))
while True:
    message = input("Please input the message:").strip()
    if message == "exit":
        sock.sendall(b'exit')
        break
    else:
        sock.sendall(message.encode('utf-8'))
        print("Waitting for recving message...")
        data = sock.recv(1024)
        print(data.decode('utf-8'))
sock.close()
```

到这里 , 我们成功实现了多并发 , 多并发是什么? 这就关系到操作系统中的进程和线程了 , 网络编程既然是实现两个进程间的通信 , 那么就逃不过进程 , 线程等了