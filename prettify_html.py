#!/usr/bin/python

from __future__ import print_function
import bs4
import argparse
import sys
import os

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--update", help="update in same file", action="store_true")
parser.add_argument("srcfile", help="the html file")
parser.add_argument("dstfile", help="destinationfile", nargs="?")

parsed_args = parser.parse_args()

if parsed_args.update and parsed_args.dstfile:
    print("You should give either one of --update or dstfile")
    parser.print_help()
    sys.exit(1)

if not parsed_args.dstfile:
    dst = parsed_args.srcfile + ".out.html"
else:
    dst = parsed_args.dstfile

with open(parsed_args.srcfile,'r') as fd:
    soup = bs4.BeautifulSoup(fd,'html.parser')

with open(dst,'w') as fd:
    fd.write(soup.prettify().encode('utf-8'))

if parsed_args.update:
    os.rename(dst, parsed_args.srcfile)

