from Crypto.Cipher import AES

key = bytes.fromhex(input("key="))
data = bytes.fromhex(input("encode data="))
mode = AES.MODE_ECB

cryptor = AES.new(key, mode)
text = cryptor.decrypt(data)
print(text.decode("utf-8"))
