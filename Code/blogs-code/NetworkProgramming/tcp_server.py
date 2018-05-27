#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import socket
sock = socket.socket()
sock.bind(('127.0.0.1', 8080))
sock.listen(5)
conn, addr = sock.accept()
print(conn,addr)
content = conn.recv(1024)
print(content.decode())
conn.send(b'Hello Lyon')
conn.close()
sock.close()