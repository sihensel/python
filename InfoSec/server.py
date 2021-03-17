#!/usr/bin/python3

import socket, sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()     # returns the hostname (arch in my case), not the IP
port = 1234                     # remember to allow the port in ufw

# bind the socket
s.bind((host, port))

# listen to connections (allow 3 connections at a time)
s.listen(3)

while True:
    try:
        client, address = s.accept()    #accept connections
    
        print(f'recieved connection from {address}')
        msg = 'Connection to the server successful!\r\n'

        # send the message to the client
        client.send(msg.encode())
        client.close()
    
    except KeyboardInterrupt:
        sys.exit()