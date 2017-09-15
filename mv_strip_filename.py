#!/usr/bin/python

from __future__ import print_function
import os
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("repl",   help="The string to remove")
parser.add_argument("files",    help="filenames to work on", nargs="+")

parsed_args = parser.parse_args()

ok=True
for i in parsed_args.files:
    if not os.access(i,os.F_OK):
        print ("{} doesn't seem to exist".format(i))
        ok=False

if not ok:
    sys.exit(1)

for i in parsed_args.files:
    src=i
    dst=src.replace(parsed_args.repl,"")
    os.rename(src,dst)

