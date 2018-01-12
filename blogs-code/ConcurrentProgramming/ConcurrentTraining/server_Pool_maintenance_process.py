#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import socket
import os
import multiprocessing
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('127.0.0.1', 8080))
server.listen(5)

def talk(conn, client_addr):
    print("Process pid : %s" % os.getpid())
    while True:
        try:
            msg = conn.recv(1024)
            if not msg:break
            conn.send(msg.upper())
        except Exception:
            break

if __name__ == '__main__':
    pool = multiprocessing.Pool()
    while True:
        conn, client_addr = server.accept()
        # 同步则一时间只有一个客户端能访问,所以使用异步
        pool.apply_async(talk,args=(conn, client_addr,))



















