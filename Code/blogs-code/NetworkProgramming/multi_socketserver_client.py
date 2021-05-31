#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import socket
sock = socket.socket()
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