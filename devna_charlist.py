#!/usr/local/bin/python3

## reference: https://en.wikipedia.org/wiki/Devanagari#Unicode

devna_helpstr = '''
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
  Om  half  bindu  single  double
      bindu        line    line
  Om  hbi    bi    ;       .

  silentA

  sa

  hy  sp   nl  cm
  -   ' '  \n  ,
'''

devna_charlist = {}
devna_charlist['k']  = '\u0915'
devna_charlist['K']  = '\u0916'
devna_charlist['g']  = '\u0917'
devna_charlist['G']  = '\u0918'
devna_charlist['gn'] = '\u0919'
devna_charlist['c']  = '\u091a'
devna_charlist['C']  = '\u091b'
devna_charlist['j']  = '\u091c'
devna_charlist['J']  = '\u091d'
devna_charlist['gy'] = '\u091e'
devna_charlist['t']  = '\u091f'
devna_charlist['T']  = '\u0920'
devna_charlist['d']  = '\u0921'
devna_charlist['D']  = '\u0922'
devna_charlist['N']  = '\u0923'
devna_charlist['th'] = '\u0924'
devna_charlist['Th'] = '\u0925'
devna_charlist['dh'] = '\u0926'
devna_charlist['Dh'] = '\u0927'
devna_charlist['n']  = '\u0928'
devna_charlist['p']  = '\u092a'
devna_charlist['P']  = '\u092b'
devna_charlist['b']  = '\u092c'
devna_charlist['B']  = '\u092d'
devna_charlist['m']  = '\u092e'
devna_charlist['y']  = '\u092f'
devna_charlist['r']  = '\u0930'
devna_charlist['l']  = '\u0932'
devna_charlist['v']  = '\u0935'
devna_charlist['sh'] = '\u0936'
devna_charlist['Sh'] = '\u0937'
devna_charlist['s']  = '\u0938'
devna_charlist['h']  = '\u0939'

devna_charlist['Om'] = '\u0950'
devna_charlist['bi'] = '\u0901'
devna_charlist['hbi'] = '\ua8f3'
devna_charlist[';'] = '\u0964'
devna_charlist['.'] = '\u0965'
devna_charlist['sa'] = '\u093d'

devna_charlist['sp'] = ' '
devna_charlist['nl'] = '\n'
devna_charlist['cm'] = ','
devna_charlist['hy'] = '-'

devna_charlist['a']  = '\u0905'
devna_charlist['A']  = '\u0906'
devna_charlist['e']  = '\u0907'
devna_charlist['E']  = '\u0908'
devna_charlist['u']  = '\u0909'
devna_charlist['U']  = '\u090a'
devna_charlist['R']  = '\u090b'
devna_charlist['ae'] = '\u090f'
devna_charlist['i']  = '\u0910'
devna_charlist['O']  = '\u0913'
devna_charlist['w']  = '\u0914'

devna_charlist['-h']  = '\u094d'
devna_charlist['-A']  = '\u093e'
devna_charlist['-e']  = '\u093f'
devna_charlist['-E']  = '\u0940'
devna_charlist['-u']  = '\u0941'
devna_charlist['-U']  = '\u0942'
devna_charlist['-R']  = '\u0943'
devna_charlist['-ae'] = '\u0947'
devna_charlist['-i']  = '\u0948'
devna_charlist['-O']  = '\u094b'
devna_charlist['-w']  = '\u094c'
devna_charlist['-m']  = '\u0902'
devna_charlist['-H']  = '\u0903'
devna_charlist['-s']  = '\u0951'
devna_charlist['-a']  = '\u0952'
#devna_charlist['-d']  = '"'
devna_charlist['-d']  = '\u1cda'

devna_charlist['0']  = '\u0966'
devna_charlist['1']  = '\u0967'
devna_charlist['2']  = '\u0968'
devna_charlist['3']  = '\u0969'
devna_charlist['4']  = '\u096a'
devna_charlist['5']  = '\u096b'
devna_charlist['6']  = '\u096c'
devna_charlist['7']  = '\u096d'
devna_charlist['8']  = '\u096e'
devna_charlist['9']  = '\u096f'


consonants =  set()
consonants.update({ 'k',  'K',  'g',  'G',  'gn' })
consonants.update({ 'c',  'C',  'j',  'J',  'gy' })
consonants.update({ 't',  'T',  'd',  'D',  'N' })
consonants.update({ 'th', 'Th', 'dh', 'Dh', 'n' })
consonants.update({ 'p',  'P',  'b',  'B',  'm' })
consonants.update({ 'y',  'r',  'l',  'v' })
consonants.update({ 'sh', 'Sh', 's',  'h' })

vowels = set()
vowels.update({ 'a'  , 'A'  , 'e'  , 'E'  , 'u'  , 'U',  'R' })
vowels.update({ 'ae' , 'i'  , 'O'  , 'w'})

vowelizers = set()
vowelizers.update({ '-a'  , '-A'  , '-e'  , '-E'  , '-u'  , '-U',  '-R' })
vowelizers.update({ '-ae' , '-i'  , '-O'  , '-w'})

# these can follow a previous vowelizer
vowelizers2 = set()
vowelizers2.update({ '-m', '-H', 'bi', 'hbi' })

# half
halfizer = '-h'

# swaras
swaras = set()
swaras.update({ '-s',  '-a'  , '-d' })

space = ' '
newline = '\n'

known_chars = {v:k for k,v in devna_charlist.items()}
