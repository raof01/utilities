# -*- coding: utf-8 -*-

from socket import inet_aton, error
import re
from PyQt5.QtWidgets import QMessageBox


def show_error_message_box(widget, error_message):
    QMessageBox.critical(widget, 'Error!', error_message, QMessageBox.Ok)


def show_info_msg_box(widget, msg1, msg2):
    QMessageBox.information(widget, msg1, msg2, QMessageBox.Ok)


def valid_ip_address(ip_address) -> bool:
    if 'localhost' == ip_address:
        return True
    if len(ip_address.split(sep='.')) != 4:
        return False
    try:
        inet_aton(ip_address)
        return True
    except error:
        return False


def valid_port(port_str) -> bool:
    matcher = re.compile('[0-9]{1,5}')
    match = matcher.match(port_str)
    if match is None:
        return False
    (start, end) = match.span()
    if start != 0 or end != len(port_str):
        return False
    port = int(port_str)
    if port > 65535 or port <= 0:
        return False
    return True
