#!/usr/bin/env python3

'''
A small script that executes different nmap scans

Part of this is still broken and the output needs to be formated properly
'''

import time, sys

try:
    import nmap
except ImportError:
    print('Missing dependency detected, exiting.')
    sys.exit()

scanner = nmap.PortScanner()

print('--- Small Python nmap automation script ---')

#ip_addr = input('Please enter the IP to scan: ')
ip_addr = '192.168.1.1'
ports = '1-1024'    # maybe make this interactive in the future


cmd = input('''\nPlease enter the type of scan:
               1) TCP Scan (-sS)
               2) UDP Scan (-sU)
               3) Comprehensive Scan (-sS -sV -sC -A -O)\n''')

print('Starting scan...')
start_time = time.time()    # measure time

if cmd == '1':
    protocol = 'tcp'
    scanner.scan(ip_addr, ports, '-v -sS')

elif cmd == '2':
    protocol = 'udp'
    scanner.scan(ip_addr, ports, '-v -sU')

elif cmd == '3':
    protocol = 'tcp'
    scanner.scan(ip_addr, ports, '-v -sS -sV -sC -A -O')

else:
    print('Please enter a number between 1 and 3.')
    sys.exit()


print('\nNmap version:', str(scanner.nmap_version()[0]) + '.' + str(scanner.nmap_version()[1]))
print('IP range:' + 4* ' ', scanner.scaninfo()[protocol]['services'])
print('IP Status:' + 3* ' ', scanner[ip_addr].state())

print('Open Ports:' + 3* ' ' , end='') 
for i, j in enumerate(scanner[ip_addr][protocol]):
    if i < len(scanner[ip_addr][protocol].keys()) -1:
        print(j, end=', ')
    else:
        print(j)    # dont print a comma after the last item

print(f'\nFinished in {round(time.time() - start_time, 2)} seconds.')
    
#print(scanner.scaninfo())
#print(scanner[ip_addr])