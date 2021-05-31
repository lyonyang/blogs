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
                             )
try:
    with connection.cursor() as cursor:
        sql = "SELECT * FROM emp"
        effect_row = cursor.execute(sql)
        print(effect_row)
        result = cursor.fetchall()
        print(result)
    connection.commit()
finally:
    connection.close()