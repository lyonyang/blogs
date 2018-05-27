#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import socketserver

class MyServer(socketserver.BaseRequestHandler):

    def handle(self):
        # 创建一个链接,继承于socketserver中的BaseRequestHandler类
        conn = self.request
        conn.sendall(bytes("Welcome to login...", encoding="utf-8"))
        print("Client connect...")
        while True:
            # 输出等待客户端发送内容
            print("Waitting for recving message...")
            # 接收客户端发送过来的内容
            message = conn.recv(1024)
            # 输出用户发送过来的内容
            print(message.decode('utf-8'))
            # 如果用户输入的是q
            if message == "exit":
                break
            # 给客户端发送内容
            data = input("Reply message:")
            conn.sendall(data.encode('utf-8'))
if __name__ == "__main__":
    server = socketserver.ThreadingTCPServer(('127.0.0.1', 999, ), MyServer)
    server.serve_forever()

