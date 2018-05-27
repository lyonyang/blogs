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
        cursor.execute("DROP TABLE IF EXISTS EMPLOYEE;")
        sql = """CREATE TABLE EMPLOYEE (
                 FIRST_NAME  CHAR(20) NOT NULL,
                 LAST_NAME  CHAR(20),
                 AGE INT,
                 SEX CHAR(1),
                 INCOME FLOAT );"""
        cursor.executemany(sql)
    connection.commit()
finally:
    connection.close()