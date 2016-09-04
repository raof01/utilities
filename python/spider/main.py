#!/usr/bin/env python3

import urllib.request

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0'

if __name__ == '__main__':
    req = urllib.request.Request('http://www.baidu.com/#')
    req.add_header('User-Agent', user_agent)
    try:
        response = urllib.request.urlopen(req)
        print(response.read().decode())
    except urllib.error.URLError as e:
        print(e.reason)
