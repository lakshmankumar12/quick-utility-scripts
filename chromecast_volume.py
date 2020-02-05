#! /usr/bin/env python3

import sys
import time

import pychromecast

requested_volume = float(sys.argv[1]) if len(sys.argv) > 1 else None

casts = pychromecast.get_chromecasts()
try:
    cast = next(c for c in casts if 'VaishKum' in c.device.friendly_name)
except StopIteration:
    print ("No chromecast - VaishKum")
    sys.exit(1)

cast.wait()

if requested_volume != None:
    cast.set_volume(requested_volume)
    print ("Volume set to {:.2f}".format(requested_volume))
else:
    print ("{:.2f}".format(cast.status.volume_level))
