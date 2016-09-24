#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import platform
from os import sep
from PyQt5.QtWidgets import (QMainWindow, QApplication,
                             QTreeView, QAction, qApp,
                             QHBoxLayout, QWidget,
                             QTableView, QSizePolicy)
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtCore import pyqtSlot, QModelIndex, Qt, pyqtSignal
from DialogConnectToDatabase import DialogConnectToDataBase
import utilities

if platform.system() == 'Darwin':
    # MySQL Connector not available for Python v3.5 on windows
    sys.path.append('..')
    from MySqlAccess import MySqlAccess


class MainWindow(QMainWindow):
    # Signals
    db_connection_saved = pyqtSignal()
    table_selected = pyqtSignal(str, str)
    sort = pyqtSignal(str, str, str, list)

    # Slots
    if platform.system() == 'Darwin':
        @pyqtSlot(str, MySqlAccess)
        def save_db_connection(self, msg, db_access):
            self.__set_connection_actions_enabled(False)
            self.statusBar().showMessage(self.__STATUS_CONNECTED + msg)
            self.__dbAccess = db_access
            self.db_connection_saved.emit()

    @pyqtSlot(str)
    def report_db_connection_failure(self, arg1):
        self.statusBar().showMessage(self.__STATUS_CONNECT_FAILED + arg1)

    @pyqtSlot()
    def quit(self):
        self.__disconnect()
        qApp.quit()

    @pyqtSlot(QModelIndex)
    def __on_tree_view_click(self, index):
        if index.isValid():
            null_item = self.__treeView.model().itemData(QModelIndex())
            parent = self.__treeView.model().itemData(index.parent())
            # parent of top item is null_item
            if parent == null_item:
                return
            self.__current_db_name = self.__treeView.model().itemData(index.parent())[0]
            self.__current_table_name = self.__treeView.model().itemData(index)[0]
            self.table_selected.emit(self.__current_db_name, self.__current_table_name)

    @pyqtSlot()
    def __list_databases(self):
        if self.__dbAccess:
            self.__populate_data(self.__dbAccess.get_database())

    @pyqtSlot(str, str)
    def __list_table_data(self, db_name, table_name):
        lst = self.__get_columns_of_table(table_name, db_name)
        self.__set_up_table_head(lst)
        self.__populate_table_data(self.__get_table_data(lst, db_name, table_name, lst[0]))

    @pyqtSlot()
    def __open_connection_dialog(self):
        self.__connDialog = DialogConnectToDataBase()
        if platform.system() == self.__OSX_NAME:
            self.__connDialog.onDbConnected.connect(self.save_db_connection)
        self.__connDialog.onDbConnectedFailed.connect(self.report_db_connection_failure)
        self.__connDialog.show()

    @pyqtSlot()
    def show_about_dialog(self):
        utilities.show_info_msg_box(self, self.__PROG_NAME, self.__PROG_INFO)

    @pyqtSlot(int)
    def __table_header_clicked(self, index):
        self.__dbAccess.flip_order()
        lst = []
        for i in range(self.__tableView.horizontalHeader().count()):
            lst.append(str(self.__tableView.model().headerData(i, Qt.Horizontal)))
        self.sort.emit(self.__current_db_name, self.__current_table_name,
                       str(self.__tableView.model().headerData(index, Qt.Horizontal)), lst)

    @pyqtSlot(str, str, str, list)
    def __sort_data(self, db_name, table_name, column_name, column_names):
        if str is None or not list:
            return
        self.__tableView.model().clear()
        self.__set_up_table_head(column_names)
        self.__populate_table_data(self.__get_table_data(column_names, db_name, table_name, column_name))

    def __setup_event_handlers(self):
        self.db_connection_saved.connect(self.__list_databases)
        self.table_selected.connect(self.__list_table_data)
        self.__treeView.clicked.connect(self.__on_tree_view_click)
        self.__connectAction.triggered.connect(self.__open_connection_dialog)
        self.__disconnAction.triggered.connect(self.__disconnect)
        self.sort.connect(self.__sort_data)
        self.__tableView.horizontalHeader().sectionClicked.connect(self.__table_header_clicked)

    def __get_db_tables(self, db_name) -> QStandardItem:
        item = QStandardItem(db_name)
        for (v,) in self.__dbAccess.get_tables(db_name):
            item.appendRow(QStandardItem(str(v)))
        return item

    def __populate_data(self, vals):
        if (vals is None) or (len(vals) == 0):
            return
        for (v,) in vals:
            self.__treeView.model().appendRow(self.__get_db_tables(str(v)))
        self.statusBar().showMessage(self.__STATUS_READY)

    def __get_columns_of_table(self, table_name, db_name) -> [list]:
        l = []
        for v in self.__dbAccess.get_columns_of_table(db_name, table_name):
            l.append(v[0])
        return l

    def __set_up_table_head(self, lst):
        if not isinstance(lst, list) or not lst:
            return
        self.__tableView.model().clear()
        self.__tableView.model().setColumnCount(len(lst))
        for (i, v) in zip(range(len(lst)), lst):
            self.__tableView.model().setHeaderData(i, Qt.Horizontal, v)

    def __get_table_data(self, lst, db_name, table_name, order_column):
        return self.__dbAccess.query(self.__dbAccess.compose_select(db_name, table_name, lst, order_column))

    def __populate_table_data(self, lst):
        if not isinstance(lst, list) or not lst:
            return
        for values in lst:
            items = []
            for v in values:
                items.append(QStandardItem(str(v)))
            self.__tableView.model().appendRow(items)

    def __clear_contents(self):
        self.__treeView.model().clear()
        self.__tableView.model().clear()
        self.__treeView.model().setHorizontalHeaderItem(0, QStandardItem(self.__DATABASE))

    def __disconnect(self):
        if self.__dbAccess is not None:
            self.__clear_contents()
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
        self.__setup_event_handlers()
        self.__dbAccess = None
        self.__current_db_name = None
        self.__current_table_name = None

    def __init_constants(self):
        # Window and menu
        self.__IMAGE_PATH = 'images' + sep
        self.__TITLE = 'MySqlDbClient'
        self.__CONNECT_PNG = self.__IMAGE_PATH + 'connect.png'
        self.__DISCONNECT_PNG = self.__IMAGE_PATH + 'disconnect.png'
        self.__EXIT_PNG = self.__IMAGE_PATH + 'exit.png'
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
        self.__tableView.setModel(QStandardItemModel())

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
        self.__connectAction.setShortcut(self.__CONNECT_SHORTCUT)
        return self.__connectAction

    def __create_disconnect_action(self) -> QAction:
        self.__disconnAction = QAction(QIcon(self.__DISCONNECT_PNG), self.__DISCONNECT_ACTION, self)
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
