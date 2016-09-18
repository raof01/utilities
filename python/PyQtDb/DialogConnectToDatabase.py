# -*- coding: utf-8 -*-

import sys
import socket
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit,
    QApplication, QHBoxLayout, QVBoxLayout, QLabel, QMessageBox)
from PyQt5.QtCore import QRect, pyqtSlot
import utilities

class DialogConnectToDataBase(QWidget):
    
    def __init__(self):
        super().__init__()
        self.__initConsts()
        self._initUI()

    def __initConsts(self):
        self.__LBL_USER_NAME = QLabel('UserName: ')
        self.__LBL_PASSWORD = QLabel('Password: ')
        self.__DIALOG_GEOMETRY = QRect(300, 300, 300, 120)
        self.__LBL_IP = QLabel('IP: ')
        self.__LBL_PORT = QLabel('Port: ')
        self.__TITLE = 'Connect to Database'
        self.__CONNECT = 'Connect'
        self.__CANCEL = 'Cancel'
        
    def _initUI(self):
        vbox = QVBoxLayout()
        vbox.setSpacing(5)
        vbox.addLayout(self.__initAddressLayout())
        vbox.addLayout(self.__initUserNameLayout())
        vbox.addLayout(self.__initPasswordLayout())
        vbox.addLayout(self. __initButtonLayout())
        self.setLayout(vbox)
        #self.setGeometry(self.__DIALOG_GEOMETRY)
        self.setWindowTitle(self.__TITLE)
    
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
        self._okButton.clicked.connect(self.saveValues)
        self._cancelButton = QPushButton(self.__CANCEL)
        self._cancelButton.clicked.connect(self.close)
        hboxBtns.addWidget(self._okButton)
        hboxBtns.addWidget(self._cancelButton)
        return hboxBtns

    @pyqtSlot()
    def saveValues(self):
        if not self.__validInput():
            return
        # TODO: Save user input
        self.close()

    def __validInput(self):
        if not utilities.validIpAddress(self._leIpAddr.text()):
            utilities.showErrorMsgBox(self, 'Invalid IP Address: ' +
                                    self._leIpAddr.text())
            return False
        
        if not utilities.validPort(self._lePort.text()):
            utilities.showErrorMsgBox(self, 'Invalid Port: ' +
                                    self._lePort.text())
            return False

        if len(self._leUserName.text()) == 0:
            utilities.showErrorMsgBox(self, 'User name must not be empty')
            return False

        if len(self._lePasswd.text()) == 0:
            utilities.showErrorMsgBox(self, 'Password must not be empty')
            return False
        return True
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DialogConnectToDataBase()
    ex.show()
    sys.exit(app.exec_())