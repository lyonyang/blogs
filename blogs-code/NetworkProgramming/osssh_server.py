#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import socket
import os
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
        data = os.popen(cmd.decode()).read()
        conn.send(data.encode('utf-8'))
    conn.close()
sock.close()



