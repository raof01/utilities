#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import exit, argv
from PyQt5.QtWidgets import QApplication
from MainWindow import MainWindow

if __name__ == '__main__':
    app = QApplication(argv)
    window = MainWindow()
    window.show()
    exit(app.exec_())