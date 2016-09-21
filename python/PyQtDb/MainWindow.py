#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import platform
from PyQt5 import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QTreeView, QAction, qApp, QMenuBar, QMenu, QHBoxLayout, QWidget
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from DialogConnectToDatabase import DialogConnectToDataBase
import utilities
if platform.system() == 'Darwin':
    # MySQL Connector not available for Python v3.5 on windows
    sys.path.append('..')
    from MySqlAccess import MySqlAccess

class MainWindow(QMainWindow):
    if platform.system() == 'Darwin':
        @pyqtSlot(str, MySqlAccess) # TODO
        def saveDbConnection(self, msg, dbAccess):
            self.__setConnectionActionsEnabled(False)
            self.statusBar().showMessage(self.__STATUS_CONNECTED + msg)
            self.__dbAccess = dbAccess
            self.__listDatabases()
    
    def __listDatabases(self):
        if self.__dbAccess:
            #select_sql = '''SELECT * FROM test_DB.Products'''
            select_sql = '''SHOW DATABASES'''
            l = self.__dbAccess.query(select_sql)
            self.statusBar().showMessage('Connected')
            self.__createDbTreeView(l)

    def __createDbTreeView(self, vals):
        if (vals is None) or (len(vals) == 0):
            return
        if self.__treeView is None:
            self.__treeView = QTreeView()
        model = QStandardItemModel()
        model.setHorizontalHeaderItem(0, QStandardItem('Database'))
        for v, in vals:
            model.appendRow(QStandardItem(str(v)))
        self.__treeView.setModel(model)
        #self.__treeView.setExpanded(self.__treeView.currentIndex(), True)
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.__treeView)
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.mainLayout)
        # set central widget
        self.setCentralWidget(self.centralWidget)
        self.statusBar().showMessage('Ready')

    @pyqtSlot(str)
    def reportDbConnectionFailure(self, arg1):
        self.statusBar().showMessage(self.__STATUS_CONNECT_FAILED + arg1)

    @pyqtSlot()
    def quit(self):
        self.__disconnect()
        qApp.quit()

    def __disconnect(self):
        if not self.__dbAccess is None:
            self.__treeView.model().clear()
            self.__dbAccess.disconnect()
            self.__setConnectionActionsEnabled(True)
            self.statusBar().showMessage(self.__STATUS_DISCONNECTED)
    
    def __setConnectionActionsEnabled(self, enabled):
        self.__disconnAction.setEnabled(not enabled)
        self.__connectAction.setEnabled(enabled)

    def __init__(self):
        super().__init__()
        self.__initConstants()
        self.initUI()
        self.__dbAccess = None
        
    def __initConstants(self):
        self.__TITLE = 'MySqlDbClient'
        self.__CONNECT_PNG = 'connect.png'
        self.__DISCONNECT_PNG = 'disconnect.png'
        self.__EXIT_PNG = 'exit.png'
        self.__CONNECT_ACTION = '&Connect...'
        self.__DISCONNECT_ACTION = '&Disconnect'
        self.__EXIT_ACTION = '&Exit'
        self.__ABOUT_ACTION = '&About...'
        self.__CONNECT_TOOLTIP = 'Connect to Database'
        self.__EXIT_TOOLTIP = 'Exit Application'
        self.__EXIT_SHORTCUT = 'Ctrl+Q'
        self.__FILE_MENU = '&File'
        self.__HELP_MENU = '&Help'
        self.__OSX_NAME = 'Darwin'
        self.__STATUS_READY = 'Ready'
        self.__STATUS_CONNECTED = 'Connected to '
        self.__STATUS_CONNECT_FAILED = 'Fail to connected to '
        self.__STATUS_DISCONNECTED = 'Disconnected'
        self.__WINDOW_WIDTH = 800
        self.__WINDOW_HEIGHT = 600
        
    def initUI(self):
        self.__initMenuBar()
        self.statusBar().showMessage(self.__STATUS_READY)
        self.__moveToCenter()
        self.setWindowTitle(self.__TITLE)
        self.__treeView = None

    def __moveToCenter(self):
        rect = qApp.desktop().availableGeometry(self)
        center = rect.center()
        self.setGeometry(0, 0, self.__WINDOW_WIDTH, self.__WINDOW_HEIGHT)
        self.move(center.x() - self.__WINDOW_HEIGHT * 0.5, center.y() - self.__WINDOW_HEIGHT * 0.5)

    def __createConnectAction(self):
        self.__connectAction = QAction(QIcon(self.__CONNECT_PNG), self.__CONNECT_ACTION, self)
        self.__connectAction.setStatusTip(self.__CONNECT_TOOLTIP)
        self.__connectAction.triggered.connect(self.__openConnectionDialog)
        return self.__connectAction

    def __createDisconnectAction(self):
        self.__disconnAction = QAction(QIcon(self.__DISCONNECT_PNG), self.__DISCONNECT_ACTION, self)
        self.__disconnAction.triggered.connect(self.__disconnect)
        return self.__disconnAction

    def __createQuitAction(self):
        quitAction = QAction(QIcon(self.__EXIT_PNG), self.__EXIT_ACTION, self)
        quitAction.setShortcut(self.__EXIT_SHORTCUT)
        quitAction.setStatusTip(self.__EXIT_TOOLTIP)
        quitAction.triggered.connect(self.quit)
        return quitAction

    def __initMenuBar(self):
        menubar = self.menuBar()
        if platform.system() == self.__OSX_NAME:
            menubar.setNativeMenuBar(False) # Very important for Mac OS X
        self.__initFileMenu(menubar)
        self.__initHelpMenu(menubar)
        self.__setConnectionActionsEnabled(True)
        
    def __initFileMenu(self, menuBar):
        fileMenu = menuBar.addMenu(self.__FILE_MENU)
        fileMenu.addAction(self.__createConnectAction())
        fileMenu.addAction(self.__createDisconnectAction())
        fileMenu.addAction(self.__createQuitAction())
        
    def __initHelpMenu(self, menuBar):
        helpMenu = menuBar.addMenu(self.__HELP_MENU)
        helpMenu.addAction(self.__createAboutAction())

    def __createAboutAction(self):
        aboutAction = QAction(self.__ABOUT_ACTION, self)
        aboutAction.triggered.connect(self.showAboutDialog)
        return aboutAction

    def showAboutDialog(self):
        utilities.showInfoMsgBox(self, 'MySQL client', 'Written in Python\nBy Felix Rao\nCopyright (c) 2016')

    def __openConnectionDialog(self):
        self.__connDialog = DialogConnectToDataBase()
        if platform.system() == 'Darwin':
            self.__connDialog.onDbConnected.connect(self.saveDbConnection)
        self.__connDialog.onDbConnectedFailed.connect(self.reportDbConnectionFailure)
        self.__connDialog.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
