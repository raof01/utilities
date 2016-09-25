# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QDialog, QPushButton, QLineEdit,
                             QHBoxLayout, QVBoxLayout, QLabel, QMessageBox)
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

    def __init__(self):
        super().__init__()
        self.__init_consts()
        self._init_ui()
        self.__set_default_values()

    def __init_consts(self):
        self.__LBL_SQL_QUERY= QLabel('SQL')
        self.__LBL_SQL_RESULTS = QLabel('Results')
        self.__TITLE = 'SQL Query'
        self.__GO = 'Go'
        self.__CANCEL = 'Cancel'

    def _init_ui(self):
        self.setWindowTitle(self.__TITLE)
        self.setModal(True)

    def __init_button_layout(self) -> QHBoxLayout:
        hbox_btns = QHBoxLayout()
        self.__go_button = QPushButton(self.__GO)
        #self.__go_button.clicked.connect(self.connect_to_db)
        self._cancelButton = QPushButton(self.__CANCEL)
        #self._cancelButton.clicked.connect(self.close)
        hbox_btns.addWidget(self.__go_button)
        hbox_btns.addWidget(self._cancelButton)
        return hbox_btns
