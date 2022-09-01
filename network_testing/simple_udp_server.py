import socket

localIP     = "10.0.100.2"
localPort   = 20001
bufferSize  = 5000

sk = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

## DF-flags
##  Note socket. IP_MTU_DISCOVER == 10
##       socket.IP_PMTUDISC_DONT == 0 (clear DF), IP_PMTUDISC_DO == 2 (set DF)
## we need setsockopt(socket, IP_MTU_DISCOVER, &val)
sk.setsockopt(socket.IPPROTO_IP, 10, 0)
sk.bind((localIP, localPort))

print("UDP server up and listening at %s,%s"%(localIP, localPort))

while(True):
    (message, addr) = sk.recvfrom(bufferSize)
    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(addr)
    print(clientMsg)
    print(clientIP)

    # Sending a reply to client
    info = "Got %d bytes"%len(message)
    sk.sendto(info.encode('utf-8'), addr)
    sk.sendto(message, addr)
