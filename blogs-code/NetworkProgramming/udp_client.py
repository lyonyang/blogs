#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import socket
sock = socket.socket(type=socket.SOCK_DGRAM)
sock.sendto(b"I'm Lyon", ('127.0.0.1', 8090))
sock.close()