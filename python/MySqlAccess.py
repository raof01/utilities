#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mysql import connector
from mysql.connector import MySQLConnection

default_host = 'localhost'
default_port = 8889

class MySqlAccess:
    '''
    Wrapper class to access MySQL DB using mysql connector/python
    '''    
    def __init__(self, db_host = default_host, db_port = default_port):
        self.__conn = MySQLConnection(host = db_host,
                                      port = db_port)
    
    def connect(self, user_name = None, user_passwd = None):
        if (user_name is None) and (user_passwd is None):
            return None
        self.__conn.connect(user = user_name, password = user_passwd)
        return 0
    
    def disconnect(self):
        self.__conn.close()

    def query(self, sql_stmt = None):
        cursor = self.__conn.cursor()
        query = sql_stmt
        cursor.execute(query)
        for row in cursor:
            print(row)
        cursor.close()

if __name__ == '__main__':
    dbAccess = MySqlAccess()
    if dbAccess.connect('test', 'test123') is None:
        print("error connecting")

    select_sql = '''SELECT * FROM test_DB.Products'''
    dbAccess.query(select_sql)
    dbAccess.disconnect()