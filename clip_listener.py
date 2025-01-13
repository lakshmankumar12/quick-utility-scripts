#!/usr/bin/env python

import socket
import threading
import fcntl
import datetime
import os
import subprocess

bind_ip = '0.0.0.0'
bind_port = 25020

from os.path import expanduser
home = expanduser("~")
clip_file = home + '/host_c/Users/laksh/Documents/cliptest.txt'

def handle_client_connection(client_socket):
    data = client_socket.recv(10000)
    client_socket.close()
    f=open(clip_file,"w")
    f.write(data.decode('utf-8'))
    f.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip, bind_port))
    server.listen(5)  # max backlog of connections
    while True:
        client_sock, address = server.accept()
        client_handler = threading.Thread(
            target=handle_client_connection,
            args=(client_sock,)  # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
        )
        client_handler.start()
    subprocess.check_output([alert_program,"Tcp Alert listener stopped!"])


main()

