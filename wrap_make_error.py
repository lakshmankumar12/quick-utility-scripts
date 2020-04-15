#!/usr/bin/python

from __future__ import print_function
import os
import sys
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("error_file", help="error_file_to_use", nargs="?", default="/tmp/errors")

parsed_args = parser.parse_args()

fd=open(parsed_args.error_file,"w")
prefix=""
branch=""
if 'SVNGITROOT' in os.environ:
    backing_dir_file=os.path.join(os.environ['SVNGITROOT'],'.backing_dir_path')
    if os.path.exists(backing_dir_file):
        with open(backing_dir_file, 'r') as fd1:
            prefix=fd1.read().strip()
    branch_file=os.path.join(os.environ['SVNGITROOT'],'.branch_name')
    if os.path.exists(branch_file):
        with open(branch_file, 'r') as fd1:
            branch=fd1.read().strip()
if prefix and branch:
    components=re.split(branch,os.getcwd())
    if components and len(components) == 2:
        cwd=os.path.join(prefix, components[1][1:])
if not cwd:
    cwd=os.getcwd()
print("make[1]: Entering directory `"+cwd+"'",file=fd)
for i in sys.stdin:
  print(i,end="")
  sys.stdout.flush()
  print(i,end="",file=fd)
print("make[1]: Leaving directory `"+cwd+"'",file=fd)

