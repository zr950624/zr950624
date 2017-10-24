from Crypto.Cipher import AES

def deco(key,data):
	try:
		key = bytes.fromhex(key)
		data = bytes.fromhex(data)
		mode = AES.MODE_ECB

		cryptor = AES.new(key, mode)
		text = cryptor.decrypt(data)
		print(text.decode("utf-8"))
	except:
		pass

f = open('1','r')
time = 1
while 1 :
	key = f.readline().strip('\n')
	data = f.readline().strip('\n')
	if(key == '' or data == ''):
		break
	deco(key,data)
