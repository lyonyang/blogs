#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import socket
sock = socket.socket(type=socket.SOCK_DGRAM)
sock.bind(('127.0.0.1', 8080))
while True:
    print("Waitting informations...")
    data, addr = sock.recvfrom(1024)
    if not data:
        continue
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