#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psutil
import pdb
import collections
import argparse
from colorama import Fore, Back, Style
import re
import sys

process_hierarchy = {}
root = None
unparented = collections.defaultdict(list)
process_by_name = collections.defaultdict(list)

class MyProcess:
    def __init__(self, p):
        global root
        global process_hierarchy
        global process_by_name
        self.p = p
        self.name = p.name()
        self.pid = p.pid
        self.ppid = p.ppid()
        self.tty = p.terminal()
        if self.ppid == 0:
            if not root:
                root = self
                self.parent = self
            else:
                self.parent = root
                self.parent.children.append(self)
        else:
            if self.ppid in process_hierarchy:
                self.parent = process_hierarchy[self.ppid]
                self.parent.children.append(self)
            else:
                unparented[self.ppid].append(self)
        process_hierarchy[self.pid] = self
        self.children = []
        if self.pid in unparented:
            for ip in unparented[self.pid]:
                ip.parent = self
                self.children.append(ip)
            del unparented[self.pid]
        process_by_name[self.name].append(self)

#indentString=u"\u250a\u2027\u2027"
indentString="|--"
def print_hierarchy(myp, cmd_options, indentLevel):
    highlight_term = ""
    if myp.tty != None and myp.parent.tty != myp.tty:
        highlight_term = Fore.RED + "(N)" + Style.RESET_ALL
    name = myp.name
    if cmd_options.grepPat:
        if cmd_options.grepPat.search(name):
            name = Fore.YELLOW + name + Style.RESET_ALL
    pid = myp.pid
    if cmd_options.pidPat:
        if cmd_options.pidPat.search(pid):
            pid = Fore.YELLOW + pid + Style.RESET_ALL
    print ("{}{}:{} --> {}{}".format(indentString*indentLevel, myp.pid, pid, highlight_term, myp.tty))
    for i in myp.children:
        print_hierarchy(i, cmd_options, indentLevel+1)

def main():
    global root

    parser = argparse.ArgumentParser()
    parser.add_argument("--grephighlight", "-g",  help="process to highlight")
    parser.add_argument("--pidhighlight", "-p",  help="pid to highlight")
    parser.add_argument("--tmuxserver", "-t",  help="process to highlight", action="store_true")
    parser.add_argument("pid",   help="pid to start", nargs="?", type=int, default=1)
    cmd_options = parser.parse_args()

    if cmd_options.grephighlight:
        setattr(cmd_options, "grepPat", re.compile(cmd_options.grephighlight))
    else:
        setattr(cmd_options, "grepPat", None)

    if cmd_options.grephighlight:
        setattr(cmd_options, "pidPat", re.compile(cmd_options.pidhighlight))
    else:
        setattr(cmd_options, "pidPat", None)

    #collect all pros
    for p in psutil.process_iter():
        myp = MyProcess(p)

    if (unparented):
        raise(Exception("unparented not empty!"))

    if cmd_options.pid != 1:
        root = process_hierarchy[cmd_options.pid]

    if cmd_options.tmuxserver:
        tmux_server_name = 'tmux: server'
        if tmux_server_name not in process_by_name:
            print ("{} not found!".format(tmux_server_name))
            sys.exit(1)
        if len(process_by_name[tmux_server_name]) != 1:
            print ("Too many {} found!".format(tmux_server_name))
        root = process_hierarchy[process_by_name[tmux_server_name][0].pid]

    print_hierarchy(root, cmd_options, 0)

try:
    main()
except Exception,e:
    #pdb.set_trace()
    raise

