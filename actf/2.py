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

def fvck(you):
	result = []
	for i in range(you):
		result.append([0 for i in range(you)])
	count = 0
	for i in itertools.combinations(range(1,you),2):
		a, b = i
		qes = str(a) + ' ' + str(b)
		print qes,
		tn.write(qes+'\n')
		ret = tn.read_until('these two folders.')
		print ret
		num = re.search('\d', ret).group()
		result[a][b] = int(num)
		result[b][a] = int(num)
		count += 1
		print 'count:',count
		if count >= (you-1)*4:
			break
	for i in result[1:]:
		print i[1:]
	for line in result[1:]:		
		if 1 not in line:
			secret = result.index(line)
			break
	secret_list = [i-1 for i in result[secret]]
	secret_list[secret]=1
	print 'secret_list: ',secret_list
	
	for i in range(10):
		string1 = tn.read_until('the secret folder?')
		print string1
		num1 = int(re.search('\d+', string1).group())
		print secret_list[num1]
		tn.write(str(secret_list[num1])+'\n')


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
		fvck(11)
		content = tn.read_until("provide your answer")
		print (content)
		fvck(21)
		content = tn.read_until("provide your answer")
		print (content)
		fvck(51)
		content = tn.read_until("provide your answer")
		print (content)
		fvck(101)
		content = tn.read_until("provide your answer")
		print (content)
		fvck(101)
		content = tn.read_until("provide your answer")
		print (content)
		fvck(101)

		print tn.read_all()
	except Exception,e:
		print e
		continue
