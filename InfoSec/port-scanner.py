#!/usr/bin/env python3

# a simple portscanner
# https://www.thepythoncode.com/article/make-port-scanner-python

import socket
import sys

host = input('Please enter a host: ')

def is_port_open(host, port):
    s = socket.socket()

    try:
        s.connect((host, port))
        s.settimeout(0.2)

    # show the error and quit
    except OSError as e:
        print(e)
        sys.exit(1)

    return True

for port in range(1, 101):
    if is_port_open(host, port):
        print(f'Port {port} is open!')
