import argparse
import socket
import sctp


### Real simply client

def sctp_init(opts):

    serveraddr          = (opts.serverip, opts.serverport)
    print ("Connecting to server:%s:%s"%serveraddr)
    sk = sctp.sctpsocket_tcp(socket.AF_INET)

    if opts.bind:
        print ("bind-address:%s", opts.bind)
        sk.bind((opts.bind, 0))
    else:
        print ("no specific local ip.. letting kernel pick one")
    sk.connect(serveraddr)

    print ("Connected")

    return sk


def full_conn(sk):
    size                = 1300
    msgFromClient       = "1234567890"*(size//10)
    recvbuffsize        = 10000

    for i in range(100):
        print ("Trying size:%d"%(size+4*i))
        msgc = msgFromClient + "ABCD"*i
        bytesToSend  = str.encode(msgc)

        sk.sctp_send(bytesToSend)
        print("Data-sent")
        data = sk.recv(10000).decode('utf-8')
        print ("Server Reply: %s"%data)
    sk.shutdown(0)
    sk.close()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bind", help="local bind address", default="")
    parser.add_argument("serverip", help="server ip")
    parser.add_argument("serverport", help="server port", type=int, nargs="?", default=15151)
    cmd_options = parser.parse_args()
    return cmd_options

opts = parse_args()
sk = sctp_init(opts)
full_conn(sk)
