#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
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
        data = subprocess.Popen(cmd.decode(),shell=True,
                                stdout=subprocess.PIPE,
                                stdin=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        stdout = data.stdout.read()
        stderr = data.stderr.read()
        res = stdout + stderr
        conn.send(res)
    conn.close()
sock.close()



