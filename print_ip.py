#!/usr/bin/python

import sys

def usage():
    print ("usage %s <ip1InDec> [<ip2InDec>... ]")
    sys.exit(1)

def ip(val):
    oct1=(val&0xff000000) >> 24;
    oct2=(val&0xff0000) >> 16;
    oct3=(val&0xff00) >> 8;
    oct4=(val&0xff);
    s1="%d.%d.%d.%d"%(oct1,oct2,oct3,oct4)
    s2="%d.%d.%d.%d"%(oct4,oct3,oct2,oct1)
    oV=(oct4 << 24) | (oct3 << 16) | (oct2 << 8) | oct1
    return (s1,s2,oV)

if len(sys.argv) < 2:
    usage()

for n,i in enumerate(sys.argv[1:],1):
    (s1,s2,oV) = ip(int(i))
    print ("%3d Val:%12s HostOrd:%16s OtherOrd:%16s OtherVal:%12d"%(n,i,s1,s2,oV))
