#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psutil
import pdb
import collections
import argparse

process_hierarchy = {}
root = None
unparented = collections.defaultdict(list)

class MyProcess:
    def __init__(self, p):
        global root
        global process_hierarchy
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

#indentString=u"\u250a\u2027\u2027"
indentString="|--"
def print_hierarchy(myp, indentLevel):
    highlight_term = ""
    if myp.tty != None and myp.parent.tty != myp.tty:
        highlight_term = "(N)"
    print ("{}{}:{} --> {}{}".format(indentString*indentLevel, myp.pid, myp.name, highlight_term, myp.tty))
    for i in myp.children:
        print_hierarchy(i, indentLevel+1)

def main():
    global root

    parser = argparse.ArgumentParser()
    parser.add_argument("pid",   help="pid to start", nargs="?", type=int, default=1)
    cmd_options = parser.parse_args()

    #collect all pros
    for p in psutil.process_iter():
        myp = MyProcess(p)

    if (unparented):
        raise(Exception("unparented not empty!"))

    if cmd_options.pid != 1:
        root = process_hierarchy[cmd_options.pid]

    print_hierarchy(root, 0)

try:
    main()
except Exception,e:
    #pdb.set_trace()
    raise

