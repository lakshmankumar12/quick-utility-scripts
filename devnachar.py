#!/usr/local/bin/python3

import sys
from devna_charlist import (
            devna_helpstr,
            devna_charlist
        )

if sys.argv[1] == '-h' or sys.argv[1] == '--help':
    print (devnahelpstr)
    sys.exit(1)

final=""
for i in sys.argv[1:]:
    if i in devna_charlist:
        final += devna_charlist[i]
    else:
        print("bad-char: %s"%i)

print (final, end="")
