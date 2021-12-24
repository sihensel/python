#!/usr/bin/env python3

# Simple server that accepts connections from clients and can recieve messages

import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()     # returns the hostname, not the IP
port = 1234

# bind the socket
s.bind((host, port))

# listen to connections (allow 3 connections at a time)
s.listen(3)

while True:
    try:
        client, address = s.accept()    # accept connections

        print(f'Recieved connection from {address}')
        msg = 'Connection to the server successful!\n'

        # send the message to the client
        client.send(msg.encode())

        # wait for a response from the client
        response = client.recv(1024)
        print(response.decode())

        client.close()
        print(f'Closed connection to {address}')

    except KeyboardInterrupt:
        sys.exit()
