#!/usr/bin/python3

import pexpect
import os
import struct, fcntl, termios, signal, sys
import argparse

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

def parse_args():
    parser = argparse.ArgumentParser(description='Connect to hetzner')
    parser.add_argument("-p","--pass_file", help="file having password for key")
    parser.add_argument("destination", help="where", choices=["blr", "direct"])
    cmd_options = parser.parse_args()
    return cmd_options

def connect_via_blr(opts):
    password = ""
    with open(opts.pass_file, "r") as fd:
        password = fd.read().strip()
    print("sshing to myhetzner via blr")
    c = spawn_child("ssh -o ServerAliveInterval=30 -o ServerAliveCountMax=1 bastionblr")
    c.expect(['magma@perf-s1ap-server'])
    print("logged into blr")
    c.sendline('ssh lakshman_dev')
    c.expect(["Enter passphrase for key '/home/magma/.ssh/lakshman_key':"])
    print("sending pass-key-1")
    c.sendline(password)
    c.expect(["Enter passphrase for key '/home/magma/.ssh/lakshman_key':"])
    print("sending pass-key-2")
    c.sendline(password)
    res = c.expect(['lakshman@lakshmandevhetzner', 'Would you like to update'])
    if res == 1:
        c.sendline("n")
        c.expect(['lakshman@lakshmandevhetzner'])
    print("ssh complete, attaching tmux")
    c.sendline('ta')
    c.interact(escape_character=None)
    print("hetzner-connect done")

def connect_direct():
    print("sshing to myhetzner")
    c = spawn_child("ssh -o ServerAliveInterval=30 -o ServerAliveCountMax=1 myhetzner")
    res = c.expect(['lakshman@lakshmandevhetzner', 'Would you like to update'])
    if res == 1:
        c.sendline("n")
        c.expect(['lakshman@lakshmandevhetzner'])
    print("ssh complete, attaching tmux")
    c.sendline('ta')
    c.interact(escape_character=None)
    print("hetzner-connect done")

def main():
    opts = parse_args()
    if opts.destination == "blr":
        connect_via_blr(opts)
    else:
        connect_direct()

if __name__ == "__main__":
    main()



