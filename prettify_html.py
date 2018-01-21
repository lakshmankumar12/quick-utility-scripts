#!/usr/bin/python

from __future__ import print_function
import bs4
import argparse
import sys
import os
import re

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--update", help="update in same file", action="store_true")
parser.add_argument("-x", "--xml", help="use xml parser instead of html", action="store_true")
parser.add_argument("-i", "--indent", help="use xml parser instead of html", type=int)
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

orig_prettify = bs4.BeautifulSoup.prettify
r = re.compile(r'^(\s*)', re.MULTILINE)
def prettify(self, encoding=None, formatter="minimal", indent_width=4):
    return r.sub(r'\1' * indent_width, orig_prettify(self, encoding, formatter))
bs4.BeautifulSoup.prettify = prettify

indentWidth=2
if parsed_args.indent:
    indentWidth = parsed_args.indent;

bs4parser="html.parser"
if parsed_args.xml:
    bs4parser = 'xml'

with open(parsed_args.srcfile,'r') as fd:
    soup = bs4.BeautifulSoup(fd,bs4parser)

with open(dst,'w') as fd:
    fd.write(soup.prettify(indent_width=indentWidth).encode('utf-8'))

if parsed_args.update:
    os.rename(dst, parsed_args.srcfile)

