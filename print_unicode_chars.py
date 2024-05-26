#!/usr/local/bin/python3

import sys
import os


helpstr = '''
    Just type unicode number points in hex-base separated by space, and it will print the chars
'''

if len(sys.argv[1:]) < 1:
    print ("No input!! See -h for help")
    sys.exit(1)

if sys.argv[1] == '-h' or sys.argv[1] == '--help':
    print (helpstr)
    sys.exit(1)

final=""
for i in sys.argv[1:]:
    final+=chr(int(i,16))

file=os.path.join(os.environ['HOME'],"host_c/Users/laksh/Downloads/a.txt")
fd=open(file,'w')
print (final, end="", file=fd)
print ("Written to %s"%file)
