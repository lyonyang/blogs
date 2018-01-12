#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
import pymysql.cursors
# Connect to the database
connection = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='myroot',
                             db='mydatabase',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
try:
    with connection.cursor() as cursor:
        sql = "UPDATE user_info SET password = '456' WHERE username = 'Lyon'"
        effect_row = cursor.execute(sql)
        print(effect_row)
    connection.commit()
except:
    # 发生错误时回滚
    connection.rollback()
connection.close()