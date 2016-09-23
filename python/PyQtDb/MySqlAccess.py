#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mysql.connector import errors
from mysql.connector import MySQLConnection

default_host = 'localhost'
default_port = 8889


class MySqlAccess:
    """
    Wrapper class to access MySQL DB using mysql connector/python
    """

    def __init__(self, db_host=default_host, db_port=default_port):
        self._conn = MySQLConnection(host=db_host,
                                     port=db_port)

    def connect(self, user_name=None, user_password=None) -> bool:
        if (user_name is None) or (user_password is None):
            return False
        try:
            self._conn.connect(user=user_name, password=user_password)
        except errors.ProgrammingError:
            return False
        return True

    def disconnect(self):
        self._conn.close()

    def query(self, sql_stmt=None) -> [list]:
        cursor = self._conn.cursor()
        query = sql_stmt
        cursor.execute(query)
        l = []
        for row in cursor:
            l.append(row)
        cursor.close()
        return l
