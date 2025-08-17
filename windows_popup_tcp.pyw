#!python3

import ctypes
import socket
import threading
import os

bind_ip = '0.0.0.0'
bind_port = 25030

# Define message box parameters
MB_OK = 0x00000000
MB_ICONINFORMATION = 0x00000040
MB_SYSTEMMODAL = 0x00001000  # System modal (dialog has focus)

def show_focused_messagebox(title, message):
    # Combine flags for an OK button, info icon, and system modal (focused)
    flags = MB_OK | MB_ICONINFORMATION | MB_SYSTEMMODAL

    # Call the Windows MessageBox function
    result = ctypes.windll.user32.MessageBoxW(
        None,                       # hWnd (None = no owner window)
        message,                    # Message text
        title,                      # Title text
        flags                       # Flags for appearance and behavior
    )

    return result

def handle_client_connection(client_socket):
    data = client_socket.recv(10000)
    client_socket.close()
    data = data.decode('utf-8')
    if len(data) > 500:
        data = data[:500]
    show_focused_messagebox("remote-msg", data)

def tcp_listener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((bind_ip, bind_port))
    sock.listen(5)  # max backlog of connections
    print(f"listener started with pid:{os.getpid()}, ip:{bind_ip} port:{bind_port}")

    try:
        while True:
            client_sock, address = sock.accept()
            client_handler = threading.Thread(
                target=handle_client_connection,
                args=(client_sock,)  # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
            )
            client_handler.start()
            client_handler.join()
    except KeyboardInterrupt:
        pass
    print ("listener.py stopped")

if __name__ == "__main__":
    tcp_listener()
