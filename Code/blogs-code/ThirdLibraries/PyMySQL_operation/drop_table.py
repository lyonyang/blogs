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
        sql = "DROP TABLE EMPLOYEE"
        cursor.execute(sql)
    connection.commit()
finally:
    connection.close()