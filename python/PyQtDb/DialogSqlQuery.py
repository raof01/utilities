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

    def __init__(self, db_access):
        super().__init__()
        self.__init_consts()
        self._init_ui()
        self._db_access = db_access

    def __init_consts(self):
        self.__LBL_SQL_QUERY= QLabel('SQL: ')
        self.__LBL_SQL_TEMPLATES = QLabel('Templates: ')
        self.__TITLE = 'SQL Query'
        self.__GO = 'Go'
        self.__CANCEL = 'Cancel'
        self.__SELECT = 'Select'
        self.__UPDATE = 'Update'
        self.__DELETE = 'Delete'
        self.__INSERT = 'Insert'
        self.__WIDTH = 800
        self.__HEIGHT = 600
        self.__SQL_INPUT_HEIGHT = 100

    def _init_ui(self):
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
        self.__go_button = QPushButton(self.__GO)
        self.__cancel_button = QPushButton(self.__CANCEL)
        hbox_layout = QHBoxLayout()
        hbox_layout.addWidget(self.__LBL_SQL_QUERY)
        hbox_layout.addWidget(self.__go_button)
        hbox_layout.addWidget(self.__cancel_button)
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
