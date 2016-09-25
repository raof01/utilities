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
        self.__init_consts()
        self.__order = self.__SQL_ORDER_DESC
        self._conn = MySQLConnection(host=db_host,
                                     port=db_port)

    def __init_consts(self):
        # SQL
        self.__SQL_SHOW_DB = 'SHOW DATABASES'
        self.__SQL_SHOW_TABLES = 'SHOW TABLES IN '
        self.__SQL_SHOW_COLUMNS_FMT = 'SHOW COLUMNS IN {0} IN {1}'
        self.__SQL_USE_DATABASE = 'USE '
        self.__SQL_ORDER_DESC = ' DESC'
        self.__SQL_ORDER_ASC = ' ASC'
        self.__SQL_SELECT = 'SELECT '
        self.__SQL_COLUMN_SEP = ', '
        self.__SQL_FROM = ' FROM '
        self.__SQL_DOT = '.'
        self.__SQL_ORDER_BY = ' ORDER BY '

        # SQL templates
        self.SQL_TEMPLATE_SELECT = 'SELECT {0} FROM {1} WHERE 1'

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

    def get_database(self) -> [list]:
        return self.query(self.__SQL_SHOW_DB)

    def get_tables(self, db_name) -> [list]:
        return self.query(self.__SQL_SHOW_TABLES + db_name)

    def get_columns_of_table(self, db_name, table_name) -> [list]:
        return self.query(self.__SQL_SHOW_COLUMNS_FMT.format(table_name, db_name))

    def flip_order(self):
        if self.__order == self.__SQL_ORDER_DESC:
            self.__order = self.__SQL_ORDER_ASC
        else:
            self.__order = self.__SQL_ORDER_DESC

    def compose_select(self, db_name, table_name, columns, order_column) -> str:
        sql = self.__SQL_SELECT
        for v in columns:
            sql += v + self.__SQL_COLUMN_SEP
        query = sql[0:len(sql) - len(self.__SQL_COLUMN_SEP)]
        query += self.__SQL_FROM + db_name + self.__SQL_DOT + table_name
        query += self.__SQL_ORDER_BY + order_column + self.__order
        return query
