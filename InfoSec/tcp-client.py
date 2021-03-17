# a simple tcp client using the SOCKET module (SSL for HTTPS)

import socket, ssl

#host = 'time.nist.gov'
#port = 13

host = 'info.cern.ch'
port = 80

#host = 'www.horads.de'
#port = 443

def tcp_client(host, port):

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if port == 13 or port == 80:
        client.connect((host, port))
        client.sendall(('GET / HTTP/1.1\r\nHost: ' + host + '\r\n\r\n').encode())
        response = client.recv(1024).decode()

    elif port == 443:
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        client_https = context.wrap_socket(client, server_hostname=host)

        client_https.connect((host, port))
        client_https.send(('GET / HTTP/1.1\r\nHost: ' + host + '\r\n\r\n').encode())

        response = client_https.recv(1024).decode()
        
    else:
        return 'Error'
    
    return str(response)


print(tcp_client(host, port))