#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import platform
from PyQt5.QtWidgets import QMainWindow, QApplication, QTreeView, QAction, qApp, QMenuBar, QMenu
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from DialogConnectToDatabase import DialogConnectToDataBase

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.__initConstants()
        self.initUI()
        
    def __initConstants(self):
        self.__TITLE = 'MySqlDbClient'
        self.__CONNECT_PNG = 'connect.png'
        self.__EXIT_PNG = 'exit.png'
        self.__CONNECT_ACTION = '&Connect...'
        self.__EXIT_ACTION = '&Exit'
        self.__CONNECT_TOOLTIP = 'Connect to Database'
        self.__EXIT_TOOLTIP = 'Exit Application'
        self.__EXIT_SHORTCUT = 'Ctrl+Q'
        self.__FILE_MENU = '&File'
        self.__OSX_NAME = 'Darwin'
        self.__WINDOW_WIDTH = 600
        self.__WINDOW_HEIGHT = 600
        
    def initUI(self):
        self.__initMenuBar()
        self.statusBar()
        self.__moveToCenter()
        self.setWindowTitle(self.__TITLE)

    def __moveToCenter(self):
        rect = qApp.desktop().availableGeometry(self)
        center = rect.center()
        self.setGeometry(0, 0, self.__WINDOW_WIDTH, self.__WINDOW_HEIGHT)
        self.move(center.x() - self.__WINDOW_HEIGHT * 0.5, center.y() - self.__WINDOW_HEIGHT * 0.5)

    def __createConnectAction(self):
        connectAction = QAction(QIcon(self.__CONNECT_PNG), self.__CONNECT_ACTION, self)
        connectAction.setStatusTip(self.__CONNECT_TOOLTIP)
        connectAction.triggered.connect(self.__openConnectionDialog)
        return connectAction

    def __createQuitAction(self):
        quitAction = QAction(QIcon(self.__EXIT_PNG), self.__EXIT_ACTION, self)
        quitAction.setShortcut(self.__EXIT_SHORTCUT)
        quitAction.setStatusTip(self.__EXIT_TOOLTIP)
        quitAction.triggered.connect(qApp.quit)
        return quitAction

    def __initMenuBar(self):
        menubar = self.menuBar()
        if platform.system() == self.__OSX_NAME:
            menubar.setNativeMenuBar(False) # Very important for Mac OS X
        fileMenu = menubar.addMenu(self.__FILE_MENU)
        fileMenu.addAction(self.__createConnectAction())
        fileMenu.addAction(self.__createQuitAction())

    def __openConnectionDialog(self):
        self.__connDialog = DialogConnectToDataBase()
        self.__connDialog.onDbConnected.connect(self.saveDbConnection)
        self.__connDialog.show()

    @pyqtSlot(str) # TODO
    def saveDbConnection(self, arg1):
        # Dummy
        print(arg1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())