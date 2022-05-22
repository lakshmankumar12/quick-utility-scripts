#!/usr/local/bin/python3

import sys

helpstr='''
    Just supply the chars to study via stdin
'''

if len(sys.argv) > 1:
    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print (helpstr)
        sys.exit(1)

for line in sys.stdin:
    for char in line:
        print ("Char: %3s  Ord: %04x  Dec: %5d"%(char,ord(char),ord(char)))

