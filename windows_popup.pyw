#!python3

import ctypes
import socket
import threading

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

def udp_listener(port=25030):
    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', port))

    print(f"Listening for UDP messages on port {port}...")

    while True:
        # Buffer size of 1024 bytes
        data, addr = sock.recvfrom(1024)
        message = data.decode('utf-8', errors='replace')

        # Display message in a non-blocking way
        threading.Thread(
            target=show_focused_messagebox,
            args=("Notification", f"{message}")
        ).start()

if __name__ == "__main__":
    # Start the UDP listener
    udp_listener()
