#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
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
