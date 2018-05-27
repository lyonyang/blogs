#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
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
    length = sock.recv(1024).decode('utf-8')
    sock.send(b'OK')
    recvsize = 0
    data = b''
    while recvsize < int(length):
        data += sock.recv(1024)
        recvsize += len(data)
    print(data.decode('gbk'))
sock.close()
