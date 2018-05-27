#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
from gevent import monkey
monkey.patch_all()
import socket
import gevent

def server(server_ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((server_ip, port))
    s.listen(5)
    while True:
        conn, addr = s.accept()
        gevent.spawn(talk, conn, addr)

def talk(conn, addr):
    try:
        while True:
            res = conn.recv(1024)
            print('Client %s:%s msg: %s' % (addr[0], addr[1], res))
            conn.send(res.upper())
    except Exception as e:
        print(e)
    finally:
        conn.close()
if __name__ == '__main__':
    server('127.0.0.1', 8080)