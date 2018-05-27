#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import tornado.ioloop
import tornado.web
import pymysql
class LoginHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('login.html')

    def post(self, *args, **kwargs):
        username = self.get_argument('username', None)
        pwd = self.get_argument('pwd', None)
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='as', db='sqldb')
        cursor = conn.cursor()
        temp = "select username from user_info where username='%s' and password = '%s'" % (username, pwd,)
        effect_row = cursor.execute(temp)
        result = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        if result:
            self.write('登录成功')
        else:
            self.write('登录失败')

application = tornado.web.Application([(r"/login", LoginHandler), ])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()