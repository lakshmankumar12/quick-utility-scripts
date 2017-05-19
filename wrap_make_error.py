#!/usr/bin/python

from __future__ import print_function
import os
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("error_file", help="error_file_to_use", nargs="?", default="/tmp/errors")

parsed_args = parser.parse_args()

fd=open(parsed_args.error_file,"w")
cwd=os.getcwd()
print("make[1]: Entering directory `"+cwd+"'",file=fd)
for i in sys.stdin:
  print(i,end="")
  sys.stdout.flush()
  print(i,end="",file=fd)
print("make[1]: Leaving directory `"+cwd+"'",file=fd)

