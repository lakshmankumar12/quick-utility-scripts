import socket

size                = 1400
msgFromClient       = "1234567890"*(size//10)
serverAddressPort   = ("10.0.100.2", 20001)
bufferSize          = 5000

for i in range(50):
    print ("Trying size:%d"%(size+4*i))
    msgc = msgFromClient + "ABCD"*i
    bytesToSend  = str.encode(msgc)
    sk = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    sk.sendto(bytesToSend, serverAddressPort)
    (msg,addr) = sk.recvfrom(bufferSize)
    print ("Message from Server {}".format(msg))
    (msg,addr) = sk.recvfrom(bufferSize)
    print ("Message from Server {}".format(msg))
    sk.close()

