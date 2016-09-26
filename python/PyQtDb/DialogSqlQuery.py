# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QDialog, QPushButton, QPlainTextEdit, QTableView,
                             QHBoxLayout, QVBoxLayout, QLabel)
from PyQt5.QtCore import pyqtSlot, pyqtSignal
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
        db_name = ' '
        table_name = ' '
        columns = ' '
        if self.__db_name is not None:
            db_name = self.__db_name
        if self.__table_name is not None:
            table_name = self.__table_name
        if self.__columns is not None:
            columns = self.__columns
        self.__sql_input.setPlainText(self.__db_access.compose_select(db_name, table_name, columns, columns[0]))

    @pyqtSlot()
    def __populate_update_template(self):
        pass

    @pyqtSlot()
    def __execute_query(self):
        self.__sql_input.setPlainText(str(self.__db_access.query(self.__sql_input.toPlainText())))

    @pyqtSlot()
    def __clear_query_input(self):
        self.__sql_input.clear()

    def __init__(self, db_access, table_name, db_name, columns):
        super().__init__()
        self.__init_consts()
        self.__init_ui()
        self.__db_access = db_access
        self.__table_name = table_name
        self.__db_name = db_name
        self.__columns = columns

    def __init_consts(self):
        self.__LBL_SQL_QUERY= QLabel('SQL: ')
        self.__LBL_SQL_TEMPLATES = QLabel('Templates: ')
        self.__TITLE = 'SQL Query'
        self.__GO = 'Go'
        self.__CLEAR = 'Clear'
        self.__CANCEL = 'Cancel'
        self.__SELECT = 'Select'
        self.__UPDATE = 'Update'
        self.__DELETE = 'Delete'
        self.__INSERT = 'Insert'
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
        self.__table_view = QTableView()
        vbox = QVBoxLayout()
        vbox.addLayout(self.__init_sql_query_layout())
        vbox.addWidget(self.__sql_input)
        vbox.addLayout(self.__init_sql_template_button_layout())
        vbox.addWidget(self.__table_view)
        return vbox

    def __setup_event_handlers(self):
        self.__cancel_button.clicked.connect(self.close)
        self.__select_button.clicked.connect(self.__populate_select_template)
        self.__go_button.clicked.connect(self.__execute_query)
        self.__clear_button.clicked.connect(self.__clear_query_input)
