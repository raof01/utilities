# -*- coding: utf-8 -*-

from socket import inet_aton, error
import re

def validIpAddress(ipAddress):
    if 'localhost' == ipAddress:
        return True
    if len(ipAddress.split(sep='.')) != 4:
        return False
    try:
        inet_aton(ipAddress)
        return True
    except error:
        return False

def validPort(portStr):
    matcher = re.compile('[0-9]{1,5}')
    try:
        (start, end) = matcher.match(portStr).span()
    except:
        return False
    if start != 0 or end != len(portStr):
        return False
    port = int(portStr)
    if port > 65535 or port <= 0:
        return False
    return True

