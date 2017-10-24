import telnetlib
import itertools
import Queue
import multiprocessing
import struct
import sha

_task_queue = Queue.Queue()
answer = multiprocessing.Queue()

for c in '0123456789abcdef':
    _task_queue.put(c)





username = 'admin&password=xxxxxx#'
password = '1'
url = '/login?username=' + username + '&password=' + password
orig_msg = url
tn = telnetlib.Telnet('119.254.101.197', port=10004, timeout=120)
tn.set_debuglevel(2)
tn.read_until('[Y/n]')
tn.write('Y\n')
tn.read_until('username:')
tn.write(username+'\n')
tn.read_until('password:')
tn.write('1')
content = tn.read_until('[Y/n] ')
tn.write('Y\n')
h = content.split()[0].strip()
print 'First: '
print h

new_msg = '/login?username=admin&password=xxxxxx#&password=1\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x081'

tn.read_until('username:')
tn.write('admin&password=xxxxxx#\n')
tn.read_until('password:')
tn.write(new_msg[len(url) - 1:] + '\n')
content = tn.read_until('[Y/n] ')
print 'Second: '
wanted = content.split()[0]
print wanted

x_index = []
for i, c in enumerate(h):
    if c == 'x':
        x_index.append(i)

print x_index


def calc(task, answer):
    for j in itertools.product('0123456789abcdef', repeat=6):
        t = (task, )
        t += j
        orig_sig = h
        orig_sig = [c for c in orig_sig]
        for i, x in enumerate(x_index):
            orig_sig[x] = t[i]
        orig_sig = ''.join(orig_sig)

        m = sha.new()
        m.count = [0, 1024]
        _digest = orig_sig.decode("hex")
        (m.H0, m.H1, m.H2, m.H3, m.H4) = struct.unpack(">IIIII", _digest)
        m.update('1')

        new_sig = m.hexdigest()
        for i in range(40):
            if wanted[i] != 'x' and wanted[i] != new_sig[i]:
                break
        else:
            answer.put(orig_sig)
            print '[*] Gotcha !!!!!!\a\a\a\a\a', orig_sig
            return
    print '[*] Task', task, 'Done'


threads = []
for x in xrange(16):
    task = _task_queue.get()
    t = multiprocessing.Process(target=calc, args=(task, answer,))
    threads.append(t)
for t1 in threads:
    t1.start()

count = 0
while 1:
    try:
        ans = answer.get(timeout=100)
    except:
        count += 1
        tn.write('Y\n')
        tn.read_until('username:')
        tn.write('admin&password=xxxxxx#\n')
        tn.read_until('password:')
        tn.write(new_msg[len(url) - 1:] + str(count) + '\n')
        content = tn.read_until('[Y/n] ')
    else:
        break
tn.write('N\n')
tn.read_until('Send login url: ')
tn.write(url)
tn.read_until('Signature: ')
tn.write(ans + '\n')
tn.read_all()
