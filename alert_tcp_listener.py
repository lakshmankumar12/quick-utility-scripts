#!/usr/bin/python

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
notif_file  = os.path.join(home,".received_alerts")

alert_program= os.path.join(home,"github","mac_scripts","pop_up_dialog.sh")

print ("Using tcp alert - program: {}".format(alert_program))

#invocation will throw error and halt script if there is a problem
subprocess.check_output([alert_program,"Test Alert"])

def handle_client_connection(client_socket):
    data = client_socket.recv(1024)
    client_socket.close()
    data = data.strip('\n')
    f=open(notif_file,"a")
    fcntl.flock(f, fcntl.LOCK_EX)
    f.write("%s - %s\n"%(datetime.datetime.now().strftime("%Y-%m-%d:%H-%M-%S"),data))
    print("%s - %s"%(datetime.datetime.now().strftime("%Y-%m-%d:%H-%M-%S"),data))
    fcntl.flock(f, fcntl.LOCK_UN)
    f.close()
    subprocess.check_output([alert_program,data])


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


import daemon

with daemon.DaemonContext():
  main()

