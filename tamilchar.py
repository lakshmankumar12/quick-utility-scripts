#!/usr/local/bin/python3

import sys

helpstr = '''
  vowels:
  a   A   e   E   u   U
  ae  AE  i   o   O   w
  half:
  -h
  consonants:
  k   gn  c   gy  d  N
  t   nn  p   m   y  r
  l   v   L   z   R  n
  s   S   h   j  sh
'''

charlist = {}
charlist['k']  = '\u0b95'
charlist['gn'] = '\u0b99'
charlist['c']  = '\u0b9a'
charlist['gy'] = '\u0b9e'
charlist['d']  = '\u0b9f'
charlist['N']  = '\u0ba3'
charlist['t']  = '\u0ba4'
charlist['nn'] = '\u0ba8'
charlist['p']  = '\u0baa'
charlist['m']  = '\u0bae'
charlist['y']  = '\u0baf'
charlist['r']  = '\u0bb0'
charlist['l']  = '\u0bb2'
charlist['v']  = '\u0bb5'
charlist['L']  = '\u0bb3'
charlist['z']  = '\u0bb4'
charlist['R']  = '\u0bb1'
charlist['n']  = '\u0ba9'
charlist['s']  = '\u0bb8'
charlist['S']  = '\u0bb7'
charlist['h']  = '\u0bb9'
charlist['j']  = '\u0b9c'
charlist['sh'] = '\u0bb6'

charlist['sp'] = ' '
charlist['nl'] = '\n'

charlist['a']  = '\u0b85'
charlist['A']  = '\u0b86'
charlist['e']  = '\u0b87'
charlist['E']  = '\u0b88'
charlist['u']  = '\u0b89'
charlist['U']  = '\u0b8a'
charlist['ae'] = '\u0b8e'
charlist['AE'] = '\u0b8f'
charlist['i']  = '\u0b90'
charlist['o']  = '\u0b92'
charlist['O']  = '\u0b93'
charlist['w']  = '\u0b94'

charlist['-h']  = '\u0bcd'
charlist['-A']  = '\u0bbe'
charlist['-e']  = '\u0bbf'
charlist['-E']  = '\u0bc0'
charlist['-u']  = '\u0bc1'
charlist['-U']  = '\u0bc2'
charlist['-ae'] = '\u0bc6'
charlist['-AE'] = '\u0bc7'
charlist['-i']  = '\u0bc8'
charlist['-o']  = '\u0bca'
charlist['-O']  = '\u0bcb'
charlist['-w']  = '\u0bcc'

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
