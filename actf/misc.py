

base1 = 'uUmFyIRoHAM6Zc4AADQAAAAAAAAAG2jewMIEqf9IFsG4GGacflDl//NdXiPat7yiztRXBVQJK3i8PVlG+DarvOyd1bnJ4rWaL+Ff315gFhXr2KKgAw8/jffY+/CnZRXOJYmKjyv5oZQeuMTQg3iwBBWRT'
base2 = 'ZJh9F0wNUpIDUpHWh6idx6joEbFt/Uy7iSf1miCZ85HYENFQ6YDYRescN5oE5mTwI3BlrRzAKr/HGXu9EbBAzB0rI7wR7G0EbDrRq4iMnC9av7vY40u+0TgRr7W8sqMW1b+xht3LgI5sUNRePmRTXgKA'

base3 = 'qeqNsVe2lME/0GhX4amB+umEPuF+uKe5K/Xf/ieZIS3wPn/oSbrkZDUa0ZN9+aeyFkWZ8oy2IA+1IB12fPahwohkjrsvGJ9liEdbH8NFEp8iQRPrfIKhh73mqq2qrrT3nS9NChS2RXT286P7v5FNXwXHz7yr3xLLUK8HPQwVWxIcVVOucxy+Qgr0NMt0Of+I3Xs2SMBpKVcG2jewMIEqf7Wl0vRBO68/HaAuDyugZYo='

str1 =  base1[1:].decode('base64')+base2.decode('base64')+base3.decode('base64')
print str1.encode('hex')
f = open('1.rar','wb')
f.write(str1)
f.close()
