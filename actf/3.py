from hashlib import sha1
import sys
import exrex
import re
from zio import *
from decimal import Decimal

def connect():
    io = zio(('119.254.101.232', 8888))
    regex = re.compile('SHA\((.*?)\) = ([\d\w]+)')
    _reg, _hash = regex.findall(io.read_until('\n'))[0]
    for candidate in exrex.generate(_reg):
        shasum = sha1(candidate).hexdigest()
        if shasum == _hash:
            io.write(candidate + '\n')
            break
    io.read_until('your answer\n')
    return io

def floyed(l):
	for k in xrange(1, 11):
		for i in xrange(1, 11):
			for j in xrange(1, 11):
				if i != j and i != k and k != j:
					if l[i][k] + l[k][j] < l[i][j]:
						l[i][j] = l[i][k] + l[k][j]
						l[j][i] = l[i][k] + l[k][j]

def meiju():
	for x in xrange(1, 10):
		for y in xrange(x + 1, 11):
			i += 1
			io.writeline('%d %d' %(x, y))
			num_s = io.read_until('folders.')
			num = pp.findall(num_s)[0]
			print num

def init(l, num):
	for i in xrange(num):
		t = []
		for j in xrange(num):
			if i == j :
				t.append(0xfe)
			else:
				t.append(0xff)
		l.append(t)
	

def check(testl1, truel2):
	e = []
	flag = False
	for i, x in enumerate(testl1):
		for j, y in enumerate(x):
			if testl1[i][j] < truel2[i][j] and truel2[i][j] != 0xff:
				e.append([i,j])
			if testl1[i][j] > truel2[i][j]:
				testl1[i][j] = truel2[i][j]
				flag = True
	if flag:
		floyed(test_map)
	return e


pp = re.compile(r'You need to click (\d+) times')
ap = re.compile(r'times between No\.(\d+) folder')
io = None
while not io:
	try:
		io = connect()
	except:
		pass


true_map = []
init(true_map, 11)
i = 0
for x in xrange(1, 8):
	for y in xrange(x + 1, 11):
		i += 1
		if i >= 41:
			break
		elif i < 41:
			io.writeline('%d %d' %(x, y))
			num_s = io.read_until('between these two folders.')
			num = pp.findall(num_s)[0]
			true_map[x - 1][y - 1] = int(num)
			true_map[y - 1][x - 1] = int(num)
			print num

for x in xrange(6):
	flag = True
	for y in xrange(10):
		if true_map[x][y] == 1:
			flag = False
	if flag:
		true_map[x][10] = 1
		true_map[10][x] = 1

tree_all = []


n = -1
for x in xrange(10):
	if true_map[x][10] == 1:
		n = x
		break
print tree_all
print true_map

for x in xrange(10):
	ans_s = io.read_until('secret folder?')
	num_a = ap.findall(ans_s)[0]
	print num_a
	if true_map[int(num_a)-1][10] == 1:
		io.writeline('1')
	else:
		io.writeline(str(true_map[int(num_a)-1][n] - 1))

# 1-10

io.read_until('(1 - 20) (1 - 20)')
true_map = []
init(true_map, 21)
i = 0
for x in xrange(1, 7):
	for y in xrange(x + 1, 21):
		i += 1
		print i
		if i >= 81:
			break
		elif i < 81:
			io.writeline('%d %d' %(x, y))
			num_s = io.read_until('between these two folders.')
			num = pp.findall(num_s)[0]
			true_map[x - 1][y - 1] = int(num)
			true_map[y - 1][x - 1] = int(num)
			print num

print true_map



for x in xrange(4):
	flag = True
	for y in xrange(20):
		if true_map[x][y] == 1:
			flag = False
	if flag:
		true_map[x][20] = 1
		true_map[20][x] = 1

tree_all = []


n = -1
for x in xrange(20):
	if true_map[x][20] == 1:
		n = x
		break
print tree_all
print true_map

for x in xrange(10):
	ans_s = io.read_until('secret folder?')
	num_a = ap.findall(ans_s)[0]
	print num_a
	if true_map[int(num_a)-1][20] == 1:
		io.writeline('1')
	else:
		io.writeline(str(true_map[int(num_a)-1][n] - 1))


# 1-20


io.read_until('(1 - 50) (1 - 50)')
print '--------------'
true_map = []
init(true_map, 51)
i = 0
for x in xrange(1, 50):
	for y in xrange(x + 1, 51):
		i += 1
		print i
		if i >= 201:
			break
		elif i < 201:
			io.writeline('%d %d' %(x, y))
			num_s = io.read_until('between these two folders.')
			num = pp.findall(num_s)[0]
			true_map[x - 1][y - 1] = int(num)
			true_map[y - 1][x - 1] = int(num)
			print num

print true_map



for x in xrange(4):
	flag = True
	for y in xrange(50):
		if true_map[x][y] == 1:
			flag = False
	if flag:
		true_map[x][50] = 1
		true_map[50][x] = 1

tree_all = []


n = -1
for x in xrange(50):
	if true_map[x][50] == 1:
		n = x
		break
print tree_all
print true_map

for x in xrange(10):
	ans_s = io.read_until('secret folder?')
	num_a = ap.findall(ans_s)[0]
	print num_a
	if true_map[int(num_a)-1][50] == 1:
		io.writeline('1')
	else:
		io.writeline(str(true_map[int(num_a)-1][n] - 1))

# 1- 50

io.read_until('-1 -1 to provide your answer')
print '--------------'
true_map = []
init(true_map, 101)
i = 0
for x in xrange(1, 100):
	for y in xrange(x + 1, 101):
		i += 1
		print i
		if i >= 401:
			break
		elif i < 401:
			io.writeline('%d %d' %(x, y))
			num_s = io.read_until('between these two folders.')
			num = pp.findall(num_s)[0]
			true_map[x - 1][y - 1] = int(num)
			true_map[y - 1][x - 1] = int(num)
			print num

print true_map



for x in xrange(4):
	flag = True
	for y in xrange(100):
		if true_map[x][y] == 1:
			flag = False
	if flag:
		true_map[x][100] = 1
		true_map[100][x] = 1

tree_all = []


n = -1
for x in xrange(5):
	if true_map[x][100] == 1:
		n = x
		break
print tree_all
print true_map

for x in xrange(10):
	ans_s = io.read_until('secret folder?')
	num_a = ap.findall(ans_s)[0]
	print num_a
	if true_map[int(num_a)-1][50] == 1:
		io.writeline('1')
	else:
		io.writeline(str(true_map[int(num_a)-1][n] - 1))
# 1-100

io.read_until('-1 -1 to provide your answer')
print '--------------'
true_map = []
init(true_map, 101)
i = 0
for x in xrange(1, 100):
	for y in xrange(x + 1, 101):
		i += 1
		print i
		if i >= 401:
			break
		elif i < 401:
			io.writeline('%d %d' %(x, y))
			num_s = io.read_until('between these two folders.')
			num = pp.findall(num_s)[0]
			true_map[x - 1][y - 1] = int(num)
			true_map[y - 1][x - 1] = int(num)
			print num

print true_map



for x in xrange(4):
	flag = True
	for y in xrange(100):
		if true_map[x][y] == 1:
			flag = False
	if flag:
		true_map[x][100] = 1
		true_map[100][x] = 1

tree_all = []


n = -1
for x in xrange(5):
	if true_map[x][100] == 1:
		n = x
		break
print tree_all
print true_map

for x in xrange(10):
	ans_s = io.read_until('secret folder?')
	num_a = ap.findall(ans_s)[0]
	print num_a
	if true_map[int(num_a)-1][50] == 1:
		io.writeline('1')
	else:
		io.writeline(str(true_map[int(num_a)-1][n] - 1))
# 1-100



io.interact()
