f = open("./pid",'r')
out = ''

for i in f.read():
	ch = str(hex(ord(i)))[2:]
	if(len(ch) == 1):
		ch = '0' + ch
	out += '\\x' + ch
#7457
for i in range(7):
	print out[1000*i*4:1000*(i+1)*4]
	print 
print out[7000*4:]
