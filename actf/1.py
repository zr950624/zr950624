import telnetlib
import hashlib
import re
import string
import time
import itertools


def check(key,h):
	s = hashlib.sha1(key).hexdigest()
	# print s, h

	if s == h:
		return True
	else:
		return False

def find(s,h):	
	key2 = ("".join(j) for j in itertools.product(string.lowercase,repeat=2))
	key1 = ("".join(i) for i in itertools.product('0123456789',repeat=4))
	keys = (s.join(i) for i in itertools.product(key1,key2))
	for key in keys:			
		if check(key,h):
			# print key	
			return key




while 1:
	try:
		tn = telnetlib.Telnet('119.254.101.232',port=8888)
		source = tn.read_until("question:")
		print (source)
		s = re.search(r'(?<=\})\w{8}(?=\[)', source).group()
		h = re.search(r'\w{40}', source).group()
		t = find(s,h)
		a = time.time()
		print t
		tn.write(t+'\n')
		print (time.time() -a)
		content = tn.read_until("provide your answer")
		print (content)
		for i in itertools.combinations(range(1,11),2):
			a, b = i
			qes = str(a) + ' ' + str(b)
			print qes
			tn.write(qes+'\n')
			ret = tn.read_until('these two folders.')
			print ret


	except Exception:
		continue
