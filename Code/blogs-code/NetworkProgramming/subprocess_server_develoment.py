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
        err = data.stderr.read()
        if err:
            res = err
        else:
            res = data.stdout.read()
        length = conn.send(str(len(res)).encode('utf-8'))
        ready = conn.recv(1024)
        if ready == b'OK':
            conn.sendall(res)
    conn.close()
sock.close()



