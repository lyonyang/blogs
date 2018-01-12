#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import socket
sock = socket.socket()
sock.connect(('127.0.0.1',8080))
sock.send(b"I'm Lyon")
content = sock.recv(1024)
print(content.decode())
sock.close()
