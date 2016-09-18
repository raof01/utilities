#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import platform
from PyQt5.QtWidgets import QMainWindow, QApplication, QTreeView, QAction, qApp, QMenuBar, QMenu
from PyQt5.QtGui import QIcon
sys.path.append('.')
from DialogConnectToDatabase import DialogConnectToDataBase

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
        
    def initUI(self):
        self.__initMenuBar()
        self.statusBar()
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('MySqlDbClient')
        self.show()

    def __createConnectAction(self):
        connectAction = QAction(QIcon('connect.png'), '&Connect...', self)
        connectAction.setStatusTip('Connect to Database')
        connectAction.triggered.connect(self.__openConnectionDialog)
        return connectAction

    def __createQuitAction(self):
        quitAction = QAction(QIcon('exit.png'), '&Exit', self)
        quitAction.setShortcut('Ctrl+Q')
        quitAction.setStatusTip('Exit Application')
        quitAction.triggered.connect(qApp.quit)
        return quitAction

    def __initMenuBar(self):
        menubar = self.menuBar()
        if platform.system() == 'Darwin':
            menubar.setNativeMenuBar(False) # Very important for Mac OS X
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(self.__createConnectAction())
        fileMenu.addAction(self.__createQuitAction())

    def __openConnectionDialog(self):
        self.__connDialog = DialogConnectToDataBase()
        self.__connDialog.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())