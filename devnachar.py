#!/usr/local/bin/python3

import sys

helpstr = '''
  vowels:
  a   A   e   E   u   U   R
  ae  i   O   w  -m  -H
  half: sva:  anud: d.sva:
  -h    -s    -a     -d
  consonants:
  k   K   g   G  gn
  c   C   j   J  gy
  t   T   d   D  N
  th  Th  dh  Dh n
  p   P   b   B  m
  y   r   l   v
  sh  Sh  s   h
  Misc:
  sp  nl
'''

charlist = {}
charlist['k']  = '\u0915'
charlist['K']  = '\u0916'
charlist['g']  = '\u0917'
charlist['G']  = '\u0918'
charlist['gn'] = '\u0919'
charlist['c']  = '\u091a'
charlist['C']  = '\u091b'
charlist['j']  = '\u091c'
charlist['J']  = '\u091d'
charlist['gy'] = '\u091e'
charlist['t']  = '\u091f'
charlist['T']  = '\u0920'
charlist['d']  = '\u0921'
charlist['D']  = '\u0922'
charlist['N']  = '\u0923'
charlist['th'] = '\u0924'
charlist['Th'] = '\u0925'
charlist['dh'] = '\u0926'
charlist['Dh'] = '\u0927'
charlist['n']  = '\u0928'
charlist['p']  = '\u092a'
charlist['P']  = '\u092b'
charlist['b']  = '\u092c'
charlist['B']  = '\u092d'
charlist['m']  = '\u092e'
charlist['y']  = '\u092f'
charlist['r']  = '\u0930'
charlist['l']  = '\u0932'
charlist['v']  = '\u0935'
charlist['sh'] = '\u0936'
charlist['Sh'] = '\u0937'
charlist['s']  = '\u0938'
charlist['h']  = '\u0939'

charlist['sp'] = ' '
charlist['nl'] = '\n'

charlist['a']  = '\u0905'
charlist['A']  = '\u0906'
charlist['e']  = '\u0907'
charlist['E']  = '\u0908'
charlist['u']  = '\u0909'
charlist['U']  = '\u090a'
charlist['R']  = '\u090b'
charlist['ae'] = '\u090f'
charlist['i']  = '\u0910'
charlist['O']  = '\u0913'
charlist['w']  = '\u0914'

charlist['-h']  = '\u094d'
charlist['-A']  = '\u093e'
charlist['-e']  = '\u093f'
charlist['-E']  = '\u0940'
charlist['-u']  = '\u0941'
charlist['-U']  = '\u0942'
charlist['-R']  = '\u0943'
charlist['-ae'] = '\u0947'
charlist['-i']  = '\u0948'
charlist['-O']  = '\u094b'
charlist['-w']  = '\u094c'
charlist['-m']  = '\u0902'
charlist['-H']  = '\u0903'
charlist['-s']  = '\u0951'
charlist['-a']  = '\u0952'
#charlist['-d']  = '"'
charlist['-d']  = '\u1cda'

if sys.argv[1] == '-h' or sys.argv[1] == '--help':
    print (helpstr)
    sys.exit(1)

final=""
for i in sys.argv[1:]:
    if i in charlist:
        final += charlist[i]
    else:
        print("bad-char: %s"%i)

print (final, end="")
