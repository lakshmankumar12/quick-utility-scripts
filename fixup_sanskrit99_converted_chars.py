#!/usr/local/bin/python3

import sys
import os

helpstr='''
    Just supply the chars to fixup via stdin
    The result will be saved in ~/host_c/Users/laksh/Downloads/a.txt
'''

if len(sys.argv) > 1:
    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print (helpstr)
        sys.exit(1)

first_chars=set(['\u0951', '\u0952', '\u1cda'])
second_chars=set([
                '\u093e',   # -A
                '\u093f',   # -e
                '\u0940',   # -E
                '\u0941',   # -u
                '\u0942',   # -U
                '\u0943',   # -R
                '\u0947',   # -ae
                '\u0948',   # -i
                '\u094b',   # -O
                '\u094c',   # -w
                '\u0902',   # -m
                '\u0903',   # -H
            ])

bha_count=0
def regular_char_processing(char):
    global bha_count
    if char == '\u002d':
        bha_count += 1
        char = '\u092d'
    elif char == '\u2021':
        char = '\ua8f3'
    return char

staging=""
final=""
for line in sys.stdin:
    for char in line:
        if not staging:
            if char not in first_chars:
                final+=regular_char_processing(char)
            else:
                staging=char
        else:
            if char not in second_chars:
                final+=staging
                final+=regular_char_processing(char)
            else:
                final+=char
                final+=staging
            staging=""


file=os.path.join(os.environ['HOME'],"host_c/Users/laksh/Downloads/a.txt")
fd=open(file,'w')
print (final, end="", file=fd)

if bha_count:
    print(f"there were {bha_count} hyphens converted to Bha")
