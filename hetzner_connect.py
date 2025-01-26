#!/usr/bin/python3

import pexpect
import os
import struct, fcntl, termios, signal, sys

def get_parent_win_size():
    with open(os.ctermid(), 'r') as fd:
        packed = fcntl.ioctl(fd, termios.TIOCGWINSZ, struct.pack('HHHH', 0, 0, 0, 0))
        rows, cols, h_pixels, v_pixels = struct.unpack('HHHH', packed)
        return (rows,cols)
    return (24,80)

def spawn_child(command):
    child = pexpect.spawn(command, encoding='utf-8')
    if not child:
        raise Exception("no child for command:{}".format(command))

    def sigwinch_passthrough (sig, discard_arg):
        s = struct.pack("HHHH", 0, 0, 0, 0)
        a = struct.unpack('hhhh', fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ , s))
        child.setwinsize(a[0],a[1])

    (r,c) = get_parent_win_size()
    signal.signal(signal.SIGWINCH, sigwinch_passthrough)
    child.setwinsize(r,c)
    return child

def main():
    print("sshing to myhetzner")
    c = spawn_child("ssh myhetzner")
    c.expect(['lakshman@lakshmandevhetzner'])
    print("ssh complete, attaching tmux")
    c.sendline('ta')
    c.interact(escape_character=None)

if __name__ == "__main__":
    main()



