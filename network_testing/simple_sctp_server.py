import argparse
import socket
import sctp

host = '10.0.2.1'
port = 15151

def start_server(opts):

    print ("Waiting on ip:%s, port:%s"%(opts.myip, opts.myport))

    sock = sctp.sctpsocket_tcp(socket.AF_INET)
    sock.bind((opts.myip, opts.myport))
    sock.listen(1)

    while True:
        # wait for a connection
        print ('waiting for a connection')
        connection, client_address = sock.accept()

        try:
            # show who connected to us
            print ('connection from', client_address)
            print (connection)
            # receive the data in small chunks and print it
            while True:
                data = connection.recv(5000).decode('utf-8')
                if data:
                    # output received data
                    print ("Data: %s" % data)
                    tosend = "Received " + str(len(data)) + " bytes"
                    connection.sendall(tosend.encode('utf-8'))
                else:
                    # no more data -- quit the loop
                    print ("no more data.")
                    break
        finally:
            # Clean up the connection
            connection.close()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("myip", help="listen ip")
    parser.add_argument("myport", help="listen port", type=int, nargs="?", default=15151)
    cmd_options = parser.parse_args()
    return cmd_options

opts = parse_args()
start_server(opts)
