#!/usr/bin/python

import sys

print ("no args received:%d"%len(sys.argv))
for n,i in enumerate(sys.argv):
  print ("arg %d is %s"%(n,i))
