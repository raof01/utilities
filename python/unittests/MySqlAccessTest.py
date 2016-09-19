#!/usr/bin/env python3

import sys
import unittest
from unittest import mock

sys.path.append('..')
from MySqlAccess import MySqlAccess

class MySqlAccessTest(unittest.TestCase):
    def setUp(self):
        self.__db_access = MySqlAccess()
        self.__use_mock = False
    
    def tearDown(self):
        if not self.__use_mock:
            self.__db_access.disconnect()
    
    def __mock_mysql_db(self):
        self.__use_mock = True
        self.__db_access.disconnect()
        self.__db_access._conn = mock.Mock()
    
    def __mock_mysql_db_connect(self):
        self.__db_access._conn.connect = mock.Mock()
    
    def test_connect_return_none_when_user_name_is_none(self):
        self.assertIsNone(self.__db_access.connect(user_passwd = 'passwd'))

    def test_connect_return_none_when_user_passwd_is_none(self):
        self.assertIsNone(self.__db_access.connect(user_name = 'user_name'))

    def test_connect_return_none_when_user_name_and_passwd_is_provided(self):
        self.__mock_mysql_db()
        self.__mock_mysql_db_connect()
        self.assertEqual(0, self.__db_access.connect(user_name = 'user_name',
                                                   user_passwd = 'passwd'))

    def test_query_to_real_db(self):
        '''
        WARNING!!! This should have MySQL DB set up
        '''
        if not self.__db_access.connect('test', 'test123') is None:
            #select_sql = '''SELECT * FROM test_DB.Products'''
            select_sql = '''SHOW DATABASES'''
            self.__db_access.query(select_sql)
            self.__db_access.disconnect()

if __name__ == '__main__':
    unittest.main()
