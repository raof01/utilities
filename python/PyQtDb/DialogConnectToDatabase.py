# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QDialog, QPushButton, QLineEdit,
                             QHBoxLayout, QVBoxLayout, QLabel)
from PyQt5.QtCore import QRect, pyqtSlot, pyqtSignal
import utilities
import platform

if platform.system() == 'Darwin':
    # MySQL Connector not available for Python v3.5 on windows
    sys.path.append('..')
    from MySqlAccess import MySqlAccess


class DialogConnectToDataBase(QDialog):
    """
    Dialog for connecting to MySQL Database
    """
    # Signals
    if platform.system() == 'Darwin':
        onDbConnected = pyqtSignal(str, MySqlAccess)
    onDbConnectedFailed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.__init_consts()
        self._init_ui()
        self.__set_default_values()

    def __init_consts(self):
        self.__LBL_USER_NAME = QLabel('UserName: ')
        self.__LBL_PASSWORD = QLabel('Password: ')
        self.__DIALOG_GEOMETRY = QRect(300, 300, 300, 120)
        self.__LBL_IP = QLabel('IP: ')
        self.__LBL_PORT = QLabel('Port: ')
        self.__TITLE = 'Connect to Database'
        self.__CONNECT = 'Connect'
        self.__CANCEL = 'Cancel'
        self.__ERR_MSG_INVALID_IP = 'Invalid IP Address: '
        self.__ERR_MSG_INVALID_PORT = 'Invalid Port: '
        self.__ERR_MSG_INVALID_USER = 'User name must not be empty'
        self.__ERR_MSG_INVALID_PASSWD = 'Password must not be empty'
        self.__DEFAULT_IP = 'localhost'
        self.__DEFAULT_PORT = '8889'
        self.__DEFAULT_USER = 'test'
        self.__DEFAULT_PASSWD = 'test123'
        self.__DELIMITER = ':'

    def _init_ui(self):
        vbox = QVBoxLayout()
        vbox.setSpacing(5)
        vbox.addLayout(self.__init_address_layout())
        vbox.addLayout(self.__init_user_name_layout())
        vbox.addLayout(self.__init_password_layout())
        vbox.addLayout(self.__init_button_layout())
        self.setLayout(vbox)
        self.setWindowTitle(self.__TITLE)
        self.setModal(True)

    def __init_address_layout(self) -> QHBoxLayout:
        hbox_addr = QHBoxLayout()
        hbox_addr
        self._leIpAddr = QLineEdit(self)
        self._lePort = QLineEdit(self)
        hbox_addr.addWidget(self.__LBL_IP)
        hbox_addr.addWidget(self._leIpAddr)
        hbox_addr.addWidget(self.__LBL_PORT)
        hbox_addr.addWidget(self._lePort)
        return hbox_addr

    def __init_user_name_layout(self) -> QHBoxLayout:
        hbox_user_name = QHBoxLayout()
        self._leUserName = QLineEdit(self)
        hbox_user_name.addWidget(self.__LBL_USER_NAME)
        hbox_user_name.addWidget(self._leUserName)
        return hbox_user_name

    def __init_password_layout(self) -> QHBoxLayout:
        hbox_passwd = QHBoxLayout()
        self._lePasswd = QLineEdit(self)
        self._lePasswd.setEchoMode(QLineEdit.Password)
        self._lePasswd.setGeometry(self._leUserName.geometry())
        self._lePasswd.move(self._lePasswd.geometry().top(),
                            self._leUserName.geometry().left())
        hbox_passwd.addWidget(self.__LBL_PASSWORD)
        hbox_passwd.addWidget(self._lePasswd)
        return hbox_passwd

    def __init_button_layout(self) -> QHBoxLayout:
        hbox_btns = QHBoxLayout()
        self._okButton = QPushButton(self.__CONNECT)
        self._okButton.clicked.connect(self.connect_to_db)
        self._cancelButton = QPushButton(self.__CANCEL)
        self._cancelButton.clicked.connect(self.close)
        hbox_btns.addWidget(self._okButton)
        hbox_btns.addWidget(self._cancelButton)
        return hbox_btns

    def __set_default_values(self):
        self._leIpAddr.setText(self.__DEFAULT_IP)
        self._lePort.setText(self.__DEFAULT_PORT)
        self._leUserName.setText(self.__DEFAULT_USER)
        self._lePasswd.setText(self.__DEFAULT_PASSWD)

    @pyqtSlot()
    def connect_to_db(self):
        if not self.__validate_input():
            return
        if platform.system() == 'Darwin':
            db_access = MySqlAccess(self._leIpAddr.text(), int(self._lePort.text()))
            if not db_access.connect(self._leUserName.text(), self._lePasswd.text()):
                self.onDbConnectedFailed.emit(self._leIpAddr.text() +
                                              self.__DELIMITER +
                                              self._lePort.text())
            else:
                self.onDbConnected.emit(self._leIpAddr.text() +
                                        self.__DELIMITER +
                                        self._lePort.text(), db_access)
        else:
            self.onDbConnectedFailed.emit(self._leIpAddr.text() +
                                          self.__DELIMITER +
                                          self._lePort.text() + ': Not supported')
        self.close()

    def __validate_input(self) -> bool:
        if not utilities.valid_ip_address(self._leIpAddr.text()):
            utilities.show_error_message_box(self, self.__ERR_MSG_INVALID_IP +
                                             self._leIpAddr.text())
            return False

        if not utilities.valid_port(self._lePort.text()):
            utilities.show_error_message_box(self, self.__ERR_MSG_INVALID_PORT +
                                             self._lePort.text())
            return False

        if len(self._leUserName.text()) == 0:
            utilities.show_error_message_box(self, self.__ERR_MSG_INVALID_USER)
            return False

        if len(self._lePasswd.text()) == 0:
            utilities.show_error_message_box(self, self.__ERR_MSG_INVALID_PASSWD)
            return False
        return True
