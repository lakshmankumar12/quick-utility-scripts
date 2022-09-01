import socket
import sctp

host = '10.0.3.253'
port = 15151

sock = sctp.sctpsocket_tcp(socket.AF_INET)
sock.bind((host, port))
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
                tosend = "We recieved " + str(len(data)) + " bytes from you"
                connection.sendall(tosend.encode('utf-8'))
            else:
                # no more data -- quit the loop
                print ("no more data.")
                break
    finally:
        # Clean up the connection
        connection.close()
