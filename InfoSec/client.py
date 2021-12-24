#! /usr/bin/env python3

# Simple client that connects to a server and can send a message

import socket
import sys

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = 'arch'
port = 1234

try:
    client.connect((host, port))
except ConnectionRefusedError:
    print(f'No server with hostname {host} is running on port {port}')
    sys.exit(1)

# max number of bytes to recieve
msg = client.recv(1024)

# print the message from the server
print(msg.decode())

response = input('Send a message to the server: ')
response += '\n'

client.send(response.encode())
client.close()
