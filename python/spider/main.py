import urllib.request

if __name__ == '__main__':
    response = urllib.request.urlopen('http://www.baidu.com')
    print(response.read().decode())
