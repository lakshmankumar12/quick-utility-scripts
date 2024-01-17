#!/usr/bin/env python

from pushbullet import Pushbullet
import sys
import os

if len(sys.argv) != 2:
  print ("Usage %s <message>"%sys.argv[0])
  sys.exit(1)

with open (os.path.join(os.environ['HOME'], '.push_bullet_key')) as fd:
    api_key = fd.read().strip()

pb = Pushbullet(api_key)

mobile_string='Xiaomi 2201116TI'
try:
  mobile = [ i for i in pb.devices if mobile_string in str(i) ][0]
except IndexError:
  print ("Huh: couldn't find mobile_string(%s) in %s"%(mobile_string, pb.devices))
  sys.exit(1)
mobile.push_note("Dev-Machine-Notification", sys.argv[1])
