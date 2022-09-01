import socket
import sctp

size                = 1400
msgFromClient       = "1234567890"*(size//10)
serveraddr          = ("10.0.3.253", 15151)
recvbuffsize        = 10000

for i in range(50):
    print ("Trying size:%d"%(size+4*i))
    msgc = msgFromClient + "ABCD"*i
    bytesToSend  = str.encode(msgc)

    sk = sctp.sctpsocket_tcp(socket.AF_INET)
    sk.connect(serveraddr)

    sk.sctp_send(bytesToSend)
    print("Data-sent")
    data = sk.recv(10000).decode('utf-8')
    print ("Got: %s"%data)
    sk.shutdown(0)
    sk.close()
