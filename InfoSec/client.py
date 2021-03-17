#! /usr/bin/python3

import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#host = '192.168.0.107'
host = 'arch'
port = 1234

client.connect((host, port))

# max number of bytes to recieve
msg = client.recv(1024)

client.close()

# print the message from the server
print(msg.decode())