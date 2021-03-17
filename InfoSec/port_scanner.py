# a simple portscanner
# https://www.thepythoncode.com/article/make-port-scanner-python

import socket

host = '192.168.0.106'

def is_port_open(host, port):
    s = socket.socket()

    try:
        s.connect((host, port))
        s.settimeout(0.2)
    except:
        return False
    else:
        return True

for port in range(1, 101):
    if is_port_open(host, port):
        print('Port ', port, 'is open!')