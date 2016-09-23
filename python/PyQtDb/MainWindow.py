#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import platform
from PyQt5 import Qt
from PyQt5.QtWidgets import (QMainWindow, QApplication,
                             QTreeView, QAction, qApp, QMenuBar,
                             QMenu, QHBoxLayout, QWidget,
                             QTableView, QSizePolicy)
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
        @pyqtSlot(str, MySqlAccess)  # TODO
        def save_db_connection(self, msg, db_access):
            self.__set_connection_actions_enabled(False)
            self.statusBar().showMessage(self.__STATUS_CONNECTED + msg)
            self.__dbAccess = db_access
            self.__list_databases()

    @pyqtSlot(str)
    def report_db_connection_failure(self, arg1):
        self.statusBar().showMessage(self.__STATUS_CONNECT_FAILED + arg1)

    @pyqtSlot()
    def quit(self):
        self.__disconnect()
        qApp.quit()

    def __list_databases(self):
        if self.__dbAccess:
            l = self.__dbAccess.query(self.__SQL_SHOW_DB)
            self.__populate_data(l)

    def __get_db_tables(self, db_name) -> QStandardItem:
        item = QStandardItem(db_name)
        l = self.__dbAccess.query(self.__SQL_SHOW_TABLES + db_name)
        for (v,) in l:
            item.appendRow(QStandardItem(str(v)))
        return item

    def __populate_data(self, vals):
        if (vals is None) or (len(vals) == 0):
            return
        for (v,) in vals:
            self.__treeView.model().appendRow(self.__get_db_tables(str(v)))
        self.statusBar().showMessage(self.__STATUS_READY)

    def __disconnect(self):
        if self.__dbAccess is not None:
            self.__treeView.model().clear()
            self.__treeView.model().setHorizontalHeaderItem(0, QStandardItem(self.__DATABASE))
            self.__dbAccess.disconnect()
            self.__set_connection_actions_enabled(True)
            self.statusBar().showMessage(self.__STATUS_DISCONNECTED)

    def __set_connection_actions_enabled(self, enabled):
        self.__disconnAction.setEnabled(not enabled)
        self.__connectAction.setEnabled(enabled)

    def __init__(self):
        super().__init__()
        self.__init_constants()
        self.init_ui()
        self.__dbAccess = None

    def __init_constants(self):
        # Window and menu
        self.__TITLE = 'MySqlDbClient'
        self.__CONNECT_PNG = 'connect.png'
        self.__DISCONNECT_PNG = 'disconnect.png'
        self.__EXIT_PNG = 'exit.png'
        self.__CONNECT_ACTION = '&Connect...'
        self.__CONNECT_SHORTCUT = 'Ctrl+O'
        self.__DISCONNECT_ACTION = '&Disconnect'
        self.__DISCONNECT_SHORTCUT = 'Ctrl+D'
        self.__EXIT_ACTION = '&Exit'
        self.__ABOUT_ACTION = '&About...'
        self.__CONNECT_TOOLTIP = 'Connect to Database'
        self.__EXIT_TOOLTIP = 'Exit Application'
        self.__EXIT_SHORTCUT = 'Ctrl+Q'
        self.__FILE_MENU = '&File'
        self.__HELP_MENU = '&Help'
        self.__OSX_NAME = 'Darwin'
        self.__WINDOW_WIDTH = 1024
        self.__WINDOW_HEIGHT = 800

        # Status
        self.__STATUS_READY = 'Ready'
        self.__STATUS_CONNECTED = 'Connected to '
        self.__STATUS_CONNECT_FAILED = 'Fail to connected to '
        self.__STATUS_DISCONNECTED = 'Disconnected'
        self.__DATABASE = 'Database'

        # SQL
        self.__SQL_SHOW_DB = 'SHOW DATABASES'
        self.__SQL_SHOW_TABLES = 'SHOW TABLES IN '

        # Info
        self.__PROG_NAME = 'MySQL client'
        self.__PROG_INFO = 'Written in Python\nBy Felix Rao\nCopyright (c) 2016'

    def init_ui(self):
        self.__init_menu_bar()
        self.statusBar().showMessage(self.__STATUS_READY)
        self.__move_to_center()
        self.setWindowTitle(self.__TITLE)
        self.__init_data_view()

    def __init_tree_view(self):
        self.__treeView = QTreeView()
        self.__treeView.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        rect = self.__treeView.geometry()
        rect.setWidth(self.__WINDOW_WIDTH / 4)
        self.__treeView.setGeometry(rect)
        model = QStandardItemModel()
        model.setHorizontalHeaderItem(0, QStandardItem(self.__DATABASE))
        self.__treeView.setModel(model)

    def __init_table_view(self):
        self.__tableView = QTableView()

    def __init_data_view(self):
        self.__init_tree_view()
        self.__init_table_view()
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.__treeView)
        self.mainLayout.addWidget(self.__tableView)
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.centralWidget)

    def __move_to_center(self):
        rect = qApp.desktop().availableGeometry(self)
        center = rect.center()
        self.setGeometry(0, 0, self.__WINDOW_WIDTH, self.__WINDOW_HEIGHT)
        self.move(center.x() - self.__WINDOW_HEIGHT * 0.5, center.y() - self.__WINDOW_HEIGHT * 0.5)

    def __create_connect_action(self) -> QAction:
        self.__connectAction = QAction(QIcon(self.__CONNECT_PNG), self.__CONNECT_ACTION, self)
        self.__connectAction.setStatusTip(self.__CONNECT_TOOLTIP)
        self.__connectAction.triggered.connect(self.__open_connection_dialog)
        self.__connectAction.setShortcut(self.__CONNECT_SHORTCUT)
        return self.__connectAction

    def __create_disconnect_action(self) -> QAction:
        self.__disconnAction = QAction(QIcon(self.__DISCONNECT_PNG), self.__DISCONNECT_ACTION, self)
        self.__disconnAction.triggered.connect(self.__disconnect)
        self.__disconnAction.setShortcut(self.__DISCONNECT_SHORTCUT)
        return self.__disconnAction

    def __create_quit_action(self) -> QAction:
        quit_action = QAction(QIcon(self.__EXIT_PNG), self.__EXIT_ACTION, self)
        quit_action.setShortcut(self.__EXIT_SHORTCUT)
        quit_action.setStatusTip(self.__EXIT_TOOLTIP)
        quit_action.triggered.connect(self.quit)
        return quit_action

    def __init_menu_bar(self):
        menu_bar = self.menuBar()
        if platform.system() == self.__OSX_NAME:
            menu_bar.setNativeMenuBar(False)  # Very important for Mac OS X
        self.__init_file_menu(menu_bar)
        self.__init_help_menu(menu_bar)
        self.__set_connection_actions_enabled(True)

    def __init_file_menu(self, menu_bar):
        file_menu = menu_bar.addMenu(self.__FILE_MENU)
        file_menu.addAction(self.__create_connect_action())
        file_menu.addAction(self.__create_disconnect_action())
        file_menu.addAction(self.__create_quit_action())

    def __init_help_menu(self, menu_bar):
        help_menu = menu_bar.addMenu(self.__HELP_MENU)
        help_menu.addAction(self.__create_about_action())

    def __create_about_action(self) -> QAction:
        about_action = QAction(self.__ABOUT_ACTION, self)
        about_action.triggered.connect(self.show_about_dialog)
        return about_action

    def show_about_dialog(self):
        utilities.show_info_msg_box(self, self.__PROG_NAME, self.__PROG_INFO)

    def __open_connection_dialog(self):
        self.__connDialog = DialogConnectToDataBase()
        if platform.system() == self.__OSX_NAME:
            self.__connDialog.onDbConnected.connect(self.save_db_connection)
        self.__connDialog.onDbConnectedFailed.connect(self.report_db_connection_failure)
        self.__connDialog.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
