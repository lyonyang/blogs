#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8080))
while True:
    msg = input("Please input message:").strip()
    if not msg: continue
    client.send(msg.encode('utf-8'))
    data = client.recv(1024)
    print(data.decode('utf-8'))