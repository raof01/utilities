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
        self.__invalid_db = False
        self.__order = self.__SQL_ORDER_DESC
        try:
            self._conn = MySQLConnection(host=db_host,
                                         port=db_port)
        except errors.InterfaceError:
            self.__invalid_db = True

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
        self.__SQL_UPDATE = 'UPDATE {0} SET '
        self.__SQL_WHERE = ' WHERE '
        self.__SQL_ASSIGN = '='
        self.__SQL_DELETE = 'DELETE FROM {0}'
        self.__SQL_INSERT = 'INSERT INTO {0}('
        self.__SQL_INSERT_VALUES = ') VALUES ('
        self.__SQL_INSERT_END = ')'
        self.__SQL_OPEN_BRACKET = '['
        self.__SQL_CLOSE_BRACKET = ']'
        self.__SQL_VALUE = 'value-'

        # SQL templates
        self.SQL_TEMPLATE_SELECT = 'SELECT {0} FROM {1} WHERE 1'

    def connect(self, user_name=None, user_password=None) -> bool:
        if (user_name is None) or (user_password is None) or self.__invalid_db:
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
        try:
            cursor.execute(query)
            l = [row for row in cursor]
        except errors.ProgrammingError:
            return None
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
        query = self.__remove_trailing_sep(sql)
        query += self.__SQL_FROM + db_name + self.__SQL_DOT + table_name
        query += self.__SQL_ORDER_BY + order_column + self.__order
        return query

    def compose_update(self, db_name, table_name, columns) -> str:
        sql = self.__SQL_UPDATE.format(db_name + self.__SQL_DOT + table_name)
        for (i, v) in zip(range(len(columns)), columns):
            sql += v + self.__SQL_ASSIGN
            sql += self.__SQL_OPEN_BRACKET + self.__SQL_VALUE + str(i + 1) + self.__SQL_CLOSE_BRACKET
            sql += self.__SQL_COLUMN_SEP
        query = self.__remove_trailing_sep(sql)
        query += self.__SQL_WHERE
        return query

    def compose_delete(self, db_name, table_name) -> str:
        sql = self.__SQL_DELETE.format(db_name + self.__SQL_DOT + table_name)
        sql += self.__SQL_WHERE
        return sql

    def compose_insert(self, db_name, table_name, columns) ->str:
        sql = self.__SQL_INSERT.format(db_name + self.__SQL_DOT + table_name)
        values = ''
        for (i, v) in zip(range(len(columns)), columns):
            sql += v + self.__SQL_COLUMN_SEP
            values += self.__SQL_OPEN_BRACKET + self.__SQL_VALUE + str(i + 1) + self.__SQL_CLOSE_BRACKET
            values += self.__SQL_COLUMN_SEP
        query = self.__remove_trailing_sep(sql) + self.__SQL_INSERT_VALUES
        values = self.__remove_trailing_sep(values)
        query += values + self.__SQL_INSERT_END
        return query

    def __remove_trailing_sep(self, s) -> str:
        if len(s) <= len(self.__SQL_COLUMN_SEP):
            return ''
        return s[0:len(s) - len(self.__SQL_COLUMN_SEP)]
