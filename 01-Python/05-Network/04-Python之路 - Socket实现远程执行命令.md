# Python之路 - Socket实现远程执行命令

## os模块实现  🍀

osssh_server.py

```python
# 导入socket模块
import socket
# 导入os模块
import os
# 创建套接字对象
sock = socket.socket()
# 重置ip和端口
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# 绑定ip和端口
sock.bind(('127.0.0.1', 8080))
# 监听
sock.listen(5)
# 链接循环
while True:
    print("Waitting for connection...")
    # 阻塞
    conn, addr = sock.accept()
    print("{}successful connection...".format(addr))
    while True:
        cmd = conn.recv(1024)
        # 接收为空说明客户端断开了连接
        if not cmd:
            print("Client is disconnected...")
            break
        print("The command is {}".format(cmd.decode()))
        # 利用os模块进行系统调用,py3中popen参数为str,所以先decode
        data = os.popen(cmd.decode()).read()
        # 发送命令执行结果
        conn.send(data.encode('utf-8'))
    # 关闭链接
    conn.close()
# 关闭套接字
sock.close()
```

osssh_client.py

```python
# 导入socket模块
import socket
# 创建套接字对象
sock = socket.socket()
# 连接服务端
sock.connect(('127.0.0.1', 8080))
while True:
    cmd = input("Please input the command:").strip()
    if not cmd:
        print("Can't empty...")
        continue
    elif cmd == 'exit':
        break
    # 发送命令
    sock.send(cmd.encode('utf-8'))
    # 接收命令执行结果
    data = sock.recv(1024)
    print(data.decode('utf-8'))
# 关闭套接字
sock.close()
```

## subprocess模块实现  🍀

subprocess_server.py

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
        cmd = conn.recv(1024)
        if not cmd:
            print("Client is disconnected...")
            break
        print("The command is {}".format(cmd.decode()))
        # 利用subprocess模块进行系统调用
        data = subprocess.Popen(cmd.decode(),shell=True,
                                stdout=subprocess.PIPE,
                                stdin=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        stdout = data.stdout.read()
        stderr = data.stderr.read()
        # 打包执行结果
        res = stdout + stderr
        # 发送执行结果
        conn.send(res)
    conn.close()
sock.close()
```

subprocess_client.py

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
    sock.send(cmd.encode('utf-8'))
    data = sock.recv(1024)
    # Windows终端默认编码是gbk,所以得用gbk进行解码
    print(data.decode('gbk'))
sock.close()
```

以上两种方法实现了简单的ssh , 即远程执行命令 , 但是这两个都一个问题 , 当我们执行多次命令后 , 结果就不是我们想要得到了 , 它会发生粘包 , 即有可能上条命令的结果粘到这条命令的结果了 , 如何解决粘包问题 ? 下一篇整理