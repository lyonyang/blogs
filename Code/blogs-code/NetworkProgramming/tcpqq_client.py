#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import socket
sock = socket.socket()
sock.connect(('127.0.0.1', 8080))
while True:
    messages = input("Please input your messages to be sent:").strip().encode('utf-8')
    if not messages:
        print("Can't be empty...")
        continue
    sock.send(messages)
    if messages == b'q':
        break
    else:
        data = sock.recv(1024)
        print("Messages from [{}]:{}".format(('127.0.0.1', 8080), data.decode('utf-8')))
sock.close()