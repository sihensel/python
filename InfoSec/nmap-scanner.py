#!/usr/bin/env python3

'''
A small script that executes different nmap scans depending on user input
https://github.com/sihensel
'''

import time
import sys

try:
    import nmap
except ImportError:
    print('Missing dependency "python-nmap", exiting.')
    sys.exit(1)

nm = nmap.PortScanner()

print('--- Small Python nmap automation script ---')

while True:
    # wait until input is valid or user quits
    cmd = input('''\nPlease enter the type of scan (q to quit):
                   1) TCP Scan (-sS)
                   2) UDP Scan (-sU)
                   3) Comprehensive Scan (-sS -sV -sC -A -O)\n''')

    # exit on q or Q
    if cmd == 'q' or cmd == 'Q':
        sys.exit(0)
    elif cmd in ['1', '2', '3']:
        break

ip_addr = input('Enter the IP to scan (hostnames don\'t work): ')

while True:
    # wait until upper port limit input is valid
    try:
        port_limit = int(input('Enter the upper port limit (default 1024): ')
                         or 1024)
    except ValueError:
        print('The port number has to be an integer')
    else:
        break

# generate port range as a string, e.g. '1-1024'
port_range = f'1-{port_limit}'

print(f'\nStarting scan on host {ip_addr} ...')
start_time = time.time()

if cmd == '1':
    protocol = 'tcp'
    options = '-v -sS'
elif cmd == '2':
    protocol = 'udp'
    options = '-v -sU'
elif cmd == '3':
    protocol = 'tcp'
    options = '-v -sS -sV -sC -A -O'

nm.scan(ip_addr, port_range, options)

# aggregate scan results and output them
print(f'\nNmap version: {nm.nmap_version()[0]}.{nm.nmap_version()[1]}')

try:
    print('IP status:' + 3 * ' ', nm[ip_addr].state())
except KeyError:
    print(f'Host {ip_addr} is not reachable')
    sys.exit(1)

print('IP range:' + 4 * ' ', nm.scaninfo()[protocol]['services'])

print('Open ports:' + 3 * ' ', end='')
for index, item in enumerate(nm[ip_addr][protocol].items(), start=1):
    if item[1]['state'] == 'closed':
        continue
    if index == len(nm[ip_addr][protocol].keys()):
        print(item[0])
    else:
        print(item[0], end=', ')

print(f'\nFinished in {round(time.time() - start_time, 2)} seconds.')
