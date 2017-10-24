from pwn import *

r = remote("localhost",4444)
#print r.recvn(10)
r.sendline("2")
print r.sendlineafter("!","3")
#print r.recvn(400)
