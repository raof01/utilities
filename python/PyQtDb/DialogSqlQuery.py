# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QDialog, QPushButton, QPlainTextEdit, QTableView,
                             QHBoxLayout, QVBoxLayout, QLabel)
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import utilities
import platform

if platform.system() == 'Darwin':
    # MySQL Connector not available for Python v3.5 on windows
    sys.path.append('..')
    from MySqlAccess import MySqlAccess


class DialogSqlQuery(QDialog):
    """
    Dialog for Sql query
    """
    # Slots
    @pyqtSlot()
    def __populate_select_template(self):
        self.__sql_input.setPlainText(self.__db_access.compose_select(self.__db_name,
                                                                      self.__table_name,
                                                                      self.__columns,
                                                                      self.__columns[0]))

    @pyqtSlot()
    def __populate_update_template(self):
        self.__sql_input.setPlainText(self.__db_access.compose_update(self.__db_name,
                                                                      self.__table_name,
                                                                      self.__columns))

    @pyqtSlot()
    def __execute_query(self):
        sql = self.__sql_input.toPlainText()
        if sql == '':
            return
        self.__action_dict[[p for p in sql.split(' ') if p != ''][0]]()
        self.__output.model().setColumnCount(len(self.__columns))
        for (i, v) in zip(range(len(self.__columns)), self.__columns):
            self.__output.model().setHeaderData(i, Qt.Horizontal, v)
        lst = self.__db_access.query(sql)
        for values in lst:
            items = []
            for v in values:
                items.append(QStandardItem(str(v)))
            self.__output.model().appendRow(items)

    @pyqtSlot()
    def __clear_query_input(self):
        self.__sql_input.clear()

    @pyqtSlot()
    def __populate_delete_template(self):
        self.__sql_input.setPlainText(self.__db_access.compose_delete(self.__db_name, self.__table_name))

    @pyqtSlot()
    def __populate_insert_template(self):
        self.__sql_input.setPlainText(self.__db_access.compose_insert(self.__db_name, self.__table_name, self.__columns))

    @staticmethod
    def none_to_space(s=None) -> str:
        if s is None:
            return ' '
        return s

    def __init__(self, db_access, table_name, db_name, columns):
        super().__init__()
        self.__init_consts()
        self.__init_ui()
        self.__db_access = db_access
        self.__table_name = self.none_to_space(table_name)
        self.__db_name = self.none_to_space(db_name)
        self.__columns = self.none_to_space(columns)
        self.__setup_output_creation()

    def __setup_output_creation(self) -> {dict}:
        return {
            self.__SELECT: self.__create_treeview_output,
            self.__UPDATE: self.__create_plaintext_output,
            self.__DELETE: self.__create_plaintext_output,
            self.__INSERT: self.__create_plaintext_output
        }

    def __create_treeview_output(self):
        self.__output = QTableView()
        self.__output.setModel(QStandardItemModel())

    def __create_plaintext_output(self):
        self.__output = QPlainTextEdit()

    def __init_consts(self):
        self.__LBL_SQL_QUERY= QLabel('SQL: ')
        self.__LBL_SQL_TEMPLATES = QLabel('Templates: ')
        self.__TITLE = 'SQL Query'
        self.__GO = 'Go'
        self.__CLEAR = 'Clear'
        self.__CANCEL = 'Cancel'
        self.__SELECT = 'SELECT'
        self.__UPDATE = 'UPDATE'
        self.__DELETE = 'DELETE'
        self.__INSERT = 'INSERT'
        self.__WIDTH = 800
        self.__HEIGHT = 600
        self.__SQL_INPUT_HEIGHT = 100

    def __init_ui(self):
        self.setLayout(self.__init_layout())
        self.__setup_event_handlers()
        self.setWindowTitle(self.__TITLE)
        self.setFixedWidth(self.__WIDTH)
        self.setFixedHeight(self.__HEIGHT)
        self.setModal(True)
        self.__action_dict = self.__setup_output_creation()

    def __init_sql_template_button_layout(self) -> QHBoxLayout:
        self.__select_button = QPushButton(self.__SELECT)
        self.__update_button = QPushButton(self.__UPDATE)
        self.__delete_button = QPushButton(self.__DELETE)
        self.__insert_button = QPushButton(self.__INSERT)
        hbox_layout = QHBoxLayout()
        hbox_layout.addWidget(self.__LBL_SQL_TEMPLATES)
        hbox_layout.addWidget(self.__select_button)
        hbox_layout.addWidget(self.__update_button)
        hbox_layout.addWidget(self.__delete_button)
        hbox_layout.addWidget(self.__insert_button)
        return hbox_layout

    def __init_sql_query_layout(self) -> QHBoxLayout:
        self.__clear_button = QPushButton(self.__CLEAR)
        self.__go_button = QPushButton(self.__GO)
        self.__cancel_button = QPushButton(self.__CANCEL)
        hbox_layout = QHBoxLayout()
        hbox_layout.addWidget(self.__LBL_SQL_QUERY)
        hbox_layout.addWidget(self.__go_button)
        hbox_layout.addWidget(self.__cancel_button)
        hbox_layout.addWidget(self.__clear_button)
        return hbox_layout

    def __init_layout(self) -> QVBoxLayout:
        self.__sql_input = QPlainTextEdit()
        self.__sql_input.setFixedHeight(self.__SQL_INPUT_HEIGHT)
        self.__output = QPlainTextEdit()
        vbox = QVBoxLayout()
        vbox.addLayout(self.__init_sql_query_layout())
        vbox.addWidget(self.__sql_input)
        vbox.addLayout(self.__init_sql_template_button_layout())
        vbox.addWidget(self.__output)
        return vbox

    def __setup_event_handlers(self):
        self.__cancel_button.clicked.connect(self.close)
        self.__select_button.clicked.connect(self.__populate_select_template)
        self.__go_button.clicked.connect(self.__execute_query)
        self.__clear_button.clicked.connect(self.__clear_query_input)
        self.__update_button.clicked.connect(self.__populate_update_template)
        self.__delete_button.clicked.connect(self.__populate_delete_template)
        self.__insert_button.clicked.connect(self.__populate_insert_template)
