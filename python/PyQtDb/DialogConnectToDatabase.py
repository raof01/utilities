# -*- coding: utf-8 -*-

import sys
import socket
from PyQt5.QtWidgets import (QDialog, QPushButton, QLineEdit,
    QApplication, QHBoxLayout, QVBoxLayout, QLabel, QMessageBox)
from PyQt5.QtCore import QObject, QRect, pyqtSlot, pyqtSignal
import utilities
import platform
if platform.system() == 'Darwin':
    # MySQL Connector not available for Python v3.5 on windows
    sys.path.append('..')
    from MySqlAccess import MySqlAccess

class DialogConnectToDataBase(QDialog):
    '''
    Dialog for connecting to MySQL Database
    '''
    # Signals
    onDbConnected = pyqtSignal(str, MySqlAccess)
    onDbConnectedFailed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.__initConsts()
        self._initUI()
        self.__setDefaultValues()

    def __initConsts(self):
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
        
    def _initUI(self):
        vbox = QVBoxLayout()
        vbox.setSpacing(5)
        vbox.addLayout(self.__initAddressLayout())
        vbox.addLayout(self.__initUserNameLayout())
        vbox.addLayout(self.__initPasswordLayout())
        vbox.addLayout(self. __initButtonLayout())
        self.setLayout(vbox)
        self.setWindowTitle(self.__TITLE)
        self.setModal(True)
    
    def __initAddressLayout(self):
        hboxAddr = QHBoxLayout()
        hboxAddr
        self._leIpAddr = QLineEdit(self)
        self._lePort = QLineEdit(self)
        hboxAddr.addWidget(self.__LBL_IP)
        hboxAddr.addWidget(self._leIpAddr)
        hboxAddr.addWidget(self.__LBL_PORT)
        hboxAddr.addWidget(self._lePort)
        return hboxAddr

    def __initUserNameLayout(self):
        hboxUserName = QHBoxLayout()
        self._leUserName = QLineEdit(self)
        hboxUserName.addWidget(self.__LBL_USER_NAME)
        hboxUserName.addWidget(self._leUserName)
        return hboxUserName

    def __initPasswordLayout(self):
        hboxPasswd = QHBoxLayout()
        self._lePasswd = QLineEdit(self)
        self._lePasswd.setEchoMode(QLineEdit.Password)
        self._lePasswd.setGeometry(self._leUserName.geometry())
        self._lePasswd.move(self._lePasswd.geometry().top(),
                            self._leUserName.geometry().left())
        hboxPasswd.addWidget(self.__LBL_PASSWORD)
        hboxPasswd.addWidget(self._lePasswd)
        return hboxPasswd

    def __initButtonLayout(self):
        hboxBtns = QHBoxLayout()
        self._okButton = QPushButton(self.__CONNECT)
        self._okButton.clicked.connect(self.connectToDb)
        self._cancelButton = QPushButton(self.__CANCEL)
        self._cancelButton.clicked.connect(self.close)
        hboxBtns.addWidget(self._okButton)
        hboxBtns.addWidget(self._cancelButton)
        return hboxBtns
    
    def __setDefaultValues(self):
        self._leIpAddr.setText(self.__DEFAULT_IP)
        self._lePort.setText(self.__DEFAULT_PORT)
        self._leUserName.setText(self.__DEFAULT_USER)
        self._lePasswd.setText(self.__DEFAULT_PASSWD)

    @pyqtSlot()
    def connectToDb(self):
        if not self.__validInput():
            return
        if platform.system() == 'Darwin':
            dbAccess = MySqlAccess(self._leIpAddr.text(), int(self._lePort.text()))
            if dbAccess.connect(self._leUserName.text(), self._lePasswd.text()) != 0:
                self.onDbConnectedFailed.emit(self._leIpAddr.text() + self.__DELIMITER + self._lePort.text())
            else:
                self.onDbConnected.emit(self._leIpAddr.text() + self.__DELIMITER + self._lePort.text(), dbAccess)
        else:
            self.onDbConnectedFailed.emit(self._leIpAddr.text() + self.__DELIMITER + self._lePort.text() + ': Not supported')
        self.close()

    def __validInput(self):
        if not utilities.validIpAddress(self._leIpAddr.text()):
            utilities.showErrorMsgBox(self, self.__ERR_MSG_INVALID_IP +
                                    self._leIpAddr.text())
            return False
        
        if not utilities.validPort(self._lePort.text()):
            utilities.showErrorMsgBox(self, self.__ERR_MSG_INVALID_PORT +
                                    self._lePort.text())
            return False

        if len(self._leUserName.text()) == 0:
            utilities.showErrorMsgBox(self, self.__ERR_MSG_INVALID_USER)
            return False

        if len(self._lePasswd.text()) == 0:
            utilities.showErrorMsgBox(self, self.__ERR_MSG_INVALID_PASSWD)
            return False
        return True
